import { useLogoutUser } from "@/hooks/useLogoutUser";
import { useAuthStore } from "@/stores/authStore";
import { LogOut, User } from "lucide-react";
import { Button } from "../ui/button";

export function Header() {
  const { tokens } = useAuthStore();
  const logoutUserMutation = useLogoutUser();


  console.log(tokens);


  const handleLogout = async () => {
    if (tokens?.access_token) {
      try {
        await logoutUserMutation.mutateAsync(tokens.access_token);
      } catch (error) {
        console.error("Logout error:", error);
        // The hook will still clear local state even if API call fails
      }
    }
  };

  return (
    <header className="border-b bg-card">
      <div className="container mx-auto px-4 py-4 md:py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="hidden md:flex h-10 w-10 items-center justify-center rounded-lg bg-primary text-primary-foreground">
              <span className=" text-lg font-bold">CR</span>
            </div>
            <div>
              <h1 className="text-2xl font-bold text-foreground">
                CodeReview Pro
              </h1>
              <p className="text-sm text-muted-foreground">
                Automated code review and analysis platform
              </p>
            </div>
          </div>

          <div className="flex flex-col md:flex-row items-center gap-4">
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <User className="hidden md:block h-4 w-4" />
              <span className="pt-4 md:p-0 text-center">
                Welcome {tokens?.username}
              </span>
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={handleLogout}
              disabled={logoutUserMutation.isPending}
              className="flex items-center gap-2"
            >
              <LogOut className="h-4 w-4" />
              {logoutUserMutation.isPending ? "Logging out..." : "Logout"}
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
}
