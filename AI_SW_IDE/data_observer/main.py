import os
import stat
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel


app = FastAPI(
    title="Data Observer API",
    description="NFS 볼륨의 데이터 상태를 모니터링하는 API",
    version="1.0.0"
)

# NFS 볼륨 마운트 포인트
NFS_ROOT = os.getenv("NFS_ROOT", "/home/jovyan")

class FileInfo(BaseModel):
    name: str
    type: str  # 'file' or 'directory'
    extension: Optional[str] = None  # 파일 확장자 (디렉터리는 None)
    size: int  # bytes
    size_human: str  # human readable size
    modified: datetime
    permissions: str

class DirectoryResponse(BaseModel):
    path: str
    total_items: int
    total_size: int
    total_size_human: str
    items: List[FileInfo]

def get_human_readable_size(size_bytes: int) -> str:
    """바이트를 사람이 읽기 쉬운 형태로 변환"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB", "TB", "PB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"

def get_file_info(file_path: Path, calculate_dir_size: bool = False) -> FileInfo:
    """파일/디렉터리 정보를 가져옴"""
    try:
        stat_info = file_path.stat()
        
        # 파일 타입 결정
        file_type = "directory" if file_path.is_dir() else "file"
        
        # 크기 계산
        if file_type == "file":
            size = stat_info.st_size
        elif file_type == "directory" and calculate_dir_size:
            # 디렉터리의 경우 하위 모든 파일 크기 계산
            size = calculate_directory_size(file_path)
        else:
            # 디렉터리지만 계산하지 않는 경우
            size = 0
        
        # 확장자 추출
        extension = None
        if file_type == "file":
            name_parts = file_path.name.rsplit('.', 1)
            if len(name_parts) > 1:
                extension = name_parts[1]
        
        # 권한 정보
        mode = stat_info.st_mode
        permissions = stat.filemode(mode)
        
        # 수정 시간
        modified = datetime.fromtimestamp(stat_info.st_mtime)
        
        return FileInfo(
            name=file_path.name,
            type=file_type,
            extension=extension,
            size=size,
            size_human=get_human_readable_size(size),
            modified=modified,
            permissions=permissions
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 정보를 가져올 수 없습니다: {str(e)}")

def vscode_sort(items: List[FileInfo]) -> List[FileInfo]:
    """VSCode 스타일 정렬: 디렉터리 먼저, 그 다음 파일들을 이름순으로"""
    directories = [item for item in items if item.type == "directory"]
    files = [item for item in items if item.type == "file"]
    
    # 각각을 이름순으로 정렬 (대소문자 구분 없이)
    directories.sort(key=lambda x: x.name.lower())
    files.sort(key=lambda x: x.name.lower())
    
    # 디렉터리 먼저, 그 다음 파일
    return directories + files

def calculate_directory_size(directory_path: Path) -> int:
    """디렉터리의 총 크기를 계산 (하위 디렉터리 포함)"""
    total_size = 0
    try:
        for item in directory_path.rglob('*'):
            if item.is_file():
                try:
                    total_size += item.stat().st_size
                except (OSError, PermissionError):
                    continue
    except (OSError, PermissionError):
        pass
    return total_size

@app.get("/")
def root():
    return {
        "message": "Data Observer API",
        "version": "1.0.0",
        "nfs_root": NFS_ROOT
    }

@app.get("/browse", response_model=DirectoryResponse)
def browse_directory(
    path: str = Query("/", description="브라우징할 경로 (NFS 루트 상대경로)"),
    include_hidden: bool = Query(False, description="숨김 파일 포함 여부"),
    sort_by: str = Query("vscode", description="정렬 기준: vscode, name, size, modified, type"),
    calculate_dir_size: bool = Query(True, description="디렉터리의 실제 크기를 계산할지 여부 (시간이 오래 걸릴 수 있음)")
):
    """지정된 경로의 디렉터리 내용을 반환"""
    
    # 경로 정규화 및 보안 검증
    if path.startswith("/"):
        path = path[1:]  # 앞의 / 제거
    
    # .. 경로 조작 방지
    if ".." in path:
        raise HTTPException(status_code=400, detail="상위 디렉터리 접근은 허용되지 않습니다")
    
    full_path = Path(NFS_ROOT) / path
    
    # 경로 존재 여부 확인
    if not full_path.exists():
        raise HTTPException(status_code=404, detail=f"경로를 찾을 수 없습니다: {path}")
    
    # 디렉터리인지 확인
    if not full_path.is_dir():
        raise HTTPException(status_code=400, detail=f"지정된 경로는 디렉터리가 아닙니다: {path}")
    
    try:
        # 디렉터리 항목 수집
        items = []
        total_size = 0
        
        for item in full_path.iterdir():
            # 숨김 파일 처리
            if not include_hidden and item.name.startswith('.'):
                continue
            
            try:
                file_info = get_file_info(item, calculate_dir_size)
                items.append(file_info)
                
                # 파일인 경우 크기 누적
                if file_info.type == "file":
                    total_size += file_info.size
                    
            except Exception as e:
                print(f"파일 정보 가져오기 실패: {item.name}, 오류: {e}")
                continue
        
        # 정렬
        if sort_by == "vscode":
            items = vscode_sort(items)
        else:
            sort_key_map = {
                "name": lambda x: x.name.lower(),
                "size": lambda x: x.size,
                "modified": lambda x: x.modified,
                "type": lambda x: (x.type, x.name.lower())  # 디렉터리 먼저, 그다음 이름순
            }
            
            if sort_by in sort_key_map:
                items.sort(key=sort_key_map[sort_by])
        
        return DirectoryResponse(
            path=f"/{path}" if path else "/",
            total_items=len(items),
            total_size=total_size,
            total_size_human=get_human_readable_size(total_size),
            items=items
        )
        
    except PermissionError:
        raise HTTPException(status_code=403, detail="디렉터리에 접근할 권한이 없습니다")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"디렉터리를 읽을 수 없습니다: {str(e)}")

@app.get("/info")
def get_path_info(path: str = Query("/", description="정보를 조회할 경로")):
    """특정 경로의 상세 정보 반환"""
    
    # 경로 정규화 및 보안 검증
    if path.startswith("/"):
        path = path[1:]
    
    if ".." in path:
        raise HTTPException(status_code=400, detail="상위 디렉터리 접근은 허용되지 않습니다")
    
    full_path = Path(NFS_ROOT) / path
    
    if not full_path.exists():
        raise HTTPException(status_code=404, detail=f"경로를 찾을 수 없습니다: {path}")
    
    try:
        file_info = get_file_info(full_path, True)  # /info 엔드포인트에서는 항상 디렉터리 크기 계산
        
        # 디렉터리인 경우 하위 항목 수와 총 크기 계산
        additional_info = {}
        if full_path.is_dir():
            try:
                child_count = len(list(full_path.iterdir()))
                dir_size = calculate_directory_size(full_path)
                additional_info.update({
                    "child_count": child_count,
                    "directory_size": dir_size,
                    "directory_size_human": get_human_readable_size(dir_size)
                })
            except PermissionError:
                additional_info["error"] = "하위 디렉터리 접근 권한 없음"
        
        return {
            "path": f"/{path}" if path else "/",
            "info": file_info,
            **additional_info
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 정보를 가져올 수 없습니다: {str(e)}")

@app.get("/health")
def health_check():
    """헬스 체크 엔드포인트"""
    nfs_accessible = os.path.exists(NFS_ROOT) and os.access(NFS_ROOT, os.R_OK)
    
    return {
        "status": "healthy" if nfs_accessible else "unhealthy",
        "nfs_root": NFS_ROOT,
        "nfs_accessible": nfs_accessible,
        "timestamp": datetime.now()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 