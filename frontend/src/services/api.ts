import type { Pizza, Extra, Order, ApiResponse, Page, OrderRequest, OrderResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

class ApiService {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Pizza endpoints
  async getPizzas(page: number = 1, perPage: number = 10): Promise<ApiResponse<Page<Pizza>>> {
    return this.request<ApiResponse<Page<Pizza>>>(`/pizzas?page=${page}&page_size=${perPage}`);
  }

  async getPizza(id: string): Promise<ApiResponse<Pizza>> {
    return this.request<ApiResponse<Pizza>>(`/pizzas/${id}`);
  }

  // Extra endpoints
  async getExtras(): Promise<ApiResponse<Extra[]>> {
    return this.request<ApiResponse<Extra[]>>('/extras');
  }

  // Order endpoints
  async createOrder(order: Omit<Order, 'id' | 'created_at'>): Promise<ApiResponse<Order>> {
    return this.request<ApiResponse<Order>>('/orders', {
      method: 'POST',
      body: JSON.stringify(order),
    });
  }

  async getOrder(id: number): Promise<ApiResponse<Order>> {
    return this.request<ApiResponse<Order>>(`/orders/${id}`);
  }

  // Checkout endpoint for new order flow
  async checkout(orderData: OrderRequest): Promise<ApiResponse<OrderResponse>> {
    return this.request<ApiResponse<OrderResponse>>('/orders/checkout', {
      method: 'POST',
      body: JSON.stringify(orderData),
    });
  }

  // Get orders by unique identifier with optional search filters
  async getOrders(
    uniqueIdentifier?: string,
    page: number = 1,
    perPage: number = 10,
    searchQuery?: string
  ): Promise<ApiResponse<OrderResponse[]>> {
    const params = new URLSearchParams();
    
    if (uniqueIdentifier) {
      params.append('unique_identifier', uniqueIdentifier);
    }
    
    params.append('page', page.toString());
    params.append('per_page', perPage.toString());
    
    if (searchQuery && searchQuery.trim()) {
      params.append('search', searchQuery.trim());
    }
    
    return this.request<ApiResponse<OrderResponse[]>>(`/orders/?${params.toString()}`);
  }

  // Health check
  async healthCheck(): Promise<{ status: string }> {
    return this.request<{ status: string }>('/health');
  }
}

export const apiService = new ApiService();
export default apiService;