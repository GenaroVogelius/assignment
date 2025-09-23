import { getApiUrl } from "@/config/env";
import axios from "axios";

interface LogoutUserResponse {
  message: string;
}

export const logoutUser = async (
  accessToken: string
): Promise<LogoutUserResponse> => {
  try {
    const response = await axios.post<LogoutUserResponse>(
      getApiUrl("/api/logout"),
      {},
      {
        headers: {
          accept: "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
      }
    );

    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(
        `Failed to logout: ${
          error.response?.data?.message ||
          error.response?.statusText ||
          error.message
        }`
      );
    }
    throw new Error(`Failed to logout: ${error}`);
  }
};
