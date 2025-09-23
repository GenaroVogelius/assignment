import type { ReviewResponse } from "@/api/Reviews/types";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { getScoreColor, getStatusColor, getStatusIcon, getRiskColor, safeFormatDate } from "@/lib/utils";

export function ReviewDetails({
  review,
  isOpen,
  onClose,
}: {
  review: ReviewResponse;
  isOpen: boolean;
  onClose: () => void;
}) {

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-3">
            Review Details
            <Badge variant="outline">{review.language}</Badge>
            <Badge className={getStatusColor(review.status)}>
              {getStatusIcon(review.status)}
              <span className="ml-1 capitalize">{review.status}</span>
            </Badge>
          </DialogTitle>
          <DialogDescription>
            Review ID: {review.id} • Created:{" "}
            {safeFormatDate(
              new Date(review.created_at),
              "MMM d, yyyy 'at' h:mm a"
            )}
          </DialogDescription>
        </DialogHeader>

        <div className="grid gap-6">
          {/* Overall Score */}
          {review.code_review.overall_score && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  Overall Score
                  <span
                    className={`text-2xl font-bold ${getScoreColor(
                      review.code_review.overall_score
                    )}`}
                  >
                    {review.code_review.overall_score}/10
                  </span>
                </CardTitle>
              </CardHeader>
            </Card>
          )}

          {/* Security Assessment */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                Security Assessment
                <Badge
                  className={getRiskColor(
                    review.code_review.security_assessment.risk_level
                  )}
                >
                  {review.code_review.security_assessment.risk_level.toUpperCase()}{" "}
                  RISK
                </Badge>
              </CardTitle>
            </CardHeader>
            <CardContent>
              {review.code_review.security_assessment.concerns.length > 0 ? (
                <div className="space-y-2">
                  <h4 className="font-medium">Security Concerns:</h4>
                  <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground">
                    {review.code_review.security_assessment.concerns.map(
                      (concern, index) => (
                        <li key={index}>{concern}</li>
                      )
                    )}
                  </ul>
                </div>
              ) : (
                <p className="text-green-600 font-medium">
                  ✅ No security concerns identified
                </p>
              )}
            </CardContent>
          </Card>

          {/* Code Submission */}
          <Card>
            <CardHeader>
              <CardTitle>Original Code</CardTitle>
            </CardHeader>
            <CardContent>
              <pre className="bg-muted p-4 rounded-lg overflow-x-auto text-sm">
                <code>{review.code_submission}</code>
              </pre>
            </CardContent>
          </Card>

          {/* Suggestions */}
          {review.code_review.suggestions && (
            <Card>
              <CardHeader>
                <CardTitle>Suggestions</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm whitespace-pre-wrap">
                  {review.code_review.suggestions}
                </p>
              </CardContent>
            </Card>
          )}

          {/* Refactored Example */}
          {review.code_review.refactored_example && (
            <Card>
              <CardHeader>
                <CardTitle>Refactored Example</CardTitle>
              </CardHeader>
              <CardContent>
                <pre className="bg-muted p-4 rounded-lg overflow-x-auto text-sm">
                  <code>{review.code_review.refactored_example}</code>
                </pre>
              </CardContent>
            </Card>
          )}

          {/* Category */}
          {review.code_review.category && (
            <Card>
              <CardHeader>
                <CardTitle>Category</CardTitle>
              </CardHeader>
              <CardContent>
                <Badge variant="outline">{review.code_review.category}</Badge>
              </CardContent>
            </Card>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}
