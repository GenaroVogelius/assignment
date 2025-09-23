import { logoutUser } from "@/api/Auth/logOutUser.post";
import { useAuthStore } from "@/stores/authStore";
import { useMutation } from "@tanstack/react-query";

export const useLogoutUser = () => {
  const { logout } = useAuthStore();

  return useMutation({
    mutationFn: (accessToken: string) => logoutUser(accessToken),
    onSuccess: (data) => {
      console.log("User logged out successfully:", data);
      // Clear tokens and user data from Zustand store
      logout();
    },
    onError: (error) => {
      console.error("Logout failed:", error);
      // Even if the API call fails, we should still clear local state
      logout();
    },
  });
};
