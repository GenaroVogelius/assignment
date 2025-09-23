import { CardDescription, CardTitle } from "@/components/ui/card";

export interface AuthHeaderProps {
  title: string;
  description: string;
}

// title = Welcome to CodeReview Pro
// Sign in to access your code review dashboard

export function AuthHeader({ title, description }: AuthHeaderProps) {
  return (
    <>
      <div className="flex justify-center mb-6">
        <div className="relative">
          <div className="flex h-20 w-20 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-600 to-indigo-700 text-white shadow-lg shadow-blue-500/25">
            <span className="text-2xl font-bold">CR</span>
          </div>
          <div className="absolute -inset-1 bg-gradient-to-br from-blue-600 to-indigo-700 rounded-2xl blur opacity-30 -z-10"></div>
        </div>
      </div>
      <CardTitle className="text-2xl text-center font-bold text-slate-900 mb-2">
        {title}
      </CardTitle>
      <CardDescription className="text-slate-600 text-base text-center pb-2">
        {description}
      </CardDescription>
    </>
  );
}
