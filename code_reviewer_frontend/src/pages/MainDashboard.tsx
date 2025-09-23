import { Header } from "@/components/Header";
import { SectionsTabs } from "@/components/SectionsTabs";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Tabs, TabsContent } from "@/components/ui/tabs";
// import { AnalyticsDashboard } from "@/features/AnalyticsDashboard";
import { CodeSubmissionForm } from "@/features/CodeSubmissionForm";
import { ReviewDashboard } from "@/features/ReviewDashboard";
import React from "react";

export const MainDashboard: React.FC = () => {

  class Enum {
    static readonly Submit = "submit";
    static readonly Reviews = "reviews";
    static readonly Analytics = "analytics";
  }

  const sections = [
    { value: Enum.Submit, title: "📝 Submit Code" },
    { value: Enum.Reviews, title: "📋 My Reviews" },
    { value: Enum.Analytics, title: "📊 Analytics" },
  ];

  const tabsContent = [
    {
      value: Enum.Submit,
      component: (
        <Card>
          <CardHeader>
            <CardTitle className="text-center">Submit Code for Review</CardTitle>
            <CardDescription className="text-center">
              Upload your code snippet and get automated feedback on code quality, security concerns, performance recommendations, issues and suggestions.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <CodeSubmissionForm />
          </CardContent>
        </Card>
      ),
    },
    {
      value: Enum.Reviews,
      component: <ReviewDashboard />,
    },
    // {
    //   value: Enum.Analytics,
    //   component: <AnalyticsDashboard />,
    // },
  ];
  return (
    <div className="p-4 min-h-screen bg-background">
      <Header />
      <main className="container mx-auto px-4 py-8">
        <Tabs defaultValue={Enum.Submit} className="space-y-6">
          <SectionsTabs sections={sections} />
          {tabsContent.map((tab) => (
            <TabsContent key={tab.value} value={tab.value}>
              {tab.component}
            </TabsContent>
          ))}
        </Tabs>
      </main>
    </div>
  );
};
