"use client"

import type * as React from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import { useLanguage } from "@/lib/hooks/use-language"
import { Button } from "@/components/ui/button"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { Menu } from "lucide-react"
import { LayoutDashboard, Users, Dumbbell, CreditCard, Tag, Key, ShoppingBag, FileText, Settings } from "lucide-react"

const navItems = [
  { href: "/dashboard", label: "dashboard.overview", icon: LayoutDashboard },
  { href: "/dashboard/members", label: "members.title", icon: Users },
  { href: "/dashboard/classes", label: "classes.title", icon: Dumbbell },
  { href: "/dashboard/payments", label: "payments.title", icon: CreditCard },
  { href: "/dashboard/promotions", label: "promotions.title", icon: Tag },
  { href: "/dashboard/access-control", label: "accessControl.title", icon: Key },
  { href: "/dashboard/staff", label: "staff.title", icon: Users },
  { href: "/dashboard/store", label: "store.title", icon: ShoppingBag },
  { href: "/dashboard/reports", label: "reports.title", icon: FileText },
  { href: "/dashboard/gym-settings", label: "gymSettings.title", icon: Settings },
]

export function MainNav({ className, ...props }: React.HTMLAttributes<HTMLElement>) {
  const { t } = useLanguage()
  const pathname = usePathname()

  const mainItems = navItems.slice(0, 5) // First 5 items always visible
  const moreItems = navItems.slice(5) // Remaining items in dropdown

  return (
    <nav className={cn("flex items-center space-x-4 lg:space-x-6", className)} {...props}>
      {mainItems.map((item) => (
        <Link
          key={item.href}
          href={item.href}
          className={cn(
            "flex items-center text-sm font-medium transition-colors hover:text-orange-500",
            pathname === item.href ? "text-orange-500" : "text-muted-foreground",
          )}
        >
          <item.icon className="mr-2 h-4 w-4" />
          <span className="hidden md:inline">{t(item.label)}</span>
        </Link>
      ))}

      {/* More dropdown for larger screens */}
      <DropdownMenu>
        <DropdownMenuTrigger asChild className="hidden md:inline-flex">
          <Button variant="ghost" className="text-sm font-medium">
            More
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent>
          {moreItems.map((item) => (
            <DropdownMenuItem key={item.href} asChild>
              <Link
                href={item.href}
                className={cn(
                  "flex items-center",
                  pathname === item.href ? "text-orange-500" : "text-muted-foreground",
                )}
              >
                <item.icon className="mr-2 h-4 w-4" />
                {t(item.label)}
              </Link>
            </DropdownMenuItem>
          ))}
        </DropdownMenuContent>
      </DropdownMenu>

      {/* Mobile menu */}
      <DropdownMenu>
        <DropdownMenuTrigger asChild className="md:hidden">
          <Button variant="ghost" size="icon">
            <Menu className="h-5 w-5" />
            <span className="sr-only">Toggle menu</span>
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end" className="w-[200px]">
          {navItems.map((item) => (
            <DropdownMenuItem key={item.href} asChild>
              <Link
                href={item.href}
                className={cn(
                  "flex items-center",
                  pathname === item.href ? "text-orange-500" : "text-muted-foreground",
                )}
              >
                <item.icon className="mr-2 h-4 w-4" />
                {t(item.label)}
              </Link>
            </DropdownMenuItem>
          ))}
        </DropdownMenuContent>
      </DropdownMenu>
    </nav>
  )
}

