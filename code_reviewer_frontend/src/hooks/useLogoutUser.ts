import { logoutUser } from "@/api/Auth/logOutUser.post";
import { useAuthStore } from "@/stores/authStore";
import { useMutation } from "@tanstack/react-query";

export const useLogoutUser = () => {
  const { logout } = useAuthStore();

  return useMutation({
    mutationFn: (accessToken: string) => logoutUser(accessToken),
    onSuccess: () => {
      logout();
    },
    onError: (error) => {
      console.error("Logout failed:", error);
      logout();
    },
  });
};
