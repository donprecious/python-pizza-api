import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import type { OrderResponse, Pizza, Extra } from '../types';
import { apiService } from '../services/api';
import Breadcrumb from '../components/Breadcrumb';
import ErrorCard from '../components/ErrorCard';

const OrdersSkeleton = () => (
  <div className="space-y-6">
    {[...Array(3)].map((_, i) => (
      <div key={i} className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 animate-pulse">
        <div className="flex justify-between items-start mb-4">
          <div className="h-6 bg-gray-200 rounded w-32"></div>
          <div className="h-5 bg-gray-200 rounded w-20"></div>
        </div>
        <div className="space-y-3">
          <div className="h-4 bg-gray-200 rounded w-3/4"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
        </div>
        <div className="border-t border-gray-200 mt-4 pt-4">
          <div className="h-6 bg-gray-200 rounded w-24"></div>
        </div>
      </div>
    ))}
  </div>
);

const Orders: React.FC = () => {
  const [orders, setOrders] = useState<OrderResponse[]>([]);
  const [pizzas, setPizzas] = useState<Pizza[]>([]);
  const [extras, setExtras] = useState<Extra[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalOrders, setTotalOrders] = useState(0);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchInput, setSearchInput] = useState('');

  // For demo purposes, we'll use a default email. In a real app, this would come from authentication
  const defaultEmail = '';

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);

        // Use search query as uniqueIdentifier if provided, otherwise use default email
        const uniqueIdentifier = searchQuery.trim() || defaultEmail;
        
        // Fetch orders, pizzas, and extras in parallel
        const [ordersResponse, pizzasResponse, extrasResponse] = await Promise.all([
          apiService.getOrders(uniqueIdentifier, currentPage, 10),
          apiService.getPizzas(),
          apiService.getExtras()
        ]);

        if (ordersResponse.is_success) {
          setOrders(ordersResponse.data);
          const meta = ordersResponse.meta as { total?: number };
          const total = meta?.total || 0;
          setTotalOrders(total);
          setTotalPages(Math.ceil(total / 10) || 1);
        }

        if (pizzasResponse.is_success) {
          setPizzas(pizzasResponse.data.items);
        }

        if (extrasResponse.is_success) {
          setExtras(extrasResponse.data);
        }
      } catch (err) {
        setError('Failed to load orders. Please try again later.');
        console.error('Error fetching orders:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [currentPage, searchQuery]);

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

  const formatDate = (dateString: string): string => {
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch {
      return 'Unknown date';
    }
  };

  const getStatusColor = (status: string): string => {
    switch (status.toLowerCase()) {
      case 'created':
        return 'bg-blue-100 text-blue-800';
      case 'confirmed':
        return 'bg-green-100 text-green-800';
      case 'preparing':
        return 'bg-yellow-100 text-yellow-800';
      case 'ready':
        return 'bg-purple-100 text-purple-800';
      case 'delivered':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setSearchQuery(searchInput);
    setCurrentPage(1); // Reset to first page when searching
  };

  const clearSearch = () => {
    setSearchInput('');
    setSearchQuery('');
    setCurrentPage(1);
  };

  const renderPaginationButtons = () => {
    const buttons = [];
    const maxVisiblePages = 5;
    
    let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
    const endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);
    
    if (endPage - startPage + 1 < maxVisiblePages) {
      startPage = Math.max(1, endPage - maxVisiblePages + 1);
    }

    // Previous button
    buttons.push(
      <button
        key="prev"
        onClick={() => handlePageChange(currentPage - 1)}
        disabled={currentPage === 1}
        className="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Previous
      </button>
    );

    // First page and ellipsis
    if (startPage > 1) {
      buttons.push(
        <button
          key={1}
          onClick={() => handlePageChange(1)}
          className="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
        >
          1
        </button>
      );
      if (startPage > 2) {
        buttons.push(
          <span key="ellipsis1" className="px-3 py-2 text-sm text-gray-500">
            ...
          </span>
        );
      }
    }

    // Page numbers
    for (let i = startPage; i <= endPage; i++) {
      buttons.push(
        <button
          key={i}
          onClick={() => handlePageChange(i)}
          className={`px-3 py-2 text-sm font-medium rounded-md ${
            currentPage === i
              ? 'bg-black text-white'
              : 'text-gray-500 bg-white border border-gray-300 hover:bg-gray-50'
          }`}
        >
          {i}
        </button>
      );
    }

    // Last page and ellipsis
    if (endPage < totalPages) {
      if (endPage < totalPages - 1) {
        buttons.push(
          <span key="ellipsis2" className="px-3 py-2 text-sm text-gray-500">
            ...
          </span>
        );
      }
      buttons.push(
        <button
          key={totalPages}
          onClick={() => handlePageChange(totalPages)}
          className="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
        >
          {totalPages}
        </button>
      );
    }

    // Next button
    buttons.push(
      <button
        key="next"
        onClick={() => handlePageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        className="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Next
      </button>
    );

    return buttons;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mb-6">
            <div className="h-6 bg-gray-200 rounded w-32 animate-pulse"></div>
          </div>
          <div className="mb-8">
            <div className="h-8 bg-gray-200 rounded w-48 animate-pulse mb-2"></div>
            <div className="h-4 bg-gray-200 rounded w-64 animate-pulse"></div>
          </div>
          <OrdersSkeleton />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <ErrorCard 
        title="Failed to load orders"
        message={error}
        onRetry={() => window.location.reload()}
        retryText="Try Again"
      />
    );
  }

  const breadcrumbItems = [
    { label: 'Menu', href: '/' },
    { label: 'My Orders' }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <Breadcrumb items={breadcrumbItems} />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-2">My Orders</h1>
          <p className="text-lg text-gray-600">
            Track your pizza orders and view order history
          </p>
        </div>

        {/* Search and Filters */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-8">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
            <div className="flex-1">
              <form onSubmit={handleSearch} className="flex gap-4">
                <div className="flex-1">
                  <label htmlFor="search" className="sr-only">
                    Search orders by email or order ID
                  </label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                      </svg>
                    </div>
                    <input
                      type="text"
                      id="search"
                      value={searchInput}
                      onChange={(e) => setSearchInput(e.target.value)}
                      placeholder="Search by email ..."
                      className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-black focus:border-black"
                    />
                  </div>
                </div>
                <button
                  type="submit"
                  className="px-6 py-2 bg-black text-white rounded-md hover:bg-gray-800 transition-colors font-medium"
                >
                  Search
                </button>
                {searchQuery && (
                  <button
                    type="button"
                    onClick={clearSearch}
                    className="px-4 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
                  >
                    Clear
                  </button>
                )}
              </form>
            </div>
            
            {/* Results summary */}
            <div className="text-sm text-gray-600">
              {searchQuery ? (
                <span>
                  Found {totalOrders} result{totalOrders !== 1 ? 's' : ''} for "{searchQuery}"
                </span>
              ) : (
                <span>
                  Showing {totalOrders} order{totalOrders !== 1 ? 's' : ''}
                </span>
              )}
            </div>
          </div>
        </div>

        {/* Orders List */}
        {orders.length === 0 ? (
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-12 text-center">
            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              {searchQuery ? 'No orders found' : 'No orders yet'}
            </h3>
            <p className="text-gray-600 mb-6">
              {searchQuery 
                ? 'Try adjusting your search terms or clear the search to see all orders.'
                : "You haven't placed any orders yet. Start by ordering your favorite pizza!"
              }
            </p>
            {!searchQuery && (
              <Link 
                to="/"
                className="inline-flex items-center px-6 py-3 bg-black text-white rounded-lg hover:bg-gray-800 transition-colors font-medium"
              >
                Order Now
              </Link>
            )}
          </div>
        ) : (
          <div className="space-y-6">
            {orders.map((order) => (
              <div key={order.id} className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow">
                {/* Order Header */}
                <div className="p-6 border-b border-gray-100">
                  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">
                        Order #{order.id.slice(-8)}
                      </h3>
                      <p className="text-sm text-gray-600">
                        {order.id}{/* Using order ID as date placeholder */}
                      </p>
                    </div>
                    <div className="flex items-center gap-4">
                      <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(order.status)}`}>
                        <div className="w-2 h-2 bg-current rounded-full mr-2"></div>
                        {order.status.charAt(0).toUpperCase() + order.status.slice(1)}
                      </span>
                      <div className="text-right">
                        <div className="text-lg font-bold text-gray-900">
                          ${order.grand_total.toFixed(2)}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Order Items */}
                <div className="p-6">
                  <div className="space-y-4">
                    {order.lines.map((line) => {
                      const extraQuantities = getExtraQuantities(line.extras);
                      
                      return (
                        <div key={line.id} className="flex items-start justify-between">
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
                                    <span key={extraId} className="inline-block mr-3">
                                      {getExtraName(extraId)}
                                      {quantity > 1 && <span className="text-gray-500"> x {quantity}</span>}
                                    </span>
                                  ))}
                                </div>
                              </div>
                            )}
                            
                            <div className="text-xs text-gray-500 mt-1">
                              ${line.unit_base_price.toFixed(2)} base
                              {line.unit_extras_total > 0 && (
                                <span> + ${line.unit_extras_total.toFixed(2)} extras</span>
                              )}
                            </div>
                          </div>
                          
                          <div className="text-right ml-4">
                            <div className="font-medium text-gray-900">
                              ${line.line_total.toFixed(2)}
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>

                  {/* Order Summary */}
                  <div className="border-t border-gray-100 mt-6 pt-4">
                    <div className="flex justify-between text-sm text-gray-600 mb-1">
                      <span>Subtotal:</span>
                      <span>${order.subtotal.toFixed(2)}</span>
                    </div>
                    {order.extras_total > 0 && (
                      <div className="flex justify-between text-sm text-gray-600 mb-1">
                        <span>Extras:</span>
                        <span>${order.extras_total.toFixed(2)}</span>
                      </div>
                    )}
                    <div className="flex justify-between font-semibold text-gray-900 text-lg">
                      <span>Total:</span>
                      <span>${order.grand_total.toFixed(2)}</span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Enhanced Pagination */}
        {totalPages > 1 && (
          <div className="mt-8">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div className="text-sm text-gray-700">
                Showing page {currentPage} of {totalPages} ({totalOrders} total orders)
              </div>
              <div className="flex items-center space-x-2">
                {renderPaginationButtons()}
              </div>
            </div>
          </div>
        )}

        {/* Back to Menu */}
        <div className="mt-8 text-center">
          <Link 
            to="/"
            className="inline-flex items-center px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors font-medium"
          >
            ← Back to Menu
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Orders;