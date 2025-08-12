import React from 'react';
import type { Pizza } from '../types';

interface PizzaImageProps {
  pizza: Pizza;
}

const PizzaImage: React.FC<PizzaImageProps> = ({ pizza }) => {
  return (
    <div className="relative">
      <div className="aspect-square rounded-xl overflow-hidden bg-white shadow-sm border border-gray-100">
        <img 
          src={pizza.image_url || 'https://septemberfarmcheese.b-cdn.net/wp-content/uploads/Blogs/Homemade-Pizza/homemade-pizza-monterey-jack-cheese.jpg'} 
          alt={pizza.name}
          className="w-full h-full object-cover"
          onError={(e) => {
            const target = e.target as HTMLImageElement;
            target.src = 'https://septemberfarmcheese.b-cdn.net/wp-content/uploads/Blogs/Homemade-Pizza/homemade-pizza-monterey-jack-cheese.jpg';
          }}
        />
      </div>
    </div>
  );
};

export default PizzaImage;