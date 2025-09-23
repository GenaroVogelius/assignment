import { SectionsTabs } from "@/components/SectionsTabs/SectionsTabs";
import { Card, CardHeader } from "@/components/ui/card";
import { Tabs, TabsContent } from "@/components/ui/tabs";
import { CreateAccountForm } from "@/features/auth/CreateAccountForm/CreateAccountForm";
import { LogAccountForm } from "@/features/auth/LogAccountForm/LogAccountForm";
export function Authentication() {
  const sections = [
    { value: "login", title: "Login" },
    { value: "register", title: "Register" },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 flex items-center justify-center p-4 relative overflow-hidden">
      <div className="relative z-10 w-full max-w-md">
        <Tabs defaultValue="login" className="w-full">
          <Card className="w-full">
            <CardHeader className="text-center pb-6">
              <SectionsTabs sections={sections} />
            </CardHeader>
            <TabsContent value="login" className="px-6 pb-6">
              <LogAccountForm />
            </TabsContent>
            <TabsContent value="register" className="px-6 pb-6">
              <CreateAccountForm />
            </TabsContent>
          </Card>
        </Tabs>
      </div>
    </div>
  );
}
