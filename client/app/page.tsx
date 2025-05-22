"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { useLanguage } from "@/lib/hooks/use-language"
import { Dumbbell, Calendar, CreditCard } from "lucide-react"

export default function ClientDashboard() {
  const { t } = useLanguage()

  return (
    <div className="space-y-4">
      <h1 className="text-3xl font-bold">{t("client.dashboard.welcome")}</h1>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">{t("client.dashboard.nextClass")}</CardTitle>
            <Dumbbell className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{t("client.dashboard.yogaClass")}</div>
            <p className="text-xs text-muted-foreground">{t("client.dashboard.today")} 18:00</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">{t("client.dashboard.monthlyClasses")}</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">12/20</div>
            <p className="text-xs text-muted-foreground">{t("client.dashboard.classesRemaining")}</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">{t("client.dashboard.membershipStatus")}</CardTitle>
            <CreditCard className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{t("client.dashboard.active")}</div>
            <p className="text-xs text-muted-foreground">{t("client.dashboard.renewalDate")} 2023-12-31</p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

