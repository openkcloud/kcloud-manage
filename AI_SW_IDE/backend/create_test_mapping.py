#!/usr/bin/env python3
import sys
import os

# 현재 경로를 Python path에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models.gpu import ServerGpuMapping, Flavor
from app.models.k8s import PodCreation
from app.models.user import User
from app.db.session import SessionLocal

def create_test_mapping():
    """사용자가 제공한 데이터에 맞는 테스트 매핑을 생성합니다."""
    db = SessionLocal()
    try:
        # 기존 데이터 확인
        servers = db.query(PodCreation).all()
        flavors = db.query(Flavor).all()
        users = db.query(User).all()
        
        print(f"서버 개수: {len(servers)}")
        print(f"GPU Flavor 개수: {len(flavors)}")
        print(f"사용자 개수: {len(users)}")
        
        # 기존 매핑 삭제
        db.query(ServerGpuMapping).delete()
        print("기존 매핑 데이터 삭제 완료")
        
        # 사용자 데이터에 맞는 매핑 생성
        # server_id | gpu_id
        # ----------+--------
        #    12     | 120
        #    13     | 122
        #    14     | 118
        #    15     | 118
        #    15     | 119
        
        test_mappings = [
            (12, 120),  # server_id 12 -> gpu_id 120 
            (13, 122),  # server_id 13 -> gpu_id 122  
            (14, 118),  # server_id 14 -> gpu_id 118 
            (15, 118),  # server_id 15 -> gpu_id 118 
            (15, 119),  # server_id 15 -> gpu_id 119 
        ]
        
        created_count = 0
        for server_id, gpu_flavor_id in test_mappings:
            # 서버와 GPU가 실제로 존재하는지 확인
            server = db.query(PodCreation).filter(PodCreation.id == server_id).first()
            flavor = db.query(Flavor).filter(Flavor.id == gpu_flavor_id).first()
            
            if server and flavor:
                mapping = ServerGpuMapping(server_id=server_id, gpu_id=gpu_flavor_id)
                db.add(mapping)
                created_count += 1
                print(f"매핑 생성: server_id={server_id} ({server.pod_name}) -> gpu_id={gpu_flavor_id} ({flavor.gpu_name})")
            else:
                print(f"매핑 실패: server_id={server_id} 또는 gpu_id={gpu_flavor_id}가 존재하지 않음")
                if not server:
                    print(f"  - 서버 {server_id}를 찾을 수 없음")
                if not flavor:
                    print(f"  - GPU Flavor {gpu_flavor_id}를 찾을 수 없음")
        
        db.commit()
        print(f"\n총 {created_count}개의 매핑이 생성되었습니다.")
        
        # 결과 확인
        mappings = db.query(ServerGpuMapping).all()
        print(f"\n=== 최종 매핑 결과 ({len(mappings)}개) ===")
        for mapping in mappings:
            server = db.query(PodCreation).filter(PodCreation.id == mapping.server_id).first()
            flavor = db.query(Flavor).filter(Flavor.id == mapping.gpu_id).first()
            user = db.query(User).filter(User.id == server.user_id).first() if server else None
            
            if server and flavor:
                user_name = user.name if user else 'Unknown'
                print(f"server_id: {mapping.server_id} ({server.pod_name}) -> gpu_id: {mapping.gpu_id} ({flavor.gpu_name}) - User: {user_name}")
            
    except Exception as e:
        print(f"오류 발생: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_mapping() 