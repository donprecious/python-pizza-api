export interface Pizza {
  id: string;
  name: string;
  base_price: number;
  ingredients: string[];
  image_url?: string;
  is_active: boolean;
}

export interface Extra {
  id: string;
  name: string;
  price: number;
}

export interface CartItem {
  pizza: Pizza;
  extras: Extra[];
  quantity: number;
}

export interface Customer {
  id?: string;
  name: string;
  email: string;
  phone: string;
  address: string;
}

export interface Order {
  id?: string;
  customer: Customer;
  items: CartItem[];
  total: number;
  status: 'pending' | 'confirmed' | 'preparing' | 'ready' | 'delivered';
  created_at?: string;
}

export interface PageMeta {
  page: number;
  per_page: number;
  total: number;
  pages: number;
  has_next: boolean;
  has_prev: boolean;
}

export interface Page<T> {
  items: T[];
  meta: PageMeta;
}

export interface ApiResponse<T> {
  is_success: boolean;
  data: T;
  message: string;
  error?: unknown;
  meta?: unknown;
}

// Order-related interfaces
export interface OrderCustomer {
  unique_identifier: string;
  fullname: string;
  full_address: string;
}

export interface OrderLine {
  pizza_id: string;
  quantity: number;
  extras: string[];
}

export interface OrderRequest {
  lines: OrderLine[];
  customer: OrderCustomer;
}

export interface OrderLineResponse {
  id: string;
  pizza_id: string;
  quantity: number;
  extras: string[];
  unit_base_price: number;
  unit_extras_total: number;
  line_total: number;
}

export interface OrderResponse {
  id: string;
  unique_identifier: string;
  status: string;
  subtotal: number;
  extras_total: number;
  grand_total: number;
  lines: OrderLineResponse[];
}

export interface CustomerDetails {
  fullname: string;
  email: string;
  address: string;
}