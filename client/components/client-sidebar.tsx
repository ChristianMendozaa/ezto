"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import { useLanguage } from "@/lib/hooks/use-language"
import { useTheme } from "@/lib/hooks/use-theme"
import {
  LayoutDashboard,
  UserCircle,
  Calendar,
  Dumbbell,
  CreditCard,
  MessageSquare,
  LogOut,
  Moon,
  Sun,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
  SidebarTrigger,
  useSidebar,
} from "@/components/ui/sidebar"

const sidebarItems = [
  { href: "/client", icon: LayoutDashboard, label: "client.dashboardTitle" },
  { href: "/client/profile", icon: UserCircle, label: "client.profileTitle" },
  { href: "/client/schedule", icon: Calendar, label: "client.schedule" },
  { href: "/client/classes", icon: Dumbbell, label: "client.classes" },
  { href: "/client/payments", icon: CreditCard, label: "client.payments" },
  { href: "/client/support", icon: MessageSquare, label: "client.support" },
]

export function ClientSidebar() {
  const pathname = usePathname()
  const { t, language, setLanguage } = useLanguage()
  const { theme, toggleTheme } = useTheme()
  const { state } = useSidebar()

  return (
    <Sidebar collapsible="icon">
      <SidebarHeader>
        <div className="flex items-center justify-between h-16 px-4 border-b border-gray-200 dark:border-gray-700">
          <img className="w-auto h-8" src="/logo.svg" alt="EzTo" />
          <SidebarTrigger />
        </div>
      </SidebarHeader>
      
      <SidebarContent>
        <SidebarMenu>
          {sidebarItems.map((item) => (
            <SidebarMenuItem key={item.href}>
              <SidebarMenuButton asChild tooltip={state === "collapsed" ? String(t(item.label)) : undefined}>
                <Link
                  href={item.href}
                  className={cn(
                    "flex items-center gap-3 rounded-lg transition-all hover:text-primary",
                    pathname === item.href ? "bg-muted text-primary" : "text-muted-foreground",
                    state === "collapsed" ? "h-9 w-9 justify-center p-0" : "px-3 py-2",
                    "relative",
                  )}
                >
                  <item.icon
                    className={cn(
                      "h-4 w-4 shrink-0",
                      state === "collapsed" && "absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2",
                    )}
                  />
                  {state !== "collapsed" && <span className="truncate">{String(t(item.label))}</span>}
                </Link>
              </SidebarMenuButton>
            </SidebarMenuItem>
          ))}
        </SidebarMenu>
      </SidebarContent>
      
      <SidebarFooter>
        <div className={cn("flex items-center gap-2 mb-2", state === "collapsed" ? "flex-col" : "justify-between")}>
          <Button variant="ghost" size="icon" onClick={toggleTheme} className="w-9 h-9 shrink-0 relative">
            {theme === "dark" ? (
              <Sun className="h-4 w-4 absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2" />
            ) : (
              <Moon className="h-4 w-4 absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2" />
            )}
          </Button>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setLanguage(language === "en" ? "es" : "en")}
            className="w-9 h-9 shrink-0 relative"
          >
            <span className="font-bold text-sm absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2">
              {language.toUpperCase()}
            </span>
          </Button>
        </div>
        
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button
              variant="ghost"
              className={cn("h-9 relative", state === "collapsed" ? "w-9 p-0" : "w-full justify-start px-3")}
            >
              <Avatar className="h-5 w-5 shrink-0">
                <AvatarImage src="/avatars/01.png" alt="@usuario" />
                <AvatarFallback>CL</AvatarFallback>
              </Avatar>
              {state !== "collapsed" && <span className="ml-2">{String(t("client.name"))}</span>}
            </Button>
          </DropdownMenuTrigger>
          
          <DropdownMenuContent align="end" className="w-56">
            <DropdownMenuLabel>{String(t("common.profile"))}</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem>
              <Link href="/client/profile" className="flex items-center w-full">
                {String(t("common.settings"))}
              </Link>
            </DropdownMenuItem>
            <DropdownMenuItem>
              <Link href="/logout" className="flex items-center w-full">
                <LogOut className="mr-2 h-4 w-4" />
                <span>{String(t("common.logout"))}</span>
              </Link>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </SidebarFooter>
    </Sidebar>
  )
}
