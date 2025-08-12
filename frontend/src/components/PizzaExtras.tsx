import React from 'react';
import type { Extra } from '../types';

interface ExtraQuantity {
  extra: Extra;
  quantity: number;
}

interface PizzaExtrasProps {
  extras: Extra[];
  selectedExtras: ExtraQuantity[];
  onExtraQuantityChange: (extra: Extra, quantity: number) => void;
}

const PizzaExtras: React.FC<PizzaExtrasProps> = ({ 
  extras, 
  selectedExtras, 
  onExtraQuantityChange 
}) => {
  const getExtraQuantity = (extraId: string): number => {
    const found = selectedExtras.find(item => item.extra.id === extraId);
    return found ? found.quantity : 0;
  };

  const handleQuantityChange = (extra: Extra, newQuantity: number) => {
    // Ensure quantity doesn't go below 0
    const quantity = Math.max(0, newQuantity);
    onExtraQuantityChange(extra, quantity);
  };

  return (
    <div>
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Customize Your Pizza</h3>
      <div className="space-y-3">
        {extras.map((extra) => {
          const quantity = getExtraQuantity(extra.id);
          const isSelected = quantity > 0;
          
          return (
            <div 
              key={extra.id} 
              className={`p-4 border rounded-lg transition-all duration-200 ${
                isSelected 
                  ? 'border-black bg-gray-50 shadow-sm' 
                  : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3">
                    <span className={`font-medium ${isSelected ? 'text-gray-900' : 'text-gray-700'}`}>
                      {extra.name}
                    </span>
                    {isSelected && (
                      <span className="text-sm font-medium text-black bg-white px-2 py-1 rounded-full border">
                        x {quantity}
                      </span>
                    )}
                  </div>
                  <div className="mt-1 text-sm text-gray-600">
                    ${extra.price.toFixed(2)} each
                    {isSelected && quantity > 1 && (
                      <span className="ml-2 font-medium text-gray-900">
                        • Total: ${(extra.price * quantity).toFixed(2)}
                      </span>
                    )}
                  </div>
                </div>
                
                <div className="flex items-center space-x-3">
                  {/* Quantity Controls */}
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => handleQuantityChange(extra, quantity - 1)}
                      disabled={quantity === 0}
                      className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium transition-all duration-200 ${
                        quantity === 0
                          ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                          : 'bg-gray-200 text-gray-700 hover:bg-gray-300 active:scale-95'
                      }`}
                    >
                      −
                    </button>
                    
                    <span className="w-8 text-center font-medium text-gray-900">
                      {quantity}
                    </span>
                    
                    <button
                      onClick={() => handleQuantityChange(extra, quantity + 1)}
                      className="w-8 h-8 rounded-full bg-black text-white flex items-center justify-center text-sm font-medium hover:bg-gray-800 transition-all duration-200 active:scale-95"
                    >
                      +
                    </button>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
      
      {/* Selected Extras Summary */}
      {selectedExtras.length > 0 && (
        <div className="mt-6 p-4 bg-black text-white rounded-lg">
          <h4 className="font-medium mb-3">Selected Extras:</h4>
          <div className="space-y-2">
            {selectedExtras.map(({ extra, quantity }) => (
              <div key={extra.id} className="flex justify-between items-center text-sm">
                <span>{extra.name} x {quantity}</span>
                <span>${(extra.price * quantity).toFixed(2)}</span>
              </div>
            ))}
          </div>
          <div className="border-t border-gray-600 mt-3 pt-3 flex justify-between items-center font-medium">
            <span>Extras Total:</span>
            <span>
              ${selectedExtras.reduce((sum, { extra, quantity }) => sum + (extra.price * quantity), 0).toFixed(2)}
            </span>
          </div>
        </div>
      )}
    </div>
  );
};

export default PizzaExtras;