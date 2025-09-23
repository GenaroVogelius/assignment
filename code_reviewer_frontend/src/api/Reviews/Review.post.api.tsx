import { getApiUrl } from "@/config/env";
import { useAuthStore } from "@/stores/authStore";
import axios from "axios";

interface ReviewSubmissionRequest {
  language: string;
  code_submission: string;
}

interface ReviewSubmissionResponse {
  message: string;
  review_id: string;
}

export const submitCodeReview = async (
  submission: ReviewSubmissionRequest
): Promise<ReviewSubmissionResponse> => {
  const { tokens } = useAuthStore.getState();

  if (!tokens?.access_token) {
    throw new Error("No authentication token found. Please log in.");
  }

  try {
    const response = await axios.post<ReviewSubmissionResponse>(
      getApiUrl("/api/reviews"),
      submission,
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${tokens.access_token}`,
          accept: "application/json",
        },
      }
    );

    const result = response.data;

    // Store in localStorage for persistence
    const existingReviews = JSON.parse(
      localStorage.getItem("codeReviews") || "[]"
    );
    existingReviews.unshift(result);
    localStorage.setItem("codeReviews", JSON.stringify(existingReviews));

    return result;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(
        `Failed to submit code review: ${
          error.response?.statusText || error.message
        }`
      );
    }
    throw new Error(`Failed to submit code review: ${error}`);
  }
};
