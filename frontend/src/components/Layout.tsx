import React from 'react';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-white">
      <nav className="bg-white border-b border-gray-200">
        <div className="container mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-black">Pizza Shop</h1>
            <div className="flex space-x-4">
              <a href="/" className="text-black hover:text-gray-600 transition-colors">
                Menu
              </a>
              <a href="#" className="text-black hover:text-gray-600 transition-colors">
                Cart
              </a>
            </div>
          </div>
        </div>
      </nav>
      <main>{children}</main>
    </div>
  );
};

export default Layout;