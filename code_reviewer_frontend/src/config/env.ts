// Environment configuration
export const config = {
  // API Base URL - defaults to localhost for development
  API_BASE_URL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000",

  // Environment
  NODE_ENV: import.meta.env.MODE || "development",

  // App version
  APP_VERSION: import.meta.env.VITE_APP_VERSION || "1.0.0",
} as const;

// Type for environment variables
export type Config = typeof config;

// Helper function to get full API URL
export const getApiUrl = (endpoint: string): string => {
  const baseUrl = config.API_BASE_URL.endsWith("/")
    ? config.API_BASE_URL.slice(0, -1)
    : config.API_BASE_URL;

  const cleanEndpoint = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;

  return `${baseUrl}${cleanEndpoint}`;
};
