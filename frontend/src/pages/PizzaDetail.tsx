import React, { useState, useEffect } from 'react';
import { useParams, useLocation, Link } from 'react-router-dom';
import type { Pizza, Extra, CustomerDetails, OrderRequest, OrderResponse } from '../types';
import { apiService } from '../services/api';
import PizzaImage from '../components/PizzaImage';
import PizzaExtras from '../components/PizzaExtras';
import Breadcrumb from '../components/Breadcrumb';
import ErrorCard from '../components/ErrorCard';
import CustomerDetailsModal from '../components/CustomerDetailsModal';
import OrderSuccessModal from '../components/OrderSuccessModal';
import OrderErrorModal from '../components/OrderErrorModal';

interface ExtraQuantity {
  extra: Extra;
  quantity: number;
}

const PizzaDetailSkeleton = () => (
  <div className="animate-pulse">
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
      <div className="bg-gray-200 h-96 rounded-xl"></div>
      <div className="space-y-6">
        <div className="h-8 bg-gray-200 rounded w-3/4"></div>
        <div className="h-4 bg-gray-200 rounded w-full"></div>
        <div className="h-4 bg-gray-200 rounded w-2/3"></div>
        <div className="space-y-2">
          <div className="h-4 bg-gray-200 rounded w-1/4"></div>
          <div className="h-4 bg-gray-200 rounded w-full"></div>
        </div>
        <div className="space-y-3">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="flex items-center space-x-3">
              <div className="w-4 h-4 bg-gray-200 rounded"></div>
              <div className="h-4 bg-gray-200 rounded flex-1"></div>
              <div className="h-4 bg-gray-200 rounded w-16"></div>
            </div>
          ))}
        </div>
        <div className="border-t pt-6">
          <div className="flex justify-between items-center mb-6">
            <div className="h-8 bg-gray-200 rounded w-24"></div>
          </div>
          <div className="h-12 bg-gray-200 rounded w-full"></div>
        </div>
      </div>
    </div>
  </div>
);

const PizzaDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const location = useLocation();
  const [pizza, setPizza] = useState<Pizza | null>(location.state?.pizza || null);
  const [extras, setExtras] = useState<Extra[]>([]);
  const [selectedExtras, setSelectedExtras] = useState<ExtraQuantity[]>([]);
  const [pizzaQuantity, setPizzaQuantity] = useState<number>(1);
  const [loading, setLoading] = useState(!pizza);
  const [error, setError] = useState<string | null>(null);
  
  // Order flow states
  const [showCustomerModal, setShowCustomerModal] = useState(false);
  const [showSuccessModal, setShowSuccessModal] = useState(false);
  const [showErrorModal, setShowErrorModal] = useState(false);
  const [orderData, setOrderData] = useState<OrderResponse | null>(null);
  const [orderError, setOrderError] = useState<string>('');
  const [isPlacingOrder, setIsPlacingOrder] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // If we don't have pizza data from route state, we need to get all pizzas and find the one we need
        let pizzaData = pizza;
        if (!pizzaData && id) {
          const pizzasResponse = await apiService.getPizzas();
          pizzaData = pizzasResponse.data.items.find((p: Pizza) => p.id === id) || null;
          setPizza(pizzaData);
        }
        
        // Always fetch extras
        const extrasResponse = await apiService.getExtras();
        setExtras(extrasResponse.data);
      } catch (err) {
        setError('Failed to load pizza details. Please try again later.');
        console.error('Error fetching pizza details:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [id, pizza]);

  const handleExtraQuantityChange = (extra: Extra, quantity: number) => {
    setSelectedExtras(prev => {
      const existingIndex = prev.findIndex(item => item.extra.id === extra.id);
      
      if (quantity === 0) {
        // Remove the extra if quantity is 0
        return prev.filter(item => item.extra.id !== extra.id);
      }
      
      if (existingIndex >= 0) {
        // Update existing extra quantity
        const updated = [...prev];
        updated[existingIndex] = { extra, quantity };
        return updated;
      } else {
        // Add new extra with quantity
        return [...prev, { extra, quantity }];
      }
    });
  };

  const handlePizzaQuantityChange = (newQuantity: number) => {
    // Ensure quantity doesn't go below 1
    const quantity = Math.max(1, newQuantity);
    setPizzaQuantity(quantity);
  };

  const calculatePizzaWithExtrasPrice = () => {
    if (!pizza) return 0;
    const extrasTotal = selectedExtras.reduce((sum, { extra, quantity }) => sum + (extra.price * quantity), 0);
    return pizza.base_price + extrasTotal;
  };

  const calculateTotal = () => {
    return calculatePizzaWithExtrasPrice() * pizzaQuantity;
  };

  const handleOrderNow = () => {
    setShowCustomerModal(true);
  };

  const handleCustomerSubmit = async (customerDetails: CustomerDetails) => {
    if (!pizza) return;

    setIsPlacingOrder(true);
    
    try {
      // Prepare order data
      const orderRequest: OrderRequest = {
        lines: [
          {
            pizza_id: pizza.id,
            quantity: pizzaQuantity,
            extras: selectedExtras.flatMap(({ extra, quantity }) =>
              Array(quantity).fill(extra.id)
            )
          }
        ],
        customer: {
          unique_identifier: customerDetails.email,
          fullname: customerDetails.fullname,
          full_address: customerDetails.address
        }
      };

      const response = await apiService.checkout(orderRequest);
      
      if (response.is_success) {
        setOrderData(response.data);
        setShowCustomerModal(false);
        setShowSuccessModal(true);
      } else {
        throw new Error(response.message || 'Order failed');
      }
    } catch (err) {
      console.error('Order failed:', err);
      setOrderError(err instanceof Error ? err.message : 'Failed to place order. Please try again.');
      setShowCustomerModal(false);
      setShowErrorModal(true);
    } finally {
      setIsPlacingOrder(false);
    }
  };

  const handleCloseModals = () => {
    setShowCustomerModal(false);
    setShowSuccessModal(false);
    setShowErrorModal(false);
    setOrderData(null);
    setOrderError('');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mb-6">
            <div className="h-6 bg-gray-200 rounded w-32 animate-pulse"></div>
          </div>
          <PizzaDetailSkeleton />
        </div>
      </div>
    );
  }

  if (error || !pizza) {
    return (
      <ErrorCard 
        title="Pizza not found"
        message={error || "The pizza you're looking for doesn't exist."}
        onRetry={() => window.location.href = '/'}
        retryText="Back to Menu"
      />
    );
  }

  const breadcrumbItems = [
    { label: 'Menu', href: '/' },
    { label: pizza.name }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <Breadcrumb items={breadcrumbItems} />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* Pizza Image */}
          <PizzaImage pizza={pizza} />

          {/* Pizza Details */}
          <div className="space-y-6">
            <div>
              <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">{pizza.name}</h1>
              <p className="text-lg text-gray-600 leading-relaxed">
                Delicious pizza made with fresh ingredients and authentic flavors, crafted to perfection for the ultimate taste experience.
              </p>
            </div>
            
            <div className="bg-gray-50 rounded-lg p-4">
              <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wide mb-3">
                Ingredients
              </h3>
              <p className="text-gray-700 leading-relaxed">{pizza.ingredients.join(', ')}</p>
            </div>

            {/* Extras Section */}
            {extras.length > 0 && (
              <PizzaExtras
                extras={extras}
                selectedExtras={selectedExtras}
                onExtraQuantityChange={handleExtraQuantityChange}
              />
            )}

            {/* Pizza Quantity Selector */}
            <div className="border-t border-gray-200 pt-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Quantity</h3>
              <div className="flex items-center space-x-4 mb-6">
                <span className="text-gray-700 font-medium">Number of pizzas:</span>
                <div className="flex items-center space-x-3">
                  <button
                    onClick={() => handlePizzaQuantityChange(pizzaQuantity - 1)}
                    disabled={pizzaQuantity === 1}
                    className={`w-10 h-10 rounded-full flex items-center justify-center text-lg font-medium transition-all duration-200 ${
                      pizzaQuantity === 1
                        ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                        : 'bg-gray-200 text-gray-700 hover:bg-gray-300 active:scale-95'
                    }`}
                  >
                    −
                  </button>
                  
                  <span className="w-12 text-center text-xl font-bold text-gray-900">
                    {pizzaQuantity}
                  </span>
                  
                  <button
                    onClick={() => handlePizzaQuantityChange(pizzaQuantity + 1)}
                    className="w-10 h-10 rounded-full bg-black text-white flex items-center justify-center text-lg font-medium hover:bg-gray-800 transition-all duration-200 active:scale-95"
                  >
                    +
                  </button>
                </div>
              </div>
            </div>

            {/* Price and Add to Cart */}
            <div className="border-t border-gray-200 pt-6">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
                <div>
                  <div className="text-3xl font-bold text-gray-900">
                    ${calculateTotal().toFixed(2)}
                  </div>
                  <div className="text-sm text-gray-500 space-y-1">
                    <div>
                      Price per pizza: ${calculatePizzaWithExtrasPrice().toFixed(2)}
                      <span className="text-gray-400"> (Base: ${pizza.base_price.toFixed(2)}
                      {selectedExtras.length > 0 && (
                        <span> + ${selectedExtras.reduce((sum, { extra, quantity }) => sum + (extra.price * quantity), 0).toFixed(2)} extras</span>
                      )})</span>
                    </div>
                    {pizzaQuantity > 1 && (
                      <div className="font-medium text-gray-700">
                        {pizzaQuantity} pizzas × ${calculatePizzaWithExtrasPrice().toFixed(2)} = ${calculateTotal().toFixed(2)}
                      </div>
                    )}
                  </div>
                </div>
              </div>
              
              <div className="space-y-3">
                <button
                  onClick={handleOrderNow}
                  className="w-full bg-black text-white py-4 px-6 rounded-lg hover:bg-gray-800 transition-all duration-200 font-medium text-lg hover:shadow-md transform hover:scale-[1.02]"
                >
                  Order {pizzaQuantity} {pizzaQuantity === 1 ? 'Pizza' : 'Pizzas'} Now
                </button>
                {/* <Link
                  to="/"
                  className="w-full border border-gray-300 text-gray-700 py-3 px-6 rounded-lg hover:bg-gray-50 transition-colors duration-200 font-medium text-center block"
                >
                  Add to Cart
                </Link> */}
                <Link
                  to="/"
                  className="w-full border border-gray-300 text-gray-700 py-3 px-6 rounded-lg hover:bg-gray-50 transition-colors duration-200 font-medium text-center block"
                >
                  Continue Shopping
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Modals */}
      <CustomerDetailsModal
        isOpen={showCustomerModal}
        onClose={handleCloseModals}
        onSubmit={handleCustomerSubmit}
        isLoading={isPlacingOrder}
      />

      <OrderSuccessModal
        isOpen={showSuccessModal}
        orderData={orderData}
        pizzas={pizza ? [pizza] : []}
        extras={extras}
        onClose={handleCloseModals}
      />

      <OrderErrorModal
        isOpen={showErrorModal}
        onClose={handleCloseModals}
        errorMessage={orderError}
      />
    </div>
  );
};

export default PizzaDetail;