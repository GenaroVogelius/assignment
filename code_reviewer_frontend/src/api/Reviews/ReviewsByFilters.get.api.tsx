import { getApiUrl } from "@/config/env";
import { useAuthStore } from "@/stores/authStore";
import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import type { ReviewResponse } from "./types";

interface FiltersApplied {
  language: string;
  status: string;
  created_after: string;
  created_before: string;
  score: string;
}

export interface ReviewsByFiltersResponse {
  message: string;
  username: string;
  email: string;
  status: string;
  filters_applied: FiltersApplied;
  total_reviews: number;
  reviews: ReviewResponse[];
}

export interface ReviewsByFiltersParams {
  language?: string;
  status?: string;
  created_after?: string;
  created_before?: string;
  score?: string;
}

export const fetchReviewsByFilters = async (
  params: ReviewsByFiltersParams = {}
): Promise<ReviewsByFiltersResponse> => {
  const { tokens } = useAuthStore.getState();

  if (!tokens?.access_token) {
    throw new Error("No authentication token found. Please log in.");
  }

  try {
    // Build query parameters
    const queryParams = new URLSearchParams();

    // Add parameters only if they are not "all" or undefined
    Object.entries(params).forEach(([key, value]) => {
      if (value && value !== "all") {
        queryParams.append(key, value);
      }
    });

    const queryString = queryParams.toString();
    const url = `${getApiUrl("/api/reviews")}${
      queryString ? `?${queryString}` : ""
    }`;

    const response = await axios.get<ReviewsByFiltersResponse>(url, {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${tokens.access_token}`,
        accept: "application/json",
      },
    });

    console.log(response.data);

    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(
        `Failed to fetch reviews: ${
          error.response?.statusText || error.message
        }`
      );
    }
    throw new Error(`Failed to fetch reviews: ${error}`);
  }
};

export const useGetReviewsByFilters = (
  params: ReviewsByFiltersParams = {},
) => {
  return useQuery({
    queryKey: ["reviews", "filters", params],
    queryFn: () => fetchReviewsByFilters(params),
    staleTime: 5 * 60 * 1000, // Consider data fresh for 5 minutes
    retry: (failureCount, error) => {
      if (error instanceof Error && error.message.includes("401")) {
        return false;
      }
      return failureCount < 3;
    },
  });
};
