import axios, { AxiosInstance, AxiosError } from 'axios';
import jwtDecode from 'jwt-decode';

interface DecodedToken {
  exp: number;
  iat: number;
  user_id: number;
  email: string;
  [key: string]: any;
}

class APIClient {
  private client: AxiosInstance;
  private accessToken: string | null = null;
  private refreshToken: string | null = null;
  private isRefreshing = false;
  private failedQueue: Array<{
    resolve: (value: string) => void;
    reject: (reason?: any) => void;
  }> = [];

  constructor() {
    const baseURL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
    const timeout = parseInt(process.env.REACT_APP_API_TIMEOUT || '30000');

    this.client = axios.create({
      baseURL,
      timeout,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Interceptor de requête
    this.client.interceptors.request.use(
      (config) => {
        const token = this.getAccessToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Interceptor de réponse
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => this.handleResponseError(error)
    );

    this.loadTokens();
  }

  private loadTokens(): void {
    const accessToken = localStorage.getItem(
      process.env.REACT_APP_JWT_STORAGE_KEY || 'access_token'
    );
    const refreshToken = localStorage.getItem(
      process.env.REACT_APP_REFRESH_TOKEN_KEY || 'refresh_token'
    );

    if (accessToken) {
      this.accessToken = accessToken;
    }
    if (refreshToken) {
      this.refreshToken = refreshToken;
    }
  }

  public setTokens(accessToken: string, refreshToken?: string): void {
    this.accessToken = accessToken;
    localStorage.setItem(
      process.env.REACT_APP_JWT_STORAGE_KEY || 'access_token',
      accessToken
    );

    if (refreshToken) {
      this.refreshToken = refreshToken;
      localStorage.setItem(
        process.env.REACT_APP_REFRESH_TOKEN_KEY || 'refresh_token',
        refreshToken
      );
    }
  }

  public getAccessToken(): string | null {
    return this.accessToken;
  }

  public clearTokens(): void {
    this.accessToken = null;
    this.refreshToken = null;
    localStorage.removeItem(
      process.env.REACT_APP_JWT_STORAGE_KEY || 'access_token'
    );
    localStorage.removeItem(
      process.env.REACT_APP_REFRESH_TOKEN_KEY || 'refresh_token'
    );
  }

  public isTokenValid(token: string): boolean {
    try {
      const decoded: DecodedToken = jwtDecode(token);
      return decoded.exp * 1000 > Date.now();
    } catch {
      return false;
    }
  }

  private processQueue(token: string): void {
    this.failedQueue.forEach((prom) => {
      prom.resolve(token);
    });
    this.failedQueue = [];
  }

  private async refreshAccessToken(): Promise<string> {
    if (!this.refreshToken) {
      throw new Error('No refresh token available');
    }

    try {
      const response = await this.client.post('/users/token/refresh/', {
        refresh: this.refreshToken,
      });

      const { access } = response.data;
      this.setTokens(access, this.refreshToken);
      return access;
    } catch (error) {
      this.clearTokens();
      throw error;
    }
  }

  private handleResponseError = async (error: AxiosError): Promise<any> => {
    const originalRequest = error.config as any;

    if (error.response?.status === 401 && !originalRequest._retry) {
      if (this.isRefreshing) {
        return new Promise((resolve, reject) => {
          this.failedQueue.push({ resolve, reject });
        })
          .then((token) => {
            originalRequest.headers.Authorization = `Bearer ${token}`;
            return this.client(originalRequest);
          })
          .catch(() => {
            this.clearTokens();
            window.location.href = '/login';
            return Promise.reject(error);
          });
      }

      this.isRefreshing = true;
      originalRequest._retry = true;

      try {
        const token = await this.refreshAccessToken();
        this.processQueue(token);
        originalRequest.headers.Authorization = `Bearer ${token}`;
        return this.client(originalRequest);
      } catch (err) {
        this.clearTokens();
        window.location.href = '/login';
        return Promise.reject(err);
      } finally {
        this.isRefreshing = false;
      }
    }

    return Promise.reject(error);
  };

  public getClient(): AxiosInstance {
    return this.client;
  }

  // Méthodes convenience
  public async get<T>(url: string, config?: any): Promise<T> {
    const response = await this.client.get<T>(url, config);
    return response.data;
  }

  public async post<T>(url: string, data?: any, config?: any): Promise<T> {
    const response = await this.client.post<T>(url, data, config);
    return response.data;
  }

  public async put<T>(url: string, data?: any, config?: any): Promise<T> {
    const response = await this.client.put<T>(url, data, config);
    return response.data;
  }

  public async patch<T>(url: string, data?: any, config?: any): Promise<T> {
    const response = await this.client.patch<T>(url, data, config);
    return response.data;
  }

  public async delete<T>(url: string, config?: any): Promise<T> {
    const response = await this.client.delete<T>(url, config);
    return response.data;
  }

  // Méthodes spécifiques pour l'authentification
  public async login<T>(credentials: { email: string; password: string }): Promise<T> {
    return this.post<T>('/users/login/', credentials);
  }

  public async signup<T>(userData: {
    email: string;
    password: string;
    first_name: string;
    last_name: string;
  }): Promise<T> {
    return this.post<T>('/users/signup/', userData);
  }

  public async requestPasswordReset<T>(email: string): Promise<T> {
    return this.post<T>('/users/password-reset/', { email });
  }

  public async confirmPasswordReset<T>(data: {
    uidb64: string;
    token: string;
    new_password: string;
  }): Promise<T> {
    return this.post<T>('/users/password-reset-confirm/', data);
  }

  public async upload<T>(
    url: string,
    files: File | FileList,
    additionalData?: Record<string, any>
  ): Promise<T> {
    const formData = new FormData();

    if (files instanceof FileList) {
      Array.from(files).forEach((file) => {
        formData.append('files', file);
      });
    } else {
      formData.append('file', files);
    }

    // Ajouter les données supplémentaires
    if (additionalData) {
      Object.entries(additionalData).forEach(([key, value]) => {
        formData.append(key, JSON.stringify(value));
      });
    }

    return this.post<T>(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  }
}

export default new APIClient();
