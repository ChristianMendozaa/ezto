import { ClientSidebar } from "@/components/client-sidebar"
import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar"
import type React from "react"

function ClientContent({ children }: { children: React.ReactNode }) {
  return (
    <SidebarInset className="flex-1 overflow-hidden">
      <main className="flex-1 overflow-y-auto p-4 md:p-6 lg:p-8">{children}</main>
    </SidebarInset>
  )
}

export default function ClientLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <SidebarProvider>
      <div className="flex h-screen overflow-hidden">
        <ClientSidebar />
        <ClientContent>{children}</ClientContent>
      </div>
    </SidebarProvider>
  )
}

