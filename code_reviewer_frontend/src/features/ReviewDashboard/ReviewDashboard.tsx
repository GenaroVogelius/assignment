import { useGetReviewById } from "@/api/Reviews/ReviewById.get.api";
import { useGetReviewsByFilters } from "@/api/Reviews/ReviewsByFilters.get.api";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  exportToCsv,
  PROGRAMMING_LANGUAGES,
  SCORE_FILTERS,
  STATUS_FILTERS,
} from "@/lib/utils";
import { useEffect, useState } from "react";
import { ReviewFilters } from "./components/ReviewFilters";
import { ReviewsPanel } from "./components/ReviewsPanel";

import type { ReviewResponse } from "@/api/Reviews/types";
import { toast } from "sonner";

export function ReviewDashboard() {
  const programmingLanguagesWithAll = ["all", ...PROGRAMMING_LANGUAGES];

  // State for filters
  const [languageFilter, setLanguageFilter] = useState(
    programmingLanguagesWithAll[0]
  );
  const [statusFilter, setStatusFilter] = useState(STATUS_FILTERS[0]);
  const [scoreFilter, setScoreFilter] = useState(SCORE_FILTERS[0]);

  // State for reviews and selection
  const [filteredReviews, setFilteredReviews] = useState<ReviewResponse[]>([]);

  const [selectedReview, setSelectedReview] = useState<ReviewResponse | null>(
    null
  );

  const [currentSearchId, setCurrentSearchId] = useState<string>("");

  const [triggerSearchById, setTriggerSearchById] = useState<boolean>(false);
  const [triggerSearchByFilters, setTriggerSearchByFilters] =
    useState<boolean>(false);

  const exportFilteredReviews = () => {
    const headers = [
      "Review ID",
      "Language",
      "Status",
      "Score",
      "Suggestions",
      "Created At",
    ];

    const rows = [
      headers,
      ...filteredReviews.map((review) => [
        review.id,
        review.language,
        review.status,
        review.code_review.overall_score,
        review.code_review.suggestions,
        review.created_at,
      ]),
    ];

    const filename = `filtered-reviews-${
      new Date().toISOString().split("T")[0]
    }.csv`;
    exportToCsv(filename, rows);
  };

  const {
    data: reviewByIdData,
    isLoading: isLoadingById,
    error: errorById,
    refetch: refetchById,
  } = useGetReviewById(currentSearchId);

  const {
    data: reviewsByFiltersData,
    isLoading: isLoadingByFilters,
    error: errorByFilters,
    refetch: refetchByFilters,
  } = useGetReviewsByFilters({
    language: languageFilter,
    status: statusFilter,
    score: scoreFilter,
  });

  // Effect para ejecutar las queries cuando se activan los triggers
  useEffect(() => {
    if (triggerSearchById) {
      refetchById();
    } else if (triggerSearchByFilters) {
      refetchByFilters();
    }
  }, [
    triggerSearchById,
    triggerSearchByFilters,
    refetchById,
    refetchByFilters,
  ]);

  const data = triggerSearchById ? reviewByIdData : reviewsByFiltersData;
  const isLoading = triggerSearchById ? isLoadingById : isLoadingByFilters;
  const error = triggerSearchById ? errorById : errorByFilters;


  useEffect(() => {
    if (data) {
      if (triggerSearchById && reviewByIdData) {
        if (reviewByIdData.message === "Review not found") {
          toast.error("Review not found", {
            description: "The review id is not valid.",
          });
        } else if (reviewByIdData.message === "Review retrieved successfully") {
          setFilteredReviews([reviewByIdData]);
        }
      } else if (triggerSearchByFilters && reviewsByFiltersData) {
        setFilteredReviews(reviewsByFiltersData.reviews || []);
        if (
          reviewsByFiltersData.reviews &&
          reviewsByFiltersData.reviews.length === 0
        ) {
          toast.error("No reviews found", {
            description: "No reviews found with the filters applied.",
          });
        }
      }
    }
  }, [
    data,
    reviewByIdData,
    reviewsByFiltersData,
    triggerSearchById,
    triggerSearchByFilters,
  ]);

  const handleSearchById = (searchIdValue: string) => {
    setCurrentSearchId(searchIdValue);
    setTriggerSearchById(true);
    setTriggerSearchByFilters(false);
  };

  const handleSearchByFilters = () => {
    setCurrentSearchId("");
    setTriggerSearchById(false);
    setTriggerSearchByFilters(true);
  };


  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">🔍 Filters</CardTitle>
          <CardDescription>
            Filter and search through your code reviews
          </CardDescription>
        </CardHeader>
        <CardContent>
          <ReviewFilters
            handleSearchById={handleSearchById}
            handleSearchByFilters={handleSearchByFilters}
            languageFilter={languageFilter}
            setLanguageFilter={setLanguageFilter}
            statusFilter={statusFilter}
            setStatusFilter={setStatusFilter}
            scoreFilter={scoreFilter}
            setScoreFilter={setScoreFilter}
            programmingLanguages={programmingLanguagesWithAll}
            currentSearchId={currentSearchId}
            setCurrentSearchId={setCurrentSearchId}
          />
        </CardContent>
      </Card>
        <ReviewsPanel
          reviews={filteredReviews}
          exportFilteredReviews={exportFilteredReviews}
          selectedReview={selectedReview}
          setSelectedReview={setSelectedReview}
        />
    </div>
  );
}
