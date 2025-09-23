import type React from "react";

import { submitCodeReview } from "@/api/Reviews/Review.post.api";
import { CodeEditor } from "@/components/CodeEditor";
import { Selector } from "@/components/Selector";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { useAuthStore } from "@/stores/authStore";
import { useMutation } from "@tanstack/react-query";
import { useState } from "react";
import { toast } from "sonner";
import { PROGRAMMING_LANGUAGES } from "@/lib/utils";


export function CodeSubmissionForm() {
  const [languageSelected, setLanguageSelected] = useState(
    PROGRAMMING_LANGUAGES[0]
  );
  const [code, setCode] = useState("");
  const { logout } = useAuthStore();

  const mutation = useMutation({
    mutationFn: submitCodeReview,
    onSuccess: () => {
      toast.success("Code submitted successfully!", {
        description: "Your code has been sent for review, check the reviews tab to see the results.",
      });
    },
    onError: (error: any) => {
      // Check if it's a 401 Unauthorized error
      if (error?.response?.status === 401 || error?.status === 401) {
        toast.error("Session expired", {
          description: "Please log in again to continue.",
        });
        logout();
      } else {
        toast.error("Submission failed", {
          description:
            "There was an error submitting your code. Please try again.",
        });
      }
    },
  });

  const handleCodeSubmission = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!languageSelected || !code) return;

    try {
      await mutation.mutateAsync({
        language: languageSelected,
        code_submission: code,
      });

      setCode("");
    } catch (error) {
      // Error handling is done in the mutation's onError callback
      console.error("Submission failed:", error);
    }
  };

  return (
    <div className="space-y-6">
      <form onSubmit={handleCodeSubmission} className="space-y-4">
        <Selector
          label="Programming language"
          placeholder="Select language"
          value={languageSelected}
          onChange={setLanguageSelected}
          required={true}
          options={PROGRAMMING_LANGUAGES}
          className="space-y-2 flex flex-col items-end text-right"
        />

        <div className="space-y-2">
          <Label htmlFor="code">Code Snippet</Label>
          <CodeEditor
            value={code}
            onChange={setCode}
            language={languageSelected}
            placeholder="Paste your code here..."
            minHeight="200px"
            required
          />
        </div>

        <Button
          type="submit"
          disabled={mutation.isPending || !languageSelected || !code}
          className="w-full"
        >
          {mutation.isPending ? (
            <>🔄 Submitting Review...</>
          ) : (
            <>📤 Submit for Review</>
          )}
        </Button>
      </form>
    </div>
  );
}
