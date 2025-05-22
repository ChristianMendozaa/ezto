"use client"

import { Table, TableBody, TableCaption, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { useLanguage } from "@/lib/hooks/use-language"

const reportData = [
  { month: "January", newMembers: 25, totalRevenue: 15000, avgAttendance: 150 },
  { month: "February", newMembers: 30, totalRevenue: 18000, avgAttendance: 165 },
  { month: "March", newMembers: 35, totalRevenue: 22000, avgAttendance: 180 },
  { month: "April", newMembers: 40, totalRevenue: 25000, avgAttendance: 200 },
  { month: "May", newMembers: 45, totalRevenue: 28000, avgAttendance: 220 },
  { month: "June", newMembers: 50, totalRevenue: 32000, avgAttendance: 240 },
]

export function Reports() {
  const { t } = useLanguage()

  return (
    <Table>
      <TableCaption>{t("dashboard.reportsSection.title")}</TableCaption>
      <TableHeader>
        <TableRow>
          <TableHead>{t("dashboard.reportsSection.columns.month")}</TableHead>
          <TableHead>{t("dashboard.reportsSection.columns.newMembers")}</TableHead>
          <TableHead>{t("dashboard.reportsSection.columns.totalRevenue")}</TableHead>
          <TableHead>{t("dashboard.reportsSection.columns.avgAttendance")}</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {reportData.map((row) => (
          <TableRow key={row.month}>
            <TableCell>{row.month}</TableCell>
            <TableCell>{row.newMembers}</TableCell>
            <TableCell>${row.totalRevenue.toLocaleString()}</TableCell>
            <TableCell>{row.avgAttendance}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}

