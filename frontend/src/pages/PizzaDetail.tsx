import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import type { Pizza, Extra } from '../types';
import { apiService } from '../services/api';

const PizzaDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [pizza, setPizza] = useState<Pizza | null>(null);
  const [extras, setExtras] = useState<Extra[]>([]);
  const [selectedExtras, setSelectedExtras] = useState<Extra[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      if (!id) return;
      
      try {
        setLoading(true);
        const [pizzaResponse, extrasResponse] = await Promise.all([
          apiService.getPizza(parseInt(id)),
          apiService.getExtras()
        ]);
        
        setPizza(pizzaResponse.data);
        setExtras(extrasResponse.data);
      } catch (err) {
        setError('Failed to load pizza details');
        console.error('Error fetching pizza details:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [id]);

  const handleExtraToggle = (extra: Extra) => {
    setSelectedExtras(prev => {
      const isSelected = prev.some(e => e.id === extra.id);
      if (isSelected) {
        return prev.filter(e => e.id !== extra.id);
      } else {
        return [...prev, extra];
      }
    });
  };

  const calculateTotal = () => {
    if (!pizza) return 0;
    const extrasTotal = selectedExtras.reduce((sum, extra) => sum + extra.price, 0);
    return pizza.price + extrasTotal;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="text-black text-xl">Loading pizza details...</div>
      </div>
    );
  }

  if (error || !pizza) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="text-center">
          <div className="text-black text-xl mb-4">{error || 'Pizza not found'}</div>
          <Link to="/" className="bg-black text-white px-4 py-2 rounded hover:bg-gray-800 transition-colors">
            Back to Menu
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white">
      <div className="container mx-auto px-4 py-8">
        <Link to="/" className="inline-block mb-6 text-black hover:text-gray-600 transition-colors">
          ← Back to Menu
        </Link>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <div>
            {pizza.image_url && (
              <img 
                src={pizza.image_url} 
                alt={pizza.name}
                className="w-full h-96 object-cover rounded-lg border border-gray-300"
              />
            )}
          </div>

          <div>
            <h1 className="text-3xl font-bold text-black mb-4">{pizza.name}</h1>
            <p className="text-gray-600 text-lg mb-6">{pizza.description}</p>
            
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-black mb-2">Ingredients:</h3>
              <p className="text-gray-700">{pizza.ingredients.join(', ')}</p>
            </div>

            <div className="mb-6">
              <h3 className="text-lg font-semibold text-black mb-4">Add Extras:</h3>
              <div className="space-y-2">
                {extras.map((extra) => (
                  <label key={extra.id} className="flex items-center space-x-3 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={selectedExtras.some(e => e.id === extra.id)}
                      onChange={() => handleExtraToggle(extra)}
                      className="w-4 h-4"
                    />
                    <span className="text-gray-700">{extra.name}</span>
                    <span className="text-black font-medium">+${extra.price.toFixed(2)}</span>
                  </label>
                ))}
              </div>
            </div>

            <div className="border-t border-gray-300 pt-6">
              <div className="flex justify-between items-center mb-6">
                <span className="text-2xl font-bold text-black">Total: ${calculateTotal().toFixed(2)}</span>
              </div>
              
              <button className="w-full bg-black text-white py-3 px-6 rounded-lg hover:bg-gray-800 transition-colors font-medium">
                Add to Cart
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PizzaDetail;