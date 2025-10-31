import React, { useState, useEffect } from "react";
import { useNavigate, useLocation, useParams } from "react-router-dom";
import {
  Card,
  Typography,
  IconButton,
  Spinner,
} from "@material-tailwind/react";
import {
  FolderIcon,
  DocumentIcon,
  ChevronRightIcon,
  ChevronLeftIcon,
  ServerIcon,
} from "@heroicons/react/24/solid";
import { fetchWithAuth } from "@/utils/auth";

// PVC 목록 카드 컴포넌트
function PVCCard({ pvc, onSelect }) {
  return (
    <Card 
      className="p-4 mb-4 hover:shadow-lg transition-shadow cursor-pointer border border-gray-200"
      onClick={() => onSelect(pvc)}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <ServerIcon className="w-8 h-8 text-blue-500" />
          <div>
            <Typography variant="h6" color="blue-gray" className="font-semibold">
              {pvc.pvc_name}
            </Typography>
            <Typography variant="small" color="gray" className="mt-1">
              {pvc.path}
            </Typography>
          </div>
        </div>
        <ChevronRightIcon className="w-5 h-5 text-gray-400" />
      </div>
    </Card>
  );
}

// 파일 브라우저 컴포넌트
function FileBrowser({ pvcId, pvcName, pvcPath, onBack }) {
  const location = useLocation();
  const navigate = useNavigate();
  
  // URL에서 현재 파일 경로 추출
  const urlParams = new URLSearchParams(location.search);
  const currentPath = urlParams.get('path') || pvcPath;
  
  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(false);
  const [fileData, setFileData] = useState(null);

  const fetchFiles = async (path = '') => {
    setLoading(true);
    try {
      const response = await fetchWithAuth(`/server/browse?pvc_id=${pvcId}&path=${encodeURIComponent(path)}`);
      if (!response.ok) {
        throw new Error('파일 목록을 불러올 수 없습니다');
      }
      const data = await response.json();
      setFileData(data);
      setEntries(data.items || []);
    } catch (error) {
      console.error("파일 목록 불러오기 실패:", error);
      setEntries([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFiles(currentPath);
  }, [currentPath, pvcId]);

  const handleFolderClick = (folderName) => {
    const newPath = `${currentPath}/${folderName}`;
    const newUrl = `${location.pathname}?pvc_id=${pvcId}&path=${encodeURIComponent(newPath)}`;
    navigate(newUrl);
  };

  const handleBack = () => {
    // 현재 경로가 PVC의 기본 경로와 같거나 더 짧으면 PVC 목록으로 돌아가기
    if (currentPath === pvcPath || currentPath.length <= pvcPath.length) {
      onBack();
      return;
    }
    
    const pvcSegments = pvcPath.split('/').filter(Boolean);
    const currentSegments = currentPath.split('/').filter(Boolean);
    
    // 현재 경로가 PVC 경로보다 긴 경우에만 뒤로가기 허용
    if (currentSegments.length > pvcSegments.length) {
      // 절대 경로로 부모 경로 생성 (맨 앞에 / 추가)
      const parentPath = '/' + currentSegments.slice(0, -1).join('/');
      
      // 부모 경로가 PVC 경로보다 짧아지지 않도록 확인
      if (parentPath.length >= pvcPath.length) {
        const newUrl = `${location.pathname}?pvc_id=${pvcId}&path=${encodeURIComponent(parentPath)}`;
        navigate(newUrl);
      } else {
        // PVC 기본 경로로 돌아가기
        const newUrl = `${location.pathname}?pvc_id=${pvcId}&path=${encodeURIComponent(pvcPath)}`;
        navigate(newUrl);
      }
    } else {
      onBack();
    }
  };

  return (
    <Card className="p-6 rounded-xl shadow-md border border-blue-gray-100 bg-white w-full">
      <div className="mb-4">
        <Typography variant="h5" color="blue-gray">
          {pvcName} - 파일 탐색기
        </Typography>
      </div>
      
      <div className="flex justify-between items-center mb-4">
        <div className="flex items-center space-x-2">
          <IconButton
            onClick={handleBack}
            ripple={false}
            className="border-gray-300 mr-2"
          >
            <ChevronLeftIcon className="w-5 h-5 text-gray-500" />
          </IconButton>
                   <Typography color="blue-gray">
           {currentPath === pvcPath ? "최상위 경로" : currentPath.replace(pvcPath, '')}
         </Typography>
        </div>
        
        {fileData && (
          <div className="text-sm text-gray-600">
            총 {fileData.total_items}개 항목 | {fileData.total_size_human}
          </div>
        )}
      </div>

      <div className="divide-y divide-gray-200">
        {loading ? (
          <div className="flex justify-center items-center h-32">
            <Spinner color="blue" />
          </div>
        ) : entries.length === 0 ? (
          <div className="text-center text-gray-500 py-10">비어 있습니다</div>
        ) : (
          entries.map((entry) => (
            <div
              key={entry.name}
              className={`flex items-center justify-between py-3 px-2 rounded-md transition cursor-pointer ${
                entry.type === "directory" ? "hover:bg-blue-50" : "hover:bg-gray-50"
              }`}
              onClick={() =>
                entry.type === "directory" && handleFolderClick(entry.name)
              }
            >
              <div className="flex items-center space-x-3">
                {entry.type === "directory" ? (
                  <FolderIcon className="w-5 h-5 text-yellow-600" />
                ) : (
                  <DocumentIcon className="w-5 h-5 text-gray-500" />
                )}
                <div>
                  <span className="text-sm font-medium">{entry.name}</span>
                  <div className="text-xs text-gray-500">
                    {entry.size_human} | {new Date(entry.modified).toLocaleDateString('ko-KR')}
                  </div>
                </div>
              </div>
              {entry.type === "directory" && (
                <ChevronRightIcon className="w-4 h-4 text-gray-400" />
              )}
            </div>
          ))
        )}
      </div>
    </Card>
  );
}

// 메인 StorageManagement 컴포넌트
export default function StorageManagement() {
  const location = useLocation();
  const navigate = useNavigate();
  
  // URL에서 PVC ID 추출
  const urlParams = new URLSearchParams(location.search);
  const selectedPvcId = urlParams.get('pvc_id');
  
  const [pvcList, setPvcList] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedPvc, setSelectedPvc] = useState(null);

  const fetchPVCList = async () => {
    setLoading(true);
    try {
      const response = await fetchWithAuth('/server/my-pvcs');
      if (!response.ok) {
        throw new Error('PVC 목록을 불러올 수 없습니다');
      }
      const data = await response.json();
      setPvcList(data.pvcs || []);
      
      // URL에 PVC ID가 있으면 해당 PVC 선택
      if (selectedPvcId) {
        const pvc = data.pvcs.find(p => p.id.toString() === selectedPvcId);
        if (pvc) {
          setSelectedPvc(pvc);
        }
      }
    } catch (error) {
      console.error("PVC 목록 불러오기 실패:", error);
      setPvcList([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPVCList();
  }, [selectedPvcId]);

  const handlePvcSelect = (pvc) => {
    setSelectedPvc(pvc);
    const newUrl = `${location.pathname}?pvc_id=${pvc.id}&path=${encodeURIComponent(pvc.path)}`;
    navigate(newUrl);
  };

  const handleBackToList = () => {
    setSelectedPvc(null);
    navigate(location.pathname);
  };

  // PVC가 선택되었으면 파일 브라우저 표시
  if (selectedPvc) {
    return (
      <FileBrowser 
        pvcId={selectedPvc.id}
        pvcName={selectedPvc.pvc_name}
        pvcPath={selectedPvc.path}
        onBack={handleBackToList}
      />
    );
  }

  // PVC 목록 표시
  return (
    <div className="p-6">
      <div className="mb-6">
        <Typography variant="h4" color="blue-gray" className="font-bold">
          스토리지 관리
        </Typography>
        <Typography variant="small" color="gray" className="mt-2">
          PVC를 선택하여 파일을 탐색하세요
        </Typography>
      </div>

      {loading ? (
        <div className="flex justify-center items-center h-32">
          <Spinner color="blue" />
        </div>
      ) : pvcList.length === 0 ? (
        <Card className="p-8 text-center">
          <Typography color="gray">
            사용 가능한 PVC가 없습니다
          </Typography>
        </Card>
      ) : (
        <div className="space-y-4">
          {pvcList.map((pvc) => (
            <PVCCard 
              key={pvc.id} 
              pvc={pvc} 
              onSelect={handlePvcSelect}
            />
          ))}
        </div>
      )}
    </div>
  );
}