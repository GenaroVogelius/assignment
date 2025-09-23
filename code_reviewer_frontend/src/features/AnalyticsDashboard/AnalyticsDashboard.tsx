import type { ReviewSubmission } from "@/api/Reviews/types";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  AlertTriangle,
  CheckCircle,
  Code,
  Download,
  TrendingDown,
  TrendingUp,
} from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

interface AnalyticsData {
  totalReviews: number;
  averageScore: number;
  completedReviews: number;
  pendingReviews: number;
  failedReviews: number;
  mostCommonLanguage: string;
  mostCommonIssues: { issue: string; count: number }[];
  scoreDistribution: { range: string; count: number }[];
  languageDistribution: {
    language: string;
    count: number;
    percentage: number;
  }[];
  dailySubmissions: { date: string; count: number }[];
  scoreOverTime: { date: string; score: number }[];
}

const COLORS = [
  "hsl(var(--chart-1))",
  "hsl(var(--chart-2))",
  "hsl(var(--chart-3))",
  "hsl(var(--chart-4))",
  "hsl(var(--chart-5))",
];

export function AnalyticsDashboard() {
  const [reviews, setReviews] = useState<ReviewSubmission[]>([]);
  const [timeRange, setTimeRange] = useState("all");

  // Load reviews from localStorage
  useEffect(() => {
    const storedReviews = localStorage.getItem("codeReviews");
    if (storedReviews) {
      const parsedReviews = JSON.parse(storedReviews).map((review: any) => ({
        ...review,
        submittedAt: new Date(review.submittedAt),
      }));
      setReviews(parsedReviews);
    }
  }, []);

  // Filter reviews by time range
  const filteredReviews = useMemo(() => {
    if (timeRange === "all") return reviews;

    const now = new Date();
    const filterDate = new Date();

    switch (timeRange) {
      case "week":
        filterDate.setDate(now.getDate() - 7);
        break;
      case "month":
        filterDate.setMonth(now.getMonth() - 1);
        break;
      case "quarter":
        filterDate.setMonth(now.getMonth() - 3);
        break;
      default:
        return reviews;
    }

    return reviews.filter((review) => review.submittedAt >= filterDate);
  }, [reviews, timeRange]);

  // Calculate analytics data
  const analyticsData: AnalyticsData = useMemo(() => {
    const completedReviews = filteredReviews.filter(
      (r) => r.status === "completed"
    );
    const scores = completedReviews.filter((r) => r.score).map((r) => r.score!);

    // Language distribution
    const languageCounts = filteredReviews.reduce((acc, review) => {
      acc[review.language] = (acc[review.language] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    const languageDistribution = Object.entries(languageCounts)
      .map(([language, count]) => ({
        language,
        count,
        percentage: Math.round((count / filteredReviews.length) * 100),
      }))
      .sort((a, b) => b.count - a.count);

    // Score distribution
    const scoreRanges = [
      { range: "9-10", min: 9, max: 10 },
      { range: "7-8", min: 7, max: 8 },
      { range: "5-6", min: 5, max: 6 },
      { range: "3-4", min: 3, max: 4 },
      { range: "1-2", min: 1, max: 2 },
    ];

    const scoreDistribution = scoreRanges.map((range) => ({
      range: range.range,
      count: scores.filter((score) => score >= range.min && score <= range.max)
        .length,
    }));

    // Common issues
    const allIssues = completedReviews.flatMap((r) => r.issues || []);
    const issueCounts = allIssues.reduce((acc, issue) => {
      acc[issue] = (acc[issue] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    const mostCommonIssues = Object.entries(issueCounts)
      .map(([issue, count]) => ({ issue, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 5);

    // Daily submissions (last 7 days)
    const last7Days = Array.from({ length: 7 }, (_, i) => {
      const date = new Date();
      date.setDate(date.getDate() - i);
      return date.toISOString().split("T")[0];
    }).reverse();

    const dailySubmissions = last7Days.map((date) => ({
      date: new Date(date).toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
      }),
      count: filteredReviews.filter(
        (r) => r.submittedAt.toISOString().split("T")[0] === date
      ).length,
    }));

    // Score over time (last 10 completed reviews)
    const recentCompletedReviews = completedReviews
      .sort((a, b) => b.submittedAt.getTime() - a.submittedAt.getTime())
      .slice(0, 10)
      .reverse();

    const scoreOverTime = recentCompletedReviews.map((review, index) => ({
      date: `Review ${index + 1}`,
      score: review.score || 0,
    }));

    return {
      totalReviews: filteredReviews.length,
      averageScore:
        scores.length > 0
          ? Math.round(
              (scores.reduce((a, b) => a + b, 0) / scores.length) * 10
            ) / 10
          : 0,
      completedReviews: completedReviews.length,
      pendingReviews: filteredReviews.filter((r) => r.status === "pending")
        .length,
      failedReviews: filteredReviews.filter((r) => r.status === "failed")
        .length,
      mostCommonLanguage: languageDistribution[0]?.language || "N/A",
      mostCommonIssues,
      scoreDistribution,
      languageDistribution,
      dailySubmissions,
      scoreOverTime,
    };
  }, [filteredReviews]);

  const exportData = () => {
    const csvContent = [
      ["Title", "Language", "Status", "Score", "Issues", "Submitted At"].join(
        ","
      ),
      ...filteredReviews.map((review) =>
        [
          `"${review.title}"`,
          review.language,
          review.status,
          review.score || "",
          `"${(review.issues || []).join("; ")}"`,
          review.submittedAt.toISOString(),
        ].join(",")
      ),
    ].join("\n");

    const blob = new Blob([csvContent], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `code-reviews-${timeRange}-${
      new Date().toISOString().split("T")[0]
    }.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  if (filteredReviews.length === 0) {
    return (
      <Card>
        <CardContent className="flex flex-col items-center justify-center py-12">
          <BarChart className="h-12 w-12 text-muted-foreground mb-4" />
          <p className="text-muted-foreground text-center">
            No data available for analytics
          </p>
          <p className="text-sm text-muted-foreground text-center mt-2">
            Submit some code reviews to see statistics
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header with filters and export */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Analytics Dashboard</h2>
          <p className="text-muted-foreground">
            Insights and statistics from your code reviews
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Select value={timeRange} onValueChange={setTimeRange}>
            <SelectTrigger className="w-40">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Time</SelectItem>
              <SelectItem value="week">Last Week</SelectItem>
              <SelectItem value="month">Last Month</SelectItem>
              <SelectItem value="quarter">Last Quarter</SelectItem>
            </SelectContent>
          </Select>
          <Button onClick={exportData} variant="outline">
            <Download className="h-4 w-4 mr-2" />
            Export CSV
          </Button>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Reviews</CardTitle>
            <Code className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {analyticsData.totalReviews}
            </div>
            <p className="text-xs text-muted-foreground">
              {analyticsData.completedReviews} completed,{" "}
              {analyticsData.pendingReviews} pending
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Average Score</CardTitle>
            {analyticsData.averageScore >= 7 ? (
              <TrendingUp className="h-4 w-4 text-green-600" />
            ) : (
              <TrendingDown className="h-4 w-4 text-red-600" />
            )}
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {analyticsData.averageScore}/10
            </div>
            <p className="text-xs text-muted-foreground">
              {analyticsData.averageScore >= 7
                ? "Good quality"
                : "Needs improvement"}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Success Rate</CardTitle>
            <CheckCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {analyticsData.totalReviews > 0
                ? Math.round(
                    (analyticsData.completedReviews /
                      analyticsData.totalReviews) *
                      100
                  )
                : 0}
              %
            </div>
            <p className="text-xs text-muted-foreground">
              Reviews completed successfully
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Top Language</CardTitle>
            <Code className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold capitalize">
              {analyticsData.mostCommonLanguage}
            </div>
            <p className="text-xs text-muted-foreground">
              Most frequently reviewed
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Language Distribution */}
        <Card>
          <CardHeader>
            <CardTitle>Language Distribution</CardTitle>
            <CardDescription>
              Breakdown of reviews by programming language
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={analyticsData.languageDistribution}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ language, percentage }) =>
                    `${language} (${percentage}%)`
                  }
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="count"
                >
                  {analyticsData.languageDistribution.map((_, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={COLORS[index % COLORS.length]}
                    />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Score Distribution */}
        <Card>
          <CardHeader>
            <CardTitle>Score Distribution</CardTitle>
            <CardDescription>Distribution of quality scores</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={analyticsData.scoreDistribution}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="range" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="hsl(var(--primary))" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Daily Submissions */}
        <Card>
          <CardHeader>
            <CardTitle>Daily Submissions</CardTitle>
            <CardDescription>
              Review submissions over the last 7 days
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={analyticsData.dailySubmissions}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="hsl(var(--chart-2))" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Score Trend */}
        <Card>
          <CardHeader>
            <CardTitle>Score Trend</CardTitle>
            <CardDescription>
              Quality score trend over recent reviews
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={analyticsData.scoreOverTime}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis domain={[0, 10]} />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="score"
                  stroke="hsl(var(--chart-3))"
                  strokeWidth={2}
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Common Issues */}
      {analyticsData.mostCommonIssues.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-yellow-500" />
              Most Common Issues
            </CardTitle>
            <CardDescription>
              Issues frequently found in code reviews
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {analyticsData.mostCommonIssues.map((issue, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between p-3 bg-muted rounded-lg"
                >
                  <span className="text-sm">{issue.issue}</span>
                  <Badge variant="secondary">{issue.count} occurrences</Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
