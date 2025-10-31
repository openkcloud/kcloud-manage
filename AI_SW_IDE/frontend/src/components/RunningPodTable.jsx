import React, { useState, useEffect } from 'react';

import { DocumentIcon, PresentationChartBarIcon, ChartBarIcon } from "@heroicons/react/24/solid";
import { fetchWithAuth } from "@/utils/auth";
import { ArrowDownTrayIcon } from "@heroicons/react/24/outline";
import { MagnifyingGlassIcon } from "@heroicons/react/24/outline";
import {
  Card,
  Input,
  CardHeader,
  IconButton,
  Typography,
} from "@material-tailwind/react";
import LoadingSpinner from './Loading';
 
const TABLE_HEAD = [
  {
    head: "TAG",
  },
  {
    head: "User Name",
  },
  {
    head: "GPU",
  },
  {
    head: "CPU/Mem",
  },
  {
    head: "Create At",
  },
  {
    head: "Status",
  },
  {
    head: "Node[GPU ID,MIG ID]",
  },
  {
    head: "",
  },
];

export function RunningPodTable() {
  const [tableRows, setTableRows] = useState([]);
  const [loading, setLoading] = useState(true);

  // 데이터를 불러오는 함수
  const fetchTableData = async () => {
    try {
      // const response = await fetch("/api/gpu/table_info");
      const response = await fetchWithAuth("/server/list");
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const result = await response.json();
      // 예: { data: [...] } 구조라면 setTableRows(result.data)
      setTableRows(result);
    } catch (error) {
      console.error("Error fetching table data:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // 마운트 시 즉시 호출
    fetchTableData();

    // 15초 간격으로 폴링
    const interval = setInterval(() => {
      fetchTableData();
    }, 60000);

    // 언마운트 시 interval 정리
    return () => clearInterval(interval);
  }, []);
  
  if (loading) {
    return <LoadingSpinner />;
  }

  const formatKoreanDateTime = (isoString) => {
    const date = new Date(isoString);
    return new Intl.DateTimeFormat("ko-KR", {
      year: "numeric",
      month: "numeric",
      day: "numeric",
      hour: "numeric",
      minute: "numeric",
      second: "numeric",
      hour12: true,
    }).format(date);
  };

  const rowBaseClass = "p-4 border-b border-gray-300";
  const lastRowClass = "p-4";

  return (
    <Card className="max p-6 shadow-l shadow-blue-gray-900/5 border border-gray-300 rounded-xl bg-white">
      {/* text-center 로 변경 */}
      <h6 className="mb-2 text-slate-800 text-xl font-semibold">
        Running Servers
      </h6>
      <table className="w-full min-w-max table-auto text-center">
        <thead>
          <tr>
            {TABLE_HEAD.map(({ head }) => (
              <th key={head} className="border-b border-gray-300 p-4">
                <div className="flex items-center justify-center gap-1">
                  <Typography color="blue-gray" variant="small" className="!font-bold">
                    {head === "Node[GPU ID,MIG ID]" ? (
                      <>
                        Node <br /> [GPU ID,MIG ID]
                      </>
                    ) : (
                      head
                    )}
                  </Typography>
                </div>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {tableRows.map((row, index) => {
            const isLast = index === tableRows.length - 1;
            const classes = isLast ? "p-4" : "p-4 border-b border-gray-300";
            return (
              <tr key={row.userName + index}>
                <td className={classes}>
                  <div className="flex justify-center">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium border ${
                      row.tags === 'JUPYTER' ? 'text-orange-400 border-orange-400' :
                      row.tags === 'LEGEND' ? 'text-blue-700 border-blue-700' :
                      row.tags === 'DEV' ? 'text-gray-600 border-gray-600' :
                      'text-gray-800 border-gray-800'
                    }`}>
                      {row.tags || 'N/A'}
                    </span>
                  </div>
                </td>
                <td className={classes}>
                  <Typography variant="small" color="blue-gray" className="font-bold">
                    {row.userName}
                  </Typography>
                </td>
                <td className={classes}>
                  <Typography variant="small" className="font-normal text-gray-600">
                    {row.node.length === 1 ? row.gpu : `${row.gpu}*${row.node.length}`}
                  </Typography>
                </td>
                <td className={classes}>
                  <Typography variant="small" className="font-normal text-gray-600">
                    {row.cpuMem}
                  </Typography>
                </td>
                <td className={classes}>
                  <Typography variant="small" className="font-normal text-gray-600">
                    {formatKoreanDateTime(row.createdAt)}
                  </Typography>
                </td>
                <td className={classes}>
                  <Typography variant="small" className="font-normal text-gray-600">
                    {row.status}
                  </Typography>
                </td>
                <td className={classes}>
                  <Typography variant="small" className="font-normal text-gray-600">
                    {Array.isArray(row.node) ? (
                      row.node.map((n, idx) => (
                        <React.Fragment key={idx}>
                          {n}
                          {idx !== row.node.length - 1 && <br />}
                        </React.Fragment>
                      ))
                    ) : (
                      row.node
                    )}
                  </Typography>
                </td>
                <td className={classes}>
                  <div className="flex items-center justify-center gap-2">
                    {/* 가운데 정렬을 위해 justify-center 추가 */}
                    <IconButton variant="text" size="sm">
                      <ChartBarIcon className="h-4 w-4 text-gray-900" />
                    </IconButton>
                  </div>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </Card>
  );
}

export default RunningPodTable;