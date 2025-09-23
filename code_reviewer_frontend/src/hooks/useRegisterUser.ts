import { registerUser } from "@/api/Auth/createUser.post";
import { useMutation } from "@tanstack/react-query";

interface RegisterUserRequest {
  username: string;
  email: string;
  password: string;
}

export const useRegisterUser = () => {
  return useMutation({
    mutationFn: (userData: RegisterUserRequest) => registerUser(userData),
    onSuccess: (data) => {
      console.log("User registered successfully:", data);
    },
    onError: (error) => {
      console.error("Registration failed:", error);
    },
  });
};
