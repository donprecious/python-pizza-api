import React from 'react';
import { Link, useLocation } from 'react-router-dom';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const location = useLocation();

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b border-gray-100 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link to="/" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-black rounded-full flex items-center justify-center">
                <span className="text-white font-bold text-sm">🍕</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 tracking-tight">Pizza Shop</h3>
            </Link>
            
            <div className="hidden md:flex items-center space-x-8">
              <Link
                to="/"
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                  location.pathname === '/'
                    ? 'text-black bg-gray-100'
                    : 'text-gray-600 hover:text-black hover:bg-gray-50'
                }`}
              >
                Menu
              </Link>
              <Link
                to="/orders"
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                  location.pathname === '/orders'
                    ? 'text-black bg-gray-100'
                    : 'text-gray-600 hover:text-black hover:bg-gray-50'
                }`}
              >
                My Orders
              </Link>
              {/* <button className="text-gray-600 hover:text-black transition-colors duration-200 px-3 py-2 rounded-md text-sm font-medium">
                Cart (0)
              </button> */}
            </div>

            {/* Mobile menu button */}
            <div className="md:hidden">
              <button className="text-gray-600 hover:text-black transition-colors duration-200 p-2">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </nav>
      
      <main className="min-h-screen">{children}</main>
      
      {/* Footer */}
      <footer className="bg-white border-t border-gray-100 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-500 text-sm">
            <p>&copy; 2024 Pizza Shop. Made with ❤️ for pizza lovers.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Layout;