import httpx
from collections import defaultdict
from pprint import pprint
from collections import Counter

from sqlalchemy.orm import Session
from app.models.gpu import Flavor, ServerGpuMapping
from app.db.session import SessionLocal
from app.core.config import PROMETHEUS_URL, v1_api
from app.models.k8s import PodCreation
from app.models.user import User
from app.core.logger import app_logger

url = f"http://{PROMETHEUS_URL}/api/v1/query"

async def query_prometheus(query: str):
    async with httpx.AsyncClient() as client_http:
        response = await client_http.get(url+'?query='+query)
    if response.status_code != 200:
        raise Exception(f"Prometheus query failed: {response.text}")
    result = response.json()
    return result.get("data", {}).get("result", [])

async def fetch_gpu_status_from_prometheus():
    query = 'DCGM_FI_DEV_MIG_MODE'
    data = await query_prometheus(query)
    flavors = dict()
    for item in data:
        metric = item["metric"]
        worker_node = metric.get("Hostname")
        gpu_id = int(metric.get("gpu", 0))
        # MIG 인스턴스
        if "GPU_I_PROFILE" in metric:
            gpu_name = metric["GPU_I_PROFILE"]
            mig_id = int(metric.get("GPU_I_ID", None))
        # Non-MIG
        elif "modelName" in metric:
            gpu_name = metric["modelName"].removeprefix("NVIDIA ").strip()
            mig_id = None
        else:
            continue

        if metric.get("exported_pod"):
            flavors[(worker_node, gpu_id, mig_id, gpu_name)] = 1
        else:
            flavors[(worker_node, gpu_id, mig_id, gpu_name)] = 0
    return flavors

async def get_cpu_memory_from_k8s(pod_name, namespace=None):
    """
    pod_name과 (선택적으로) namespace를 받아 해당 pod의 cpu, memory limit를 반환합니다.
    """
    try:
        if namespace is None:
            # namespace가 주어지지 않으면 default로 설정
            namespace = "default"
        
        pod = v1_api.read_namespaced_pod(name=pod_name, namespace=namespace)
        container = pod.spec.containers[0]  # 첫 번째 컨테이너 가정
        
        limits = container.resources.limits or {}
        cpu = limits.get('cpu', 'N/A')
        memory = limits.get('memory', 'N/A')
        
        return cpu, memory
    except Exception as e:
        app_logger.error(f"Pod {pod_name}의 CPU/Memory 정보를 가져오는 중 오류: {e}")
        return "N/A", "N/A"

async def get_pod_internal_ip(pod_name, namespace=None):
    """
    pod_name과 (선택적으로) namespace를 받아 해당 pod의 internal IP를 반환합니다.
    """
    try:
        if namespace is None:
            namespace = "default"
        
        pod = v1_api.read_namespaced_pod(name=pod_name, namespace=namespace)
        internal_ip = pod.status.pod_ip
        
        return internal_ip
    except Exception as e:
        app_logger.error(f"Pod {pod_name}의 Internal IP를 가져오는 중 오류: {e}")
        return None

async def sync_flavors_to_db():
    db: Session = SessionLocal()
    try:
        # 1. Prometheus에서 모든 GPU 정보 추출
        prometheus_flavors = await fetch_gpu_status_from_prometheus()  # {(worker_node, gpu_id, gpu_name): 0}
        # 2. k8s에서 사용중인 GPU 추출
        # used_gpus = await fetch_used_gpus_from_k8s()  # set of (worker_node, gpu_id)
        # # 3. 사용중인 GPU는 available=1로 표시
        # for (worker_node, gpu_id, gpu_name) in prometheus_flavors.keys():
        #     if (worker_node, gpu_id) in used_gpus:
        #         prometheus_flavors[(worker_node, gpu_id, gpu_name)] = 1
        # 4. DB 동기화 (upsert & delete)
        db_flavors = db.query(Flavor).all()
        db_flavor_keys = {(f.worker_node, f.gpu_id, f.gpu_name) for f in db_flavors}
        prometheus_keys = set(prometheus_flavors.keys())
        # upsert 및 삭제 전, key를 항상 정규화
        def normalize_key(worker_node, gpu_id, mig_id, gpu_name):
            # mig_id는 변환하지 않고 그대로 사용
            return (
                str(worker_node).strip().lower() if worker_node else "",
                int(gpu_id) if gpu_id is not None else -1,
                mig_id,  # 변환 없이 그대로
                str(gpu_name).strip().lower() if gpu_name else ""
            )

        # upsert
        for (worker_node, gpu_id, mig_id, gpu_name), available in prometheus_flavors.items():
            norm_key = normalize_key(worker_node, gpu_id, mig_id, gpu_name)
            flavor = db.query(Flavor).filter(
                Flavor.worker_node == norm_key[0],
                Flavor.gpu_id == norm_key[1],
                Flavor.mig_id == norm_key[2], # mig_id는 그대로 비교
                Flavor.gpu_name == norm_key[3]
            ).first()
            if flavor:
                flavor.available = available
            else:
                db.add(Flavor(
                    worker_node=norm_key[0],
                    gpu_id=norm_key[1],
                    mig_id=norm_key[2], # mig_id는 그대로 저장
                    gpu_name=norm_key[3],
                    available=available
                ))

        # delete
        db_flavor_keys = {normalize_key(f.worker_node, f.gpu_id, f.mig_id, f.gpu_name) for f in db_flavors} # mig_id는 그대로 비교
        prometheus_keys = {normalize_key(*k) for k in prometheus_flavors.keys()}

        for flavor in db_flavors:
            norm_key = normalize_key(flavor.worker_node, flavor.gpu_id, flavor.mig_id, flavor.gpu_name) # mig_id는 그대로 비교
            if norm_key not in prometheus_keys:
                db.delete(flavor)
        db.commit()
        app_logger.info(f"동기화된 flavor: {len(prometheus_flavors)}개")
    finally:
        db.close()

def extract_user_name_from_pod(pod_name):
    # 예: jupyter-js-lee---a4b212d2 → js.lee
    if pod_name.startswith("jupyter-"):
        parts = pod_name.split('-')
        if len(parts) >= 3:
            return f"{parts[1]}.{parts[2]}"
    return None

async def sync_gpu_pod_status_from_prometheus():
    db = SessionLocal()
    try:
        data = await query_prometheus('DCGM_FI_DEV_MIG_MODE')
    
        
        # 1. Prometheus에서 현재 실행 중인 Pod 목록 수집
        prometheus_pods = set()
        
        # 1. pod별로 점유한 gpu_name 모으기
        pod_gpu_map = defaultdict(list)
        pod_info_map = dict()  # pod별로 기타 정보 저장
        pod_gpu_details = defaultdict(list)  # pod별로 상세 GPU 정보 저장 (worker_node, gpu_id, mig_id, gpu_name)

        for item in data:
            metric = item["metric"]
            exported_pod = metric.get("exported_pod")
            if not exported_pod:
                continue
            
            prometheus_pods.add(exported_pod)  # 현재 실행 중인 Pod 목록에 추가
            
            # GPU 이름 추출
            if "GPU_I_PROFILE" in metric:
                gpu_name = metric["GPU_I_PROFILE"]
                # GPU_I_ID가 None이면 None으로 두기
                mig_id_raw = metric.get("GPU_I_ID")
                mig_id = int(mig_id_raw) if mig_id_raw is not None else None
            else:
                gpu_name = metric.get("modelName", "").removeprefix("NVIDIA ").strip()
                mig_id = None
            
            worker_node = metric.get("Hostname")
            gpu_id = int(metric.get("gpu", 0))
            
            pod_gpu_map[exported_pod].append(gpu_name)
            pod_gpu_details[exported_pod].append((worker_node, gpu_id, mig_id, gpu_name))
            # 기타 정보는 마지막 값으로 저장(필요시 더 정교하게)
            pod_info_map[exported_pod] = metric

        # 2. DB에서 서버들의 Pod 목록 조회
        db_servers = db.query(PodCreation).all()
        
        # 3. DB에는 있지만 Prometheus에는 없는 Pod 찾기 (삭제된 Pod)
        deleted_pods = []
        for server in db_servers:
            if server.pod_name not in prometheus_pods and server.tags != 'LEGEND':
                deleted_pods.append(server)
        
        # 4. 삭제된 Pod들을 DB에서 제거
        for server in deleted_pods:
            # 관련 GPU 매핑도 삭제
            db.query(ServerGpuMapping).filter(ServerGpuMapping.server_id == server.id).delete()
            db.delete(server)

        # 5. 현재 실행 중인 Pod들 처리 (기존 로직)
        for pod_name, gpu_names in pod_gpu_map.items():
            app_logger.debug(f"pod_name: {pod_name} gpu_names: {gpu_names}")
            
            gpu_counter = Counter(gpu_names)
            gpu_str_list = []
            for name, count in gpu_counter.items():
                if count > 1:
                    gpu_str_list.append(f"{name} * {count}")
                else:
                    gpu_str_list.append(name)
            gpu_str = ", ".join(gpu_str_list)
            metric = pod_info_map[pod_name]
            
            
            if pod_name.startswith("ailabserver-"):
                server = db.query(PodCreation).filter(PodCreation.pod_name == pod_name).first()
            else:
                # user_name 추출 및 user_id 조회
                user_name = extract_user_name_from_pod(pod_name)
                user = db.query(User).filter(User.name == user_name).first()
                if not user:
                    user = db.query(User).filter(User.name == "dev").first()
                user_id = user.id if user else None

                # cpu, memory 정보 가져오기
                namespace = metric.get("exported_namespace") or metric.get("namespace") or "default"
                cpu, memory = await get_cpu_memory_from_k8s(pod_name, namespace)
                
                # internal IP 가져오기
                internal_ip = await get_pod_internal_ip(pod_name, namespace)
                
                # tags 결정
                if pod_name.startswith("jupyter-"):
                    tags = "JUPYTER"
                elif pod_name.startswith("ailabserver-"):
                    tags = "DASHBOARD"
                else:
                    tags = "DEV"

                # servers 테이블 upsert (LEGEND 태그가 아닌 경우만)
                server = db.query(PodCreation).filter(
                    PodCreation.pod_name == pod_name,
                    (PodCreation.tags != 'LEGEND') | (PodCreation.tags.is_(None))
                ).first()
                
                if server:
                    server.gpu = gpu_str
                    server.cpu = cpu
                    server.memory = memory
                    if internal_ip:
                        server.internal_ip = internal_ip
                    server.tags = tags  # 항상 태그 업데이트
                    if server.status != "Running":
                        server.status = "Running"

                else:
                    # LEGEND 태그인 서버가 이미 있는지 확인
                    existing_legend = db.query(PodCreation).filter(
                        PodCreation.pod_name == pod_name,
                        PodCreation.tags == 'LEGEND'
                    ).first()
                    
                    if not existing_legend:
                        # LEGEND가 아니고 새로운 서버인 경우에만 생성
                        server = PodCreation(
                            user_id=user_id,
                            server_name=pod_name,
                            pod_name=pod_name,
                            cpu=cpu,
                            memory=memory,
                            gpu=gpu_str,
                            description=None,
                            internal_ip=internal_ip,
                            status="Running",
                            tags=tags
                        )
                        db.add(server)
                        db.flush()  # server.id를 얻기 위해 flush
                        pass  # 새 서버 생성됨
                    else:
                        continue  # LEGEND 태그 서버는 건너뜀
                        continue

            # 서버-GPU 매핑 처리 (LEGEND가 아닌 경우만)
            if server:
                # 기존 매핑 삭제
                deleted_count = db.query(ServerGpuMapping).filter(ServerGpuMapping.server_id == server.id).delete()
                
                # 새로운 매핑 추가
                mapping_count = 0
                for worker_node, gpu_id, mig_id, gpu_name in pod_gpu_details[pod_name]:

                    
                    # 정규화 함수를 외부에서 정의 (매번 새로 정의하지 않도록)
                    norm_worker_node = str(worker_node).strip().lower() if worker_node else ""
                    norm_gpu_id = int(gpu_id) if gpu_id is not None else -1
                    norm_mig_id = mig_id  # mig_id는 None일 수 있음
                    norm_gpu_name = str(gpu_name).strip().lower() if gpu_name else ""
                    

                    
                    # gpu_flavor 테이블에서 해당 GPU 찾기
                    query = db.query(Flavor).filter(
                        Flavor.worker_node == norm_worker_node,
                        Flavor.gpu_id == norm_gpu_id,
                        Flavor.gpu_name == norm_gpu_name
                    )
                    
                    # mig_id 조건 추가 (None 처리 포함)
                    if norm_mig_id is None:
                        query = query.filter(Flavor.mig_id.is_(None))
                    else:
                        query = query.filter(Flavor.mig_id == norm_mig_id)
                    
                    gpu_flavor = query.first()
                    
                    if gpu_flavor:
                        # 중복 체크
                        existing_mapping = db.query(ServerGpuMapping).filter(
                            ServerGpuMapping.server_id == server.id,
                            ServerGpuMapping.gpu_id == gpu_flavor.id
                        ).first()
                        
                        if not existing_mapping:
                            # 매핑 추가
                            mapping = ServerGpuMapping(
                                server_id=server.id,
                                gpu_id=gpu_flavor.id
                            )
                            db.add(mapping)
                            mapping_count += 1


        db.commit()
    except Exception as e:
        app_logger.error(f"sync_gpu_pod_status_from_prometheus 실행 중 오류: {e}")
        db.rollback()
        raise
    finally:
        db.close()
