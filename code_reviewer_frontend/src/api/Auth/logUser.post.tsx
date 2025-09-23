import axios from "axios";

interface LoginUserRequest {
  username: string;
  password: string;
}

interface LoginUserResponse {
  username: string;
  access_token: string;
  token_type: string;
  expires_in: number;
}

export const loginUser = async (
  userData: LoginUserRequest
): Promise<LoginUserResponse> => {
  try {
    const response = await axios.post<LoginUserResponse>(
      "http://127.0.0.1:8000/api/login",
      userData,
      {
        headers: {
          accept: "application/json",
          "Content-Type": "application/json",
        },
      }
    );

    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(
        `Failed to login: ${
          error.response?.data?.message ||
          error.response?.statusText ||
          error.message
        }`
      );
    }
    throw new Error(`Failed to login: ${error}`);
  }
};
