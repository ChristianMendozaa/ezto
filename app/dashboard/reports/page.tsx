"use client"

import { useState } from "react"
import { useLanguage } from "@/lib/hooks/use-language"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { MainNav } from "@/components/main-nav"
import { UserNav } from "@/components/user-nav"
import { Search, Download, FileText } from "lucide-react"
import { ThemeToggle } from "@/components/theme-toggle"
import { LanguageToggle } from "@/components/language-toggle"

// Mock data for reports
const reports = [
  { id: 1, name: "Monthly Financial Report", type: "financial", dateGenerated: "2023-07-01" },
  { id: 2, name: "Weekly Attendance Summary", type: "attendance", dateGenerated: "2023-07-07" },
  { id: 3, name: "Quarterly Membership Overview", type: "membership", dateGenerated: "2023-06-30" },
  { id: 4, name: "Annual Revenue Report", type: "financial", dateGenerated: "2023-01-01" },
  { id: 5, name: "Monthly New Members Report", type: "membership", dateGenerated: "2023-07-01" },
]

export default function ReportsPage() {
  const { t } = useLanguage()
  const [timeRange, setTimeRange] = useState("monthly")
  const [reportType, setReportType] = useState("financial")

  return (
    <div className="hidden flex-col md:flex">
      <div className="border-b">
        <div className="flex h-16 items-center px-4">
          <MainNav className="mx-6" />
          <div className="ml-auto flex items-center space-x-4">
            <LanguageToggle />
            <ThemeToggle />
            <UserNav />
          </div>
        </div>
      </div>
      <div className="flex-1 space-y-4 p-8 pt-6">
        <div className="flex items-center justify-between space-y-2">
          <h2 className="text-3xl font-bold tracking-tight">{t("reports.title")}</h2>
          <div className="flex items-center space-x-2">
            <Button>
              <FileText className="mr-2 h-4 w-4" />
              {t("reports.generate")}
            </Button>
          </div>
        </div>
        <div className="flex flex-col space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>{t("reports.title")}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex justify-between mb-4">
                <div className="flex space-x-2">
                  <Select value={timeRange} onValueChange={setTimeRange}>
                    <SelectTrigger className="w-[180px]">
                      <SelectValue placeholder={t("reports.timeRange.label")} />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="daily">{t("reports.timeRange.daily")}</SelectItem>
                      <SelectItem value="weekly">{t("reports.timeRange.weekly")}</SelectItem>
                      <SelectItem value="monthly">{t("reports.timeRange.monthly")}</SelectItem>
                      <SelectItem value="yearly">{t("reports.timeRange.yearly")}</SelectItem>
                    </SelectContent>
                  </Select>
                  <Select value={reportType} onValueChange={setReportType}>
                    <SelectTrigger className="w-[180px]">
                      <SelectValue placeholder={t("reports.type.label")} />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="financial">{t("reports.type.financial")}</SelectItem>
                      <SelectItem value="attendance">{t("reports.type.attendance")}</SelectItem>
                      <SelectItem value="membership">{t("reports.type.membership")}</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="flex w-full max-w-sm items-center space-x-2">
                  <Input placeholder={t("common.search")} className="w-[300px]" />
                  <Button type="submit" size="icon">
                    <Search className="h-4 w-4" />
                  </Button>
                </div>
              </div>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>{t("reports.table.name")}</TableHead>
                    <TableHead>{t("reports.table.type")}</TableHead>
                    <TableHead>{t("reports.table.dateGenerated")}</TableHead>
                    <TableHead className="text-right">{t("reports.table.actions")}</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {reports.map((report) => (
                    <TableRow key={report.id}>
                      <TableCell className="font-medium">{report.name}</TableCell>
                      <TableCell>{t(`reports.type.${report.type}`)}</TableCell>
                      <TableCell>{report.dateGenerated}</TableCell>
                      <TableCell className="text-right">
                        <Button variant="ghost" size="icon">
                          <Download className="h-4 w-4" />
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

