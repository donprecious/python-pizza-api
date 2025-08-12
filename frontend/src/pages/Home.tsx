import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import type { Pizza } from '../types';
import { apiService } from '../services/api';

const Home: React.FC = () => {
  const [pizzas, setPizzas] = useState<Pizza[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPizzas = async () => {
      try {
        setLoading(true);
        const response = await apiService.getPizzas();
        setPizzas(response.data);
      } catch (err) {
        setError('Failed to load pizzas');
        console.error('Error fetching pizzas:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchPizzas();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="text-black text-xl">Loading pizzas...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="text-black text-xl">{error}</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-black mb-4">Pizza Menu</h1>
          <p className="text-gray-600 text-lg">Choose from our delicious selection of pizzas</p>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {pizzas.map((pizza) => (
            <div key={pizza.id} className="border border-gray-300 rounded-lg overflow-hidden hover:shadow-lg transition-shadow">
              {pizza.image_url && (
                <img 
                  src={pizza.image_url} 
                  alt={pizza.name}
                  className="w-full h-48 object-cover"
                />
              )}
              <div className="p-6">
                <h2 className="text-xl font-semibold text-black mb-2">{pizza.name}</h2>
                <p className="text-gray-600 mb-4">{pizza.description}</p>
                <div className="mb-4">
                  <p className="text-sm text-gray-500 mb-2">Ingredients:</p>
                  <p className="text-sm text-gray-700">{pizza.ingredients.join(', ')}</p>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-2xl font-bold text-black">${pizza.price.toFixed(2)}</span>
                  <Link 
                    to={`/pizza/${pizza.id}`}
                    className="bg-black text-white px-4 py-2 rounded hover:bg-gray-800 transition-colors"
                  >
                    View Details
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>

        {pizzas.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-600 text-lg">No pizzas available at the moment.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Home;