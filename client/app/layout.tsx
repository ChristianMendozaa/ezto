"use client";
import { ClientSidebar } from "@/components/client-sidebar";
import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar";
import type React from "react";
import { useAuth } from "@/lib/auth-context";
import { useEffect } from "react";
import { useRouter } from "next/navigation";

function ClientContent({ children }: { children: React.ReactNode }) {
  return (
    <SidebarInset className="flex-1 overflow-hidden">
      <main className="flex-1 overflow-y-auto p-4 md:p-6 lg:p-8">{children}</main>
    </SidebarInset>
  );
}

export default function ClientLayout({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && (!user || user.role !== "gym_member")) {
      router.replace("/login");
    }
  }, [user, loading, router]);

  if (loading || !user) return <p>Cargando...</p>;

  return (
    <SidebarProvider>
      <div className="flex h-screen overflow-hidden">
        <ClientSidebar />
        <ClientContent>{children}</ClientContent>
      </div>
    </SidebarProvider>
  );
}
