"use client";
import { MainNav } from "@/components/main-nav";
import { UserNav } from "@/components/user-nav";
import { ThemeToggle } from "@/components/theme-toggle";
import { LanguageToggle } from "@/components/language-toggle";
import { useAuth } from "@/lib/auth-context";
import type React from "react";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();
  const router = useRouter();
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  useEffect(() => {
    if (isMounted && !loading && (!user || user.role !== "gym_owner")) {
      router.replace("/login");
    }
  }, [user, loading, router, isMounted]);

  if (!isMounted || loading) return <p>Cargando...</p>;

  return (
    <div className="flex flex-col min-h-screen">
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center">
          <MainNav className="mx-6" />
          <div className="ml-auto flex items-center space-x-4">
            <LanguageToggle />
            <ThemeToggle />
            <UserNav />
          </div>
        </div>
      </header>
      <main className="flex-1 container mx-auto py-6">{children}</main>
    </div>
  );
}
