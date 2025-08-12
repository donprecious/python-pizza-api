import React from 'react';
import { Link } from 'react-router-dom';
import type { OrderResponse, Pizza, Extra } from '../types';

interface OrderSuccessModalProps {
  isOpen: boolean;
  orderData: OrderResponse | null;
  pizzas: Pizza[];
  extras: Extra[];
  onClose: () => void;
}

const OrderSuccessModal: React.FC<OrderSuccessModalProps> = ({
  isOpen,
  orderData,
  pizzas,
  extras,
  onClose
}) => {
  if (!isOpen || !orderData) return null;

  const getPizzaName = (pizzaId: string): string => {
    const pizza = pizzas.find(p => p.id === pizzaId);
    return pizza ? pizza.name : 'Unknown Pizza';
  };

  const getExtraName = (extraId: string): string => {
    const extra = extras.find(e => e.id === extraId);
    return extra ? extra.name : 'Unknown Extra';
  };

  const getExtraQuantities = (extraIds: string[]): { [key: string]: number } => {
    const quantities: { [key: string]: number } = {};
    extraIds.forEach(id => {
      quantities[id] = (quantities[id] || 0) + 1;
    });
    return quantities;
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-xl max-w-lg w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          {/* Success Header */}
          <div className="text-center mb-6">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Order Placed Successfully!</h2>
            <p className="text-gray-600">Thank you for your order. We'll start preparing your delicious pizza right away.</p>
          </div>

          {/* Order Details */}
          <div className="bg-gray-50 rounded-lg p-4 mb-6">
            <div className="flex justify-between items-center mb-3">
              <h3 className="font-semibold text-gray-900">Order Details</h3>
              <span className="text-sm text-gray-500">#{orderData.id.slice(-8)}</span>
            </div>
            
            <div className="space-y-3">
              {orderData.lines.map((line) => {
                const extraQuantities = getExtraQuantities(line.extras);
                
                return (
                  <div key={line.id} className="border-b border-gray-200 pb-3 last:border-b-0 last:pb-0">
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <h4 className="font-medium text-gray-900">
                          {getPizzaName(line.pizza_id)}
                          {line.quantity > 1 && (
                            <span className="text-sm text-gray-600 ml-2">x {line.quantity}</span>
                          )}
                        </h4>
                        
                        {line.extras.length > 0 && (
                          <div className="mt-1">
                            <p className="text-sm text-gray-600">Extras:</p>
                            <div className="text-sm text-gray-700 ml-2">
                              {Object.entries(extraQuantities).map(([extraId, quantity]) => (
                                <div key={extraId}>
                                  {getExtraName(extraId)}
                                  {quantity > 1 && <span className="text-gray-500"> x {quantity}</span>}
                                </div>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                      
                      <div className="text-right ml-4">
                        <div className="font-medium text-gray-900">
                          ${line.line_total.toFixed(2)}
                        </div>
                        <div className="text-xs text-gray-500">
                          ${line.unit_base_price.toFixed(2)} base
                          {line.unit_extras_total > 0 && (
                            <span> + ${line.unit_extras_total.toFixed(2)} extras</span>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Order Summary */}
          <div className="bg-black text-white rounded-lg p-4 mb-6">
            <div className="space-y-2">
              <div className="flex justify-between">
                <span>Subtotal:</span>
                <span>${orderData.subtotal.toFixed(2)}</span>
              </div>
              {orderData.extras_total > 0 && (
                <div className="flex justify-between">
                  <span>Extras Total:</span>
                  <span>${orderData.extras_total.toFixed(2)}</span>
                </div>
              )}
              <div className="border-t border-gray-600 pt-2 flex justify-between font-bold text-lg">
                <span>Grand Total:</span>
                <span>${orderData.grand_total.toFixed(2)}</span>
              </div>
            </div>
          </div>

          {/* Order Status */}
          <div className="text-center mb-6">
            <div className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
              <div className="w-2 h-2 bg-blue-600 rounded-full mr-2"></div>
              Order {orderData.status}
            </div>
            <p className="text-sm text-gray-600 mt-2">
              We'll send you updates about your order status.
            </p>
          </div>

          {/* Action Buttons */}
          <div className="space-y-3">
            <Link
              to="/"
              onClick={onClose}
              className="w-full bg-black text-white py-3 px-4 rounded-lg hover:bg-gray-800 transition-colors font-medium text-center block"
            >
              Return to Home
            </Link>
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

export default OrderSuccessModal;