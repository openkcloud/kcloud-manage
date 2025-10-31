import React, { useEffect, useState } from "react";
import { MyServerCard } from '@/components/MyServerCard';
import { fetchWithAuth } from "@/utils/auth";


const MyServer = () => {
  const [servers, setServers] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetchWithAuth("/server/my-server");
        if (!res || !res.ok) {
          throw new Error("서버에서 응답을 받을 수 없습니다.");
        }
        const data = await res.json();
        setServers(data);
      } catch (error) {
        console.error("서버 목록 불러오기 실패:", error);
      }
    };

    fetchData();
  }, []);

  const handleDelete = (id) => {
    setServers((prev) => prev.filter((server) => server.id !== id));
  };

  return (
    <div className="space-y-4">
      {servers.map((server, index) => (
        <MyServerCard key={server.id} server={server} index={index} onDelete={handleDelete} />
      ))}

      {/* 🔽 추가로 "빈 카드"도 렌더링 */}
      <MyServerCard />
    </div>
  );
}

export default MyServer;