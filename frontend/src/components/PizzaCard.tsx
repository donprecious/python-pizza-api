import React from 'react';
import { Link } from 'react-router-dom';
import type { Pizza } from '../types';

interface PizzaCardProps {
  pizza: Pizza;
}

const PizzaCard: React.FC<PizzaCardProps> = ({ pizza }) => {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-lg hover:-translate-y-1 transition-all duration-300 group">
      <div className="relative overflow-hidden">
        <img 
          src={pizza.image_url || 'https://septemberfarmcheese.b-cdn.net/wp-content/uploads/Blogs/Homemade-Pizza/homemade-pizza-monterey-jack-cheese.jpg'} 
          alt={pizza.name}
          className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
          onError={(e) => {
            const target = e.target as HTMLImageElement;
            target.src = 'https://septemberfarmcheese.b-cdn.net/wp-content/uploads/Blogs/Homemade-Pizza/homemade-pizza-monterey-jack-cheese.jpg';
          }}
        />
        {/* <div className="absolute inset-0 bg-black bg-opacity-10 group-hover:bg-opacity-10 transition-all duration-300"></div> */}
      </div>
      
      <div className="p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-2 group-hover:text-black transition-colors">
          {pizza.name}
        </h2>
        <p className="text-gray-600 mb-4 text-sm leading-relaxed">
          Delicious pizza with fresh ingredients and authentic flavors
        </p>
        
        <div className="mb-6">
          <p className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-2">
            Ingredients
          </p>
          <p className="text-sm text-gray-700 leading-relaxed">
            {pizza.ingredients.join(', ')}
          </p>
        </div>
        
        <div className="flex justify-between items-center">
          <div className="flex flex-col">
            <span className="text-2xl font-bold text-gray-900">
              ${pizza.base_price.toFixed(2)}
            </span>
            <span className="text-xs text-gray-500">Starting price</span>
          </div>
          <Link 
            to={`/pizza/${pizza.id}`}
            state={{ pizza }}
            className="bg-black text-white px-6 py-2.5 rounded-lg hover:bg-gray-800 transition-all duration-200 font-medium text-sm hover:shadow-md transform hover:scale-105"
          >
            View Details
          </Link>
        </div>
      </div>
    </div>
  );
};

export default PizzaCard;