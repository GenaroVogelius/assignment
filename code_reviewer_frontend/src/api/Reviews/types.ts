interface SecurityAssessment {
  risk_level: "low" | "medium" | "high";
  concerns: string[];
}

export interface CodeReview {
  overall_score: number;
  category: string;
  security_assessment: SecurityAssessment;
  suggestions: string;
  refactored_example: string;
}

export interface ReviewResponse {
  id: string;
  language: string;
  code_submission: string;
  code_review: CodeReview;
  review_status: "pending" | "completed" | "failed";
  created_at: string;
  updated_at: string;
  status: string;
}

export interface FiltersApplied {
  language: string;
  status: string;
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

