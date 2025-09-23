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
  PROGRAMMING_LANGUAGES,
  SCORE_FILTERS,
  STATUS_FILTERS,
} from "@/lib/utils";
import { useEffect, useState } from "react";
import { ReviewFilters } from "./components/ReviewFilters";
import { ReviewsPanel } from "./components/ReviewsPanel";

import type { ReviewResponse } from "@/api/Reviews/types";

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
    const csvContent = [
      [
        "Review ID",
        "Language",
        "Status",
        "Score",
        "Suggestions",
        "Created At",
      ].join(","),
      ...filteredReviews.map((review) =>
        [
          `"${review.id}"`,
          review.language,
          review.review_status,
          review.code_review.overall_score.toString(),
          `"${review.code_review.suggestions}"`,
          review.created_at,
        ].join(",")
      ),
    ].join("\n");

    const blob = new Blob([csvContent], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `filtered-reviews-${
      new Date().toISOString().split("T")[0]
    }.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  // Hooks para obtener datos - deben estar en el nivel superior del componente
  const {
    data: reviewByIdData,
    isLoading: isLoadingById,
    error: errorById,
    refetch: refetchById,
  } = useGetReviewById(currentSearchId, {
    enabled: false, // No ejecutar automáticamente
  });

  const {
    data: reviewsByFiltersData,
    isLoading: isLoadingByFilters,
    error: errorByFilters,
    refetch: refetchByFilters,
  } = useGetReviewsByFilters(
    {
      language: languageFilter,
      status: statusFilter,
      score: scoreFilter,
    },
    {
      enabled: false, // No ejecutar automáticamente
    }
  );

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

  // Determinar qué datos usar basado en el trigger activo
  const data = triggerSearchById ? reviewByIdData : reviewsByFiltersData;
  const isLoading = triggerSearchById ? isLoadingById : isLoadingByFilters;
  const error = triggerSearchById ? errorById : errorByFilters;

  // TODO: Usar isLoading y error para mostrar estados de carga y errores en la UI
  // Temporal: usar las variables para evitar warnings de linting
  if (isLoading || error) {
    // Estas variables estarán disponibles para uso futuro en la UI
  }

  // Effect para procesar los datos cuando se reciban de las APIs
  useEffect(() => {
    if (data) {
      if (triggerSearchById && reviewByIdData) {
        // Si es búsqueda por ID, crear un array con un solo elemento
        setFilteredReviews([reviewByIdData]);
      } else if (triggerSearchByFilters && reviewsByFiltersData) {
        // Si es búsqueda por filtros, usar el array de reviews
        setFilteredReviews(reviewsByFiltersData.reviews || []);
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
