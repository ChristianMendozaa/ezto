import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import { useLanguage } from "@/lib/hooks/use-language"
import type React from "react"

export function MainNav({ className, ...props }: React.HTMLAttributes<HTMLElement>) {
  const { t } = useLanguage()
  const pathname = usePathname()

  return (
    <nav className={cn("flex items-center space-x-4 lg:space-x-6", className)} {...props}>
      <Link
        href="/dashboard"
        className={cn(
          "text-sm font-medium transition-colors hover:text-orange-500",
          pathname === "/dashboard" ? "text-orange-500" : "text-muted-foreground",
        )}
      >
        {t("dashboard.overview")}
      </Link>
      <Link
        href="/dashboard/members"
        className={cn(
          "text-sm font-medium transition-colors hover:text-orange-500",
          pathname === "/dashboard/members" ? "text-orange-500" : "text-muted-foreground",
        )}
      >
        {t("members.title")}
      </Link>
      <Link
        href="/dashboard/classes"
        className={cn(
          "text-sm font-medium transition-colors hover:text-orange-500",
          pathname === "/dashboard/classes" ? "text-orange-500" : "text-muted-foreground",
        )}
      >
        {t("classes.title")}
      </Link>
      <Link
        href="/dashboard/payments"
        className={cn(
          "text-sm font-medium transition-colors hover:text-orange-500",
          pathname === "/dashboard/payments" ? "text-orange-500" : "text-muted-foreground",
        )}
      >
        {t("payments.title")}
      </Link>
      <Link
        href="/dashboard/reports"
        className={cn(
          "text-sm font-medium transition-colors hover:text-orange-500",
          pathname === "/dashboard/reports" ? "text-orange-500" : "text-muted-foreground",
        )}
      >
        {t("reports.title")}
      </Link>
    </nav>
  )
}

