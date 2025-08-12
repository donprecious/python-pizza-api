import React from 'react';

const LoadingSkeleton: React.FC = () => (
  <div className="animate-pulse">
    <div className="bg-gray-200 h-48 w-full rounded-t-xl"></div>
    <div className="p-6 space-y-4">
      <div className="h-6 bg-gray-200 rounded w-3/4"></div>
      <div className="h-4 bg-gray-200 rounded w-full"></div>
      <div className="h-4 bg-gray-200 rounded w-2/3"></div>
      <div className="flex justify-between items-center">
        <div className="h-8 bg-gray-200 rounded w-20"></div>
        <div className="h-10 bg-gray-200 rounded w-24"></div>
      </div>
    </div>
  </div>
);

export default LoadingSkeleton;