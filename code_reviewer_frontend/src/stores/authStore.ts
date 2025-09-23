import { create } from "zustand";
import { persist } from "zustand/middleware";

interface User {
  id: string;
  email: string;
  name: string;
}

interface AuthTokens {
  username: string;
  access_token: string;
  token_type: string;
  expires_in: number;
}

interface AuthState {
  user: User | null;
  tokens: AuthTokens | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  setTokens: (tokens: AuthTokens) => void;
  setUser: (user: User) => void;
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => void;
  checkAuth: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      tokens: null,
      isLoading: false,
      isAuthenticated: false,

      setTokens: (tokens: AuthTokens) => {
        set({ tokens, isAuthenticated: true });
      },

      setUser: (user: User) => {
        set({ user, isAuthenticated: true });
      },

      login: async (email: string, password: string): Promise<boolean> => {
        try {
          set({ isLoading: true });

          // Simulate API call - replace with actual authentication logic
          await new Promise((resolve) => setTimeout(resolve, 1000));

          // For demo purposes, accept any email/password combination
          // In a real app, this would be an API call to your backend
          if (email && password) {
            const userData: User = {
              id: "1",
              email,
              name: email.split("@")[0], // Use email prefix as name
            };

            set({
              user: userData,
              isAuthenticated: true,
              isLoading: false,
            });

            return true;
          }

          set({ isLoading: false });
          return false;
        } catch (error) {
          console.error("Login failed:", error);
          set({ isLoading: false });
          return false;
        }
      },

      logout: () => {
        set({
          user: null,
          tokens: null,
          isAuthenticated: false,
        });
      },

      checkAuth: () => {
        const { user, tokens } = get();
        set({ isAuthenticated: !!(user || tokens) });
      },
    }),
    {
      name: "auth-storage",
      partialize: (state) => ({ user: state.user, tokens: state.tokens }),
    }
  )
);
