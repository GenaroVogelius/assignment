import { getApiUrl } from "@/config/env";
import axios from "axios";

interface RegisterUserRequest {
  username: string;
  email: string;
  password: string;
}

interface RegisterUserResponse {
  message: string;
  user?: {
    id: string;
    username: string;
    email: string;
  };
}

export const registerUser = async (
  userData: RegisterUserRequest
): Promise<RegisterUserResponse> => {
  try {
    const response = await axios.post<RegisterUserResponse>(
      getApiUrl("/api/register"),
      userData,
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(
        `Failed to register user: ${
          error.response?.data?.message ||
          error.response?.statusText ||
          error.message
        }`
      );
    }
    throw new Error(`Failed to register user: ${error}`);
  }
};
