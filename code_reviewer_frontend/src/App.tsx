import { ProtectedRoute } from "@/components/ProtectedRoute";
import { Toaster } from "@/components/ui/sonner";
import { MainDashboard } from "@/pages/MainDashboard";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient();

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ProtectedRoute>
        <MainDashboard />
      </ProtectedRoute>
      <Toaster />
    </QueryClientProvider>
  );
}
