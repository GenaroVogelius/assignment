import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useRegisterUser } from "@/hooks/useRegisterUser";
import { Eye, EyeOff, Loader2 } from "lucide-react";
import React, { useState } from "react";
import { AuthHeader } from "../components/AuthHeader/AuthHeader";

export const CreateAccountForm: React.FC = () => {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const registerUserMutation = useRegisterUser();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (!email || !password || !username) {
      setError("Please fill in all fields");
      return;
    }

    try {
      await registerUserMutation.mutateAsync({
        username,
        email,
        password,
      });
      setSuccess("Account created successfully!");
      // Reset form
      setEmail("");
      setUsername("");
      setPassword("");
    } catch (error) {
      setError(
        error instanceof Error ? error.message : "Failed to create account"
      );
    }
  };

  return (
    <>
      <AuthHeader
        title="Create Your Account"
        description="Join CodeReview Pro and start reviewing code like a pro"
      />
      <CardContent className="px-0">
        <form onSubmit={handleSubmit} className="space-y-6">
          {error && (
            <Alert variant="destructive" className="border-red-200 bg-red-50">
              <AlertDescription className="text-red-800">
                {error}
              </AlertDescription>
            </Alert>
          )}

          {success && (
            <Alert className="border-green-200 bg-green-50">
              <AlertDescription className="text-green-800">
                {success}
              </AlertDescription>
            </Alert>
          )}

          <div className="space-y-3">
            <Label
              htmlFor="email"
              className="text-sm font-semibold text-slate-700"
            >
              Email
            </Label>
            <Input
              id="email"
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={registerUserMutation.isPending}
              required
              className="h-12 border-slate-200 transition-all duration-200"
            />
          </div>

          <div className="space-y-3">
            <Label
              htmlFor="username"
              className="text-sm font-semibold text-slate-700"
            >
              Username
            </Label>
            <Input
              id="username"
              type="username"
              placeholder="Enter your username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              disabled={registerUserMutation.isPending}
              required
              className="h-12 border-slate-200 transition-all duration-200"
            />
          </div>

          <div className="space-y-3">
            <Label
              htmlFor="password"
              className="text-sm font-semibold text-slate-700"
            >
              Password
            </Label>
            <div className="relative">
              <Input
                id="password"
                type={showPassword ? "text" : "password"}
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={registerUserMutation.isPending}
                required
                className="h-12 border-slate-200 transition-all duration-200 pr-12"
              />
              <Button
                type="button"
                variant="ghost"
                size="sm"
                className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent text-slate-400 hover:text-slate-600"
                onClick={() => setShowPassword(!showPassword)}
                disabled={registerUserMutation.isPending}
              >
                {showPassword ? (
                  <EyeOff className="h-4 w-4" />
                ) : (
                  <Eye className="h-4 w-4" />
                )}
              </Button>
            </div>
          </div>

          <Button
            type="submit"
            className="w-full h-12 text-white font-semibold shadow-lg transition-all duration-200"
            disabled={registerUserMutation.isPending}
          >
            {registerUserMutation.isPending ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Creating account...
              </>
            ) : (
              "Create Account"
            )}
          </Button>
        </form>
      </CardContent>
    </>
  );
};
