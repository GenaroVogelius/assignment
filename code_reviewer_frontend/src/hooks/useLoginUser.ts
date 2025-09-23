import { loginUser } from "@/api/Auth/logUser.post";
import { useAuthStore } from "@/stores/authStore";
import { useMutation } from "@tanstack/react-query";

interface LoginUserRequest {
  username: string;
  password: string;
}

export const useLoginUser = () => {
  const { setTokens } = useAuthStore();

  return useMutation({
    mutationFn: (userData: LoginUserRequest) => loginUser(userData),
    onSuccess: (data) => {
      // Store tokens using Zustand
      setTokens({
        username: data.username,
        access_token: data.access_token,
        token_type: data.token_type,
        expires_in: data.expires_in,
      });
    },
    onError: (error) => {
      console.error("Login failed:", error);
    },
  });
};
