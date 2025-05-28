"use client"

import { useState } from "react"
import { useLanguage } from "@/lib/hooks/use-language"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { useAccessLogs } from "@/hooks/useAccessLogs"
import { useAccessAlerts } from "@/hooks/useAccessAlerts"
import { AlertTriangle, Trash2 } from "lucide-react"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { format } from "date-fns"
import { es } from "date-fns/locale"

export default function AccessControlPage() {
  const { t } = useLanguage()
  const [activeTab, setActiveTab] = useState("access-logs")
  const { logs: accessLogs, loading: loadingLogs } = useAccessLogs()
  const { alerts, loading: loadingAlerts } = useAccessAlerts()

  return (
    <div className="flex-1 space-y-4 p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">{t("accessControl.title")}</h2>
      </div>
      <Tabs defaultValue="access-logs" className="space-y-4">
        <TabsList>
          <TabsTrigger value="access-logs" onClick={() => setActiveTab("access-logs")}>
            {t("accessControl.tabs.accessLogs")}
          </TabsTrigger>
          <TabsTrigger value="alerts" onClick={() => setActiveTab("alerts")}>
            {t("accessControl.tabs.alerts")}
          </TabsTrigger>
        </TabsList>

        <TabsContent value="access-logs" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>{t("accessControl.accessLogs.title")}</CardTitle>
            </CardHeader>
            <CardContent>
              {loadingLogs ? (
                <p>{t("loading")}</p>
              ) : (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>{t("accessControl.accessLogs.table.name")}</TableHead>
                      <TableHead>{t("accessControl.accessLogs.table.timestamp")}</TableHead>
                      <TableHead>{t("accessControl.accessLogs.table.status")}</TableHead>
                      <TableHead>{t("accessControl.nfcDevices.table.type")}</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {accessLogs.map((log, index) => (
                      <TableRow key={index}>
                        <TableCell className="font-medium">{log.name}</TableCell>
                        <TableCell>{format(new Date(log.timestamp), "dd MMM yyyy, HH:mm", { locale: es })}</TableCell>
                        <TableCell>
                          <Badge variant={log.status === "granted" ? "success" : "destructive"}>
                            {t(`accessControl.accessLogs.status.${log.status}`)}
                          </Badge>
                        </TableCell>
                        <TableCell>{log.device_type}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="alerts" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>{t("accessControl.alerts.title")}</CardTitle>
            </CardHeader>
            <CardContent>
              {loadingAlerts ? (
                <p>{t("loading")}</p>
              ) : (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>{t("accessControl.alerts.table.name")}</TableHead>
                      <TableHead>{t("accessControl.alerts.table.type")}</TableHead>
                      <TableHead>{t("accessControl.alerts.table.location")}</TableHead>
                      <TableHead>{t("accessControl.alerts.table.timestamp")}</TableHead>
                      <TableHead className="text-right">{t("accessControl.alerts.table.actions")}</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {alerts.map((alert, index) => (
                      <TableRow key={index}>
                        <TableCell className="font-medium">{alert.name}</TableCell>
                        <TableCell>{alert.type}</TableCell>
                        <TableCell>{alert.location}</TableCell>
                        <TableCell>{format(new Date(alert.timestamp), "dd MMM yyyy, HH:mm", { locale: es })}</TableCell>
                        <TableCell className="text-right">
                          <DropdownMenu>
                            <DropdownMenuTrigger asChild>
                              <Button variant="ghost" className="h-8 w-8 p-0">
                                <span className="sr-only">{t("accessControl.alerts.actions.open")}</span>
                                <AlertTriangle className="h-4 w-4" />
                              </Button>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent align="end">
                              <DropdownMenuLabel>{t("accessControl.alerts.actions.title")}</DropdownMenuLabel>
                              <DropdownMenuItem>
                                <AlertTriangle className="mr-2 h-4 w-4" />
                                {t("accessControl.alerts.actions.investigate")}
                              </DropdownMenuItem>
                              <DropdownMenuItem>
                                <Trash2 className="mr-2 h-4 w-4" />
                                {t("accessControl.alerts.actions.dismiss")}
                              </DropdownMenuItem>
                            </DropdownMenuContent>
                          </DropdownMenu>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}