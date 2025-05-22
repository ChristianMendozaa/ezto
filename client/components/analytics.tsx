"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { useLanguage } from "@/lib/hooks/use-language"
import { Bar, BarChart, Line, LineChart, ResponsiveContainer, XAxis, YAxis } from "recharts"

const membershipData = [
  { month: "Jan", members: 100 },
  { month: "Feb", members: 120 },
  { month: "Mar", members: 150 },
  { month: "Apr", members: 180 },
  { month: "May", members: 220 },
  { month: "Jun", members: 250 },
]

const revenueData = [
  { month: "Jan", revenue: 5000 },
  { month: "Feb", revenue: 6000 },
  { month: "Mar", revenue: 7500 },
  { month: "Apr", revenue: 9000 },
  { month: "May", revenue: 11000 },
  { month: "Jun", revenue: 12500 },
]

const classAttendanceData = [
  { class: "Yoga", attendance: 50 },
  { class: "Spinning", attendance: 40 },
  { class: "Zumba", attendance: 35 },
  { class: "Pilates", attendance: 30 },
  { class: "Boxing", attendance: 25 },
]

const peakHoursData = [
  { hour: "6AM", visitors: 10 },
  { hour: "8AM", visitors: 30 },
  { hour: "10AM", visitors: 20 },
  { hour: "12PM", visitors: 15 },
  { hour: "2PM", visitors: 25 },
  { hour: "4PM", visitors: 40 },
  { hour: "6PM", visitors: 50 },
  { hour: "8PM", visitors: 35 },
]

export function Analytics() {
  const { t } = useLanguage()

  return (
    <div className="grid gap-4 md:grid-cols-2">
      <Card>
        <CardHeader>
          <CardTitle>{t("dashboard.analyticsSection.membershipGrowth")}</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={membershipData}>
              <XAxis dataKey="month" />
              <YAxis />
              <Line type="monotone" dataKey="members" stroke="#8884d8" />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>{t("dashboard.analyticsSection.revenueOverTime")}</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={revenueData}>
              <XAxis dataKey="month" />
              <YAxis />
              <Line type="monotone" dataKey="revenue" stroke="#82ca9d" />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>{t("dashboard.analyticsSection.classAttendance")}</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={classAttendanceData}>
              <XAxis dataKey="class" />
              <YAxis />
              <Bar dataKey="attendance" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>{t("dashboard.analyticsSection.peakHours")}</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={peakHoursData}>
              <XAxis dataKey="hour" />
              <YAxis />
              <Bar dataKey="visitors" fill="#82ca9d" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  )
}

