import React from 'react';

interface ErrorCardProps {
  title?: string;
  message: string;
  onRetry?: () => void;
  retryText?: string;
}

const ErrorCard: React.FC<ErrorCardProps> = ({ 
  title = "Oops! Something went wrong", 
  message, 
  onRetry, 
  retryText = "Try Again" 
}) => {
  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <div className="text-center max-w-md">
        <div className="w-16 h-16 mx-auto mb-4 bg-red-100 rounded-full flex items-center justify-center">
          <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h2 className="text-xl font-semibold text-gray-900 mb-2">{title}</h2>
        <p className="text-gray-600 mb-6">{message}</p>
        {onRetry && (
          <button 
            onClick={onRetry}
            className="bg-black text-white px-6 py-2 rounded-lg hover:bg-gray-800 transition-colors duration-200"
          >
            {retryText}
          </button>
        )}
      </div>
    </div>
  );
};

export default ErrorCard;