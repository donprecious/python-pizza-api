import React from 'react';

interface OrderErrorModalProps {
  isOpen: boolean;
  onClose: () => void;
  errorMessage?: string;
}

const OrderErrorModal: React.FC<OrderErrorModalProps> = ({
  isOpen,
  onClose,
  errorMessage = "We're sorry, but there was an issue processing your order. Please try again or contact our support team if the problem persists."
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-xl max-w-md w-full">
        <div className="p-6">
          {/* Error Header */}
          <div className="text-center mb-6">
            <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Order Failed</h2>
            <p className="text-gray-600 leading-relaxed">
              {errorMessage}
            </p>
          </div>

          {/* Helpful Tips */}
          <div className="bg-gray-50 rounded-lg p-4 mb-6">
            <h3 className="font-medium text-gray-900 mb-2">What you can do:</h3>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>• Check your internet connection</li>
              <li>• Verify your delivery address is correct</li>
              <li>• Try placing the order again</li>
              <li>• Contact our support team if the issue continues</li>
            </ul>
          </div>

          {/* Action Buttons */}
          <div className="space-y-3">
            <button
              onClick={onClose}
              className="w-full bg-black text-white py-3 px-4 rounded-lg hover:bg-gray-800 transition-colors font-medium"
            >
              Try Again
            </button>
            <button
              onClick={onClose}
              className="w-full border border-gray-300 text-gray-700 py-3 px-4 rounded-lg hover:bg-gray-50 transition-colors font-medium"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OrderErrorModal;