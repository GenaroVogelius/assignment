import { clsx, type ClassValue } from "clsx";
import { format } from "date-fns";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export const PROGRAMMING_LANGUAGES = [
  "javascript",
  "typescript",
  "python",
  "java",
  "cpp",
  "c",
  "csharp",
  "php",
  "ruby",
  "go",
  "rust",
  "swift",
  "kotlin",
  "scala",
  "r",
  "matlab",
  "sql",
  "html",
  "css",
  "scss",
  "json",
  "xml",
  "yaml",
  "markdown",
  "bash",
  "powershell",
];

export const STATUS_FILTERS = ["all", "pending", "completed", "failed"];

export const DATE_RANGE_FILTERS = ["all", "today", "week", "month"];

export const SCORE_FILTERS = [
  "all",
  "1",
  "2",
  "3",
  "4",
  "5",
  "6",
  "7",
  "8",
  "9",
  "10",
];

export const safeFormatDate = (date: Date, formatString: string) => {
  try {
    return format(date, formatString);
  } catch (error) {
    return "Invalid Date";
  }
};





export const getStatusColor = (status: string) => {
  switch (status.toLowerCase()) {
    case "completed":
      return "bg-green-100 text-green-800 border-green-200";
    case "pending":
      return "bg-yellow-100 text-yellow-800 border-yellow-200";
    case "failed":
      return "bg-red-100 text-red-800 border-red-200";
    default:
      return "bg-gray-100 text-gray-800 border-gray-200";
  }
};

export const getStatusIcon = (status: string) => {
  switch (status.toLowerCase()) {
    case "completed":
      return "✅";
    case "pending":
      return "⏳";
    case "failed":
      return "❌";
    default:
      return "📋";
  }
};

export const getScoreColor = (score: number) => {
  if (score >= 8) return "text-green-600";
  if (score >= 6) return "text-yellow-600";
  return "text-red-600";
};

export const getRiskColor = (risk: string) => {
  switch (risk.toLowerCase()) {
    case "high":
      return "bg-red-100 text-red-800 border-red-200";
    case "medium":
      return "bg-yellow-100 text-yellow-800 border-yellow-200";
    case "low":
      return "bg-green-100 text-green-800 border-green-200";
    default:
      return "bg-gray-100 text-gray-800 border-gray-200";
  }
};