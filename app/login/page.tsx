"use client";
import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import { useAuth } from "app/context/AuthContext";
import { toast } from "sonner";
import { Loader2, Activity } from "lucide-react";


export default function LoginPage() {
  const { login } = useAuth();
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);

    try {
      if (!formData.email || !formData.password) {
        toast.error("Email and password are required");
        return;
      }

      // Execute login
      await login(formData.email, formData.password);
      toast.success("Welcome back!");
      router.push("/dashboard");
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : "Invalid credentials";
      toast.error(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full min-h-screen lg:grid lg:grid-cols-2 font-sans">
      
      {/* ---------------- LEFT SIDE: THE FORM (Clean White) ---------------- */}
      <div className="flex items-center justify-center py-12 px-4 sm:px-12 bg-white">
        <div className="mx-auto grid w-full max-w-md gap-6">
          
          {/* Mobile-only Logo */}
          <div className="lg:hidden flex items-center gap-2 mb-4 text-slate-900">
             <div className="h-8 w-8 bg-[#6366f1] rounded-lg flex items-center justify-center">
                <Activity className="w-5 h-5 text-white" />
             </div>
             <span className="font-bold text-xl tracking-tight">ThinkFit</span>
          </div>

          <Link href="/" className="mb-4 text-sm font-medium text-slate-500 hover:text-indigo-600 transition-colors">
            &larr; Back to home
          </Link>

          <div className="grid gap-2 text-left">
            <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Welcome back</h1>
            <p className="text-slate-500 text-sm">
              Enter your credentials to access your dashboard.
            </p>
          </div>

          <form onSubmit={handleSubmit} className="mt-4">
            <div className="flex flex-col gap-5">

              {/* Email */}
              <LabelInputContainer>
                <Label className="text-sm font-medium text-slate-700" htmlFor="email">Email</Label>
                <Input
                  id="email"
                  placeholder="athlete@example.com"
                  type="email"
                  className="text-slate-900"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  required
                  disabled={loading}
                />
              </LabelInputContainer>

              {/* Password */}
              <LabelInputContainer>
                <div className="flex items-center justify-between">
                  <Label className="text-sm font-medium text-slate-700" htmlFor="password">Password</Label>
                  <Link href="/forgot-password" className="text-xs text-indigo-600 font-medium hover:underline">
                    Forgot password?
                  </Link>
                </div>
                <Input
                  id="password"
                  placeholder="••••••••"
                  type="password"
                  className="text-slate-900"
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  required
                  disabled={loading}
                />
              </LabelInputContainer>

              {/* MAIN ACTION BUTTON */}
              <button
                className="group/btn relative mt-4 block h-11 w-full rounded-xl bg-slate-900 font-semibold text-white shadow-[0px_1px_0px_0px_#ffffff40_inset,0px_-1px_0px_0px_#ffffff40_inset] hover:bg-slate-800 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                type="submit"
                disabled={loading}
              >
                {loading ? (
                  <span className="flex items-center justify-center">
                    <Loader2 className="w-4 h-4 mr-2 animate-spin"/>
                    Logging in...
                  </span>
                ) : (
                  <>
                    Log in &rarr;
                    <BottomGradient />
                  </>
                )}
              </button>

            </div>
          </form>

          <div className="mt-4 text-center text-sm text-slate-600">
            Don't have an account?{" "}
            <Link href="/signup" className="font-semibold text-indigo-600 underline-offset-4 hover:underline">
              Sign up
            </Link>
          </div>
        </div>
      </div>

      {/* ---------------- RIGHT SIDE: VISUAL PANEL ---------------- */}
      <div
        className="hidden lg:flex flex-col justify-between p-12 text-white relative overflow-hidden bg-cover bg-center"
        style={{ backgroundImage: "url('/uploads/login.jpg')" }} 
      >
        {/* Dark Overlay */}
        <div className="absolute inset-0 bg-slate-950/35" />

        {/* Branding Top Left */}
        <div className="relative z-10 flex items-center gap-2 text-lg font-bold tracking-tight">
          <div className="h-8 w-8 bg-indigo-500 rounded-lg flex items-center justify-center shadow-lg">
            <Activity className="w-5 h-5 text-white" />
          </div>
          ThinkFit
        </div>

        {/* Hero Text */}
        <div className="relative z-10 mt-auto max-w-md">
          <blockquote className="space-y-2">
            <p className="text-xl font-medium leading-relaxed tracking-wide">
              &ldquo;Consistency is key. Log in to keep your streaks alive and stay on top of your daily targets.&rdquo;
            </p>
          </blockquote>
        </div>

        {/* Soft Glow */}
        <div className="absolute bottom-[-150px] right-[-150px] w-[400px] h-[400px] bg-cyan-500/30 rounded-full blur-[120px]" />
      </div>
    </div>
  );
}

// --- Internal Helper Components ---
const BottomGradient = () => {
  return (
    <>
      <span className="absolute inset-x-0 -bottom-px block h-px w-full bg-gradient-to-r from-transparent via-indigo-500 to-transparent opacity-0 transition duration-500 group-hover/btn:opacity-100" />
      <span className="absolute inset-x-10 -bottom-px mx-auto block h-px w-1/2 bg-gradient-to-r from-transparent via-cyan-500 to-transparent opacity-0 blur-sm transition duration-500 group-hover/btn:opacity-100" />
    </>
  );
};

const LabelInputContainer = ({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) => {
  return (
    <div className={cn("flex w-full flex-col space-y-1.5", className)}>
      {children}
    </div>
  );
};