import { getApiUrl } from "@/config/env";
import { useAuthStore } from "@/stores/authStore";
import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import type { ReviewResponse } from "./types";

export const fetchReviewById = async (
  reviewId: string
): Promise<ReviewResponse> => {
  const { tokens } = useAuthStore.getState();

  if (!tokens?.access_token) {
    throw new Error("No authentication token found. Please log in.");
  }

  try {
    const response = await axios.get<ReviewResponse>(
      getApiUrl(`/api/reviews/${reviewId}`),
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${tokens.access_token}`,
          accept: "application/json",
        },
      }
    );

    console.log(response.data);

    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(
        `Failed to fetch review: ${error.response?.statusText || error.message}`
      );
    }
    throw new Error(`Failed to fetch review: ${error}`);
  }
};

export const useGetReviewById = (
  reviewId: string,
) => {
  return useQuery({
    queryKey: ["review", reviewId],
    queryFn: () => fetchReviewById(reviewId),
    staleTime: 5 * 60 * 1000, 
    retry: (failureCount, error) => {
      // Don't retry on 404 or 401 errors
      if (error instanceof Error && error.message.includes("404")) {
        return false;
      }
      if (error instanceof Error && error.message.includes("401")) {
        return false;
      }
      return failureCount < 3;
    },
  });
};
