export interface Pizza {
  id: number;
  name: string;
  description: string;
  price: number;
  ingredients: string[];
  image_url?: string;
}

export interface Extra {
  id: number;
  name: string;
  price: number;
}

export interface CartItem {
  pizza: Pizza;
  extras: Extra[];
  quantity: number;
}

export interface Customer {
  id?: number;
  name: string;
  email: string;
  phone: string;
  address: string;
}

export interface Order {
  id?: number;
  customer: Customer;
  items: CartItem[];
  total: number;
  status: 'pending' | 'confirmed' | 'preparing' | 'ready' | 'delivered';
  created_at?: string;
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}