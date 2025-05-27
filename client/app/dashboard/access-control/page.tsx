"use client"

import { useState } from "react"
import { useLanguage } from "@/lib/hooks/use-language"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { Search, Plus, MoreHorizontal, Edit, Trash2, AlertTriangle, UserCheck } from "lucide-react"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

// Mock data for access logs
const accessLogs = [
  {
    id: 1,
    name: "John Doe",
    type: "Member",
    accessPoint: "Main Entrance",
    timestamp: "2023-07-10 08:30:15",
    status: "granted",
  },
  {
    id: 2,
    name: "Jane Smith",
    type: "Employee",
    accessPoint: "Staff Room",
    timestamp: "2023-07-10 09:15:22",
    status: "granted",
  },
  {
    id: 3,
    name: "Mike Johnson",
    type: "Member",
    accessPoint: "Gym Area",
    timestamp: "2023-07-10 10:05:47",
    status: "denied",
  },
  {
    id: 4,
    name: "Sarah Williams",
    type: "Member",
    accessPoint: "Pool",
    timestamp: "2023-07-10 11:30:03",
    status: "granted",
  },
  {
    id: 5,
    name: "Tom Brown",
    type: "Employee",
    accessPoint: "Main Entrance",
    timestamp: "2023-07-10 12:45:39",
    status: "granted",
  },
]

// Mock data for NFC devices
const nfcDevices = [
  { id: 1, name: "John Doe", type: "Card", nfcId: "A1B2C3D4", status: "active" },
  { id: 2, name: "Jane Smith", type: "Wristband", nfcId: "E5F6G7H8", status: "active" },
  { id: 3, name: "Mike Johnson", type: "Card", nfcId: "I9J0K1L2", status: "inactive" },
  { id: 4, name: "Sarah Williams", type: "Wristband", nfcId: "M3N4O5P6", status: "active" },
  { id: 5, name: "Tom Brown", type: "Card", nfcId: "Q7R8S9T0", status: "active" },
]

// Mock data for alerts
const alerts = [
  {
    id: 1,
    name: "John Doe",
    type: "Unauthorized Access Attempt",
    location: "Staff Room",
    timestamp: "2023-07-10 14:30:15",
  },
  {
    id: 2,
    name: "Unknown",
    type: "Multiple Failed Attempts",
    location: "Main Entrance",
    timestamp: "2023-07-10 16:45:22",
  },
  { id: 3, name: "Mike Johnson", type: "Access Outside Hours", location: "Gym Area", timestamp: "2023-07-10 22:05:47" },
]

export default function AccessControlPage() {
  const { t } = useLanguage()
  const [activeTab, setActiveTab] = useState("access-logs")
  const [isAddNFCOpen, setIsAddNFCOpen] = useState(false)

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
          <TabsTrigger value="nfc-devices" onClick={() => setActiveTab("nfc-devices")}>
            {t("accessControl.tabs.nfcDevices")}
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
              <div className="flex justify-between mb-4">
                <div className="flex w-full max-w-sm items-center space-x-2">
                  <Input placeholder={t("accessControl.search")} className="w-[300px]" />
                  <Button type="submit" size="icon">
                    <Search className="h-4 w-4" />
                  </Button>
                </div>
              </div>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>{t("accessControl.accessLogs.table.name")}</TableHead>
                    <TableHead>{t("accessControl.accessLogs.table.type")}</TableHead>
                    <TableHead>{t("accessControl.accessLogs.table.accessPoint")}</TableHead>
                    <TableHead>{t("accessControl.accessLogs.table.timestamp")}</TableHead>
                    <TableHead>{t("accessControl.accessLogs.table.status")}</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {accessLogs.map((log) => (
                    <TableRow key={log.id}>
                      <TableCell className="font-medium">{log.name}</TableCell>
                      <TableCell>{log.type}</TableCell>
                      <TableCell>{log.accessPoint}</TableCell>
                      <TableCell>{log.timestamp}</TableCell>
                      <TableCell>
                        <Badge variant={log.status === "granted" ? "success" : "destructive"}>
                          {t(`accessControl.accessLogs.status.${log.status}`)}
                        </Badge>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="nfc-devices" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>{t("accessControl.nfcDevices.title")}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex justify-between mb-4">
                <div className="flex w-full max-w-sm items-center space-x-2">
                  <Input placeholder={t("accessControl.search")} className="w-[300px]" />
                  <Button type="submit" size="icon">
                    <Search className="h-4 w-4" />
                  </Button>
                </div>
                <Dialog open={isAddNFCOpen} onOpenChange={setIsAddNFCOpen}>
                  <DialogTrigger asChild>
                    <Button>
                      <Plus className="mr-2 h-4 w-4" />
                      {t("accessControl.nfcDevices.add")}
                    </Button>
                  </DialogTrigger>
                  <DialogContent className="sm:max-w-[425px]">
                    <DialogHeader>
                      <DialogTitle>{t("accessControl.nfcDevices.addDevice")}</DialogTitle>
                      <DialogDescription>{t("accessControl.nfcDevices.addDeviceDescription")}</DialogDescription>
                    </DialogHeader>
                    <div className="grid gap-4 py-4">
                      <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="name" className="text-right">
                          {t("accessControl.nfcDevices.form.name")}
                        </Label>
                        <Input id="name" className="col-span-3" />
                      </div>
                      <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="type" className="text-right">
                          {t("accessControl.nfcDevices.form.type")}
                        </Label>
                        <Select>
                          <SelectTrigger id="type" className="col-span-3">
                            <SelectValue placeholder={t("accessControl.nfcDevices.form.selectType")} />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="card">{t("accessControl.nfcDevices.form.typeCard")}</SelectItem>
                            <SelectItem value="wristband">
                              {t("accessControl.nfcDevices.form.typeWristband")}
                            </SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="nfcId" className="text-right">
                          {t("accessControl.nfcDevices.form.nfcId")}
                        </Label>
                        <Input id="nfcId" className="col-span-3" />
                      </div>
                    </div>
                    <DialogFooter>
                      <Button type="submit" onClick={() => setIsAddNFCOpen(false)}>
                        {t("accessControl.nfcDevices.form.save")}
                      </Button>
                    </DialogFooter>
                  </DialogContent>
                </Dialog>
              </div>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>{t("accessControl.nfcDevices.table.name")}</TableHead>
                    <TableHead>{t("accessControl.nfcDevices.table.type")}</TableHead>
                    <TableHead>{t("accessControl.nfcDevices.table.nfcId")}</TableHead>
                    <TableHead>{t("accessControl.nfcDevices.table.status")}</TableHead>
                    <TableHead className="text-right">{t("accessControl.nfcDevices.table.actions")}</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {nfcDevices.map((device) => (
                    <TableRow key={device.id}>
                      <TableCell className="font-medium">{device.name}</TableCell>
                      <TableCell>{device.type}</TableCell>
                      <TableCell>{device.nfcId}</TableCell>
                      <TableCell>
                        <Badge variant={device.status === "active" ? "success" : "secondary"}>
                          {t(`accessControl.nfcDevices.status.${device.status}`)}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-right">
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" className="h-8 w-8 p-0">
                              <span className="sr-only">{t("accessControl.nfcDevices.actions.open")}</span>
                              <MoreHorizontal className="h-4 w-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuLabel>{t("accessControl.nfcDevices.actions.title")}</DropdownMenuLabel>
                            <DropdownMenuItem>
                              <Edit className="mr-2 h-4 w-4" />
                              {t("accessControl.nfcDevices.actions.edit")}
                            </DropdownMenuItem>
                            <DropdownMenuItem>
                              <UserCheck className="mr-2 h-4 w-4" />
                              {t("accessControl.nfcDevices.actions.assignUser")}
                            </DropdownMenuItem>
                            <DropdownMenuSeparator />
                            <DropdownMenuItem>
                              <Trash2 className="mr-2 h-4 w-4" />
                              {t("accessControl.nfcDevices.actions.delete")}
                            </DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="alerts" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>{t("accessControl.alerts.title")}</CardTitle>
            </CardHeader>
            <CardContent>
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
                  {alerts.map((alert) => (
                    <TableRow key={alert.id}>
                      <TableCell className="font-medium">{alert.name}</TableCell>
                      <TableCell>{alert.type}</TableCell>
                      <TableCell>{alert.location}</TableCell>
                      <TableCell>{alert.timestamp}</TableCell>
                      <TableCell className="text-right">
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" className="h-8 w-8 p-0">
                              <span className="sr-only">{t("accessControl.alerts.actions.open")}</span>
                              <MoreHorizontal className="h-4 w-4" />
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
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}