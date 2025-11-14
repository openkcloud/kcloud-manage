import React from 'react';
import GPUComponent from './GPUComponent';

const GPUNode = ({ gpuId, data }) => {
  return (
    // flex 컨테이너로 변경, 아이템 사이 간격을 위해 space-x-2 적용
    <div className="flex shadow-none">
      {data.map((item, index) => (
        <GPUComponent
          key={index}
          compute={item.compute}
          gpuId={gpuId}
          migId={item.migId}
          flavor={item.flavor}
          user={item.user}
          status={item.status}
        />
      ))}
    </div>
  );
};

export default GPUNode;