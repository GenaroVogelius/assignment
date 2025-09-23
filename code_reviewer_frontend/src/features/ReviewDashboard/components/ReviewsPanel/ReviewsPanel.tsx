import type { ReviewResponse } from "@/api/Reviews/types";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { ReviewDetails } from "./components/ReviewDetails/ReviewDetails";
import { ReviewList } from "./components/ReviewList/ReviewList";
import { getStatusColor, getStatusIcon, getScoreColor } from "@/lib/utils";

export function ReviewsPanel({
  reviews,
  exportFilteredReviews,
  selectedReview,
  setSelectedReview,
}: {
  reviews: ReviewResponse[];
  exportFilteredReviews: () => void;
  selectedReview: ReviewResponse | null;
  setSelectedReview: (review: ReviewResponse) => void;
}) {
  const [isDialogOpen, setIsDialogOpen] = useState(false);

  const handleReviewSelect = (review: ReviewResponse) => {
    setSelectedReview(review);
    setIsDialogOpen(true);
  };

  const handleDialogClose = () => {
    setIsDialogOpen(false);
  };


  return (
    <div className="grid grid-cols-1 gap-6">
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold">
            Review History ({reviews.length})
          </h3>
          {reviews.length > 0 && (
            <Button onClick={exportFilteredReviews} variant="outline" size="sm">
              📥 Export all reviews into CSV
            </Button>
          )}
        </div>

        <ReviewList
          reviews={reviews}
          selectedReview={selectedReview}
          setSelectedReview={handleReviewSelect}
          getStatusColor={getStatusColor}
          getStatusIcon={getStatusIcon}
          getScoreColor={getScoreColor}
        />
      </div>

      {/* Review Details */}
      {selectedReview && (
        <ReviewDetails
          review={selectedReview}
          isOpen={isDialogOpen}
          onClose={handleDialogClose}
        />
      )}
    </div>
  );
}
