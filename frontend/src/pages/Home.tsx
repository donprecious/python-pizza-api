import React, { useState, useEffect } from 'react';
import type { Pizza } from '../types';
import { apiService } from '../services/api';
import PizzaCard from '../components/PizzaCard';
import ErrorCard from '../components/ErrorCard';
import HeroSection from '../components/HeroSection';
import LoadingSkeleton from '../components/LoadingSkeleton';

const Home: React.FC = () => {
  const [pizzas, setPizzas] = useState<Pizza[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchPizzas = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiService.getPizzas();
      setPizzas(response.data.items);
    } catch (err) {
      setError('Failed to load pizzas. Please try again later.');
      console.error('Error fetching pizzas:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPizzas();
  }, []);

  if (error) {
    return (
      <ErrorCard 
        message={error} 
        onRetry={fetchPizzas}
      />
    );
  }

  return (
    <div className="min-h-screen">
      <HeroSection 
        title="Pizza Menu"
        subtitle="Choose from our delicious selection of handcrafted pizzas made with fresh, premium ingredients"
      />

      {/* Pizza Grid */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-2">
            {[...Array(6)].map((_, index) => (
              <div key={index} className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
                <LoadingSkeleton />
              </div>
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-2">
            {pizzas.map((pizza) => (
              <PizzaCard key={pizza.id} pizza={pizza} />
            ))}
          </div>
        )}

        {!loading && pizzas.length === 0 && (
          <div className="text-center py-16">
            <div className="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
              <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No pizzas available</h3>
            <p className="text-gray-600">Check back later for our delicious pizza selection.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Home;