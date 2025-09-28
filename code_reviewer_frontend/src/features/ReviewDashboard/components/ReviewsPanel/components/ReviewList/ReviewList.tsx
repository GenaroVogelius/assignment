import type { ReviewResponse } from "@/api/Reviews/types";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { safeFormatDate } from "@/lib/utils";

export function ReviewList({
  reviews,
  selectedReview,
  setSelectedReview,
  getStatusColor,
  getStatusIcon,
  getScoreColor,
}: {
  reviews: ReviewResponse[];
  selectedReview: ReviewResponse | null;
  setSelectedReview: (review: ReviewResponse) => void;
  getStatusColor: (status: string) => string;
  getStatusIcon: (status: string) => string;
  getScoreColor: (score: number) => string;
}) {
  return reviews.length === 0 ? (
    <Card>
      <CardContent className="flex flex-col items-center justify-center py-12">
        <span className="text-4xl mb-4">🔍</span>
        <p className="text-muted-foreground text-center">
          Use the filters to search for reviews
        </p>
      </CardContent>
    </Card>
  ) : (
    <div className="space-y-3">
      {reviews.map((review) => (
        <Card
          key={review.id}
          className={`cursor-pointer transition-colors hover:bg-muted/50 ${
            selectedReview?.id === review.id ? "ring-2 ring-primary" : ""
          }`}
          onClick={() => setSelectedReview(review)}
        >
          <CardContent className="p-4">
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-2">
                  <h4 className="font-medium">Review ID: {review.id}</h4>
                </div>
                <div className="flex items-center gap-4 text-sm text-muted-foreground">
                  <div className="flex items-center gap-1">
                    📅{" "}
                    {safeFormatDate(new Date(review.created_at), "MMM d, yyyy")}
                  </div>
                  {review.code_review?.overall_score && (
                    <div
                      className={`font-medium ${getScoreColor(
                        review.code_review.overall_score
                      )}`}
                    >
                      Score: {review.code_review.overall_score}/10
                    </div>
                  )}
                </div>
              </div>
              <div className="flex items-center gap-2">
                <Badge className={getStatusColor(review.status)}>
                  {getStatusIcon(review.status)}
                  <span className="ml-1 capitalize">{review.status}</span>
                </Badge>
                <Badge variant="outline" className="text-xs">
                  {review.language}
                </Badge>
              </div>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
