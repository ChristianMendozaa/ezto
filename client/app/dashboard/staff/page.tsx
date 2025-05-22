"use client"

import { useState } from "react"
import { useLanguage } from "@/lib/hooks/use-language"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { Search, Plus, MoreHorizontal, Edit, Trash2, Clock, Shield } from "lucide-react"
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
import { Switch } from "@/components/ui/switch"

// Mock data for staff members
const staffMembers = [
  { id: 1, name: "John Doe", role: "Trainer", schedule: "Mon, Wed, Fri 9AM-5PM", accessLevel: "Full" },
  { id: 2, name: "Jane Smith", role: "Receptionist", schedule: "Tue, Thu, Sat 8AM-4PM", accessLevel: "Limited" },
  { id: 3, name: "Mike Johnson", role: "Manager", schedule: "Mon-Fri 8AM-6PM", accessLevel: "Full" },
  { id: 4, name: "Sarah Williams", role: "Trainer", schedule: "Mon, Tue, Thu, Fri 2PM-10PM", accessLevel: "Standard" },
  { id: 5, name: "Tom Brown", role: "Maintenance", schedule: "Wed-Sun 10AM-6PM", accessLevel: "Limited" },
]

// Mock data for roles and permissions
const initialRoles = [
  { id: 1, name: "Trainer", permissions: { members: true, classes: true, payments: false, reports: false } },
  { id: 2, name: "Receptionist", permissions: { members: true, classes: true, payments: true, reports: false } },
  { id: 3, name: "Manager", permissions: { members: true, classes: true, payments: true, reports: true } },
  { id: 4, name: "Maintenance", permissions: { members: false, classes: false, payments: false, reports: false } },
]

const permissionPages = [
  "members",
  "classes",
  "payments",
  "reports",
  "promotions",
  "access-control",
  "store",
  "gym-settings",
]

export default function StaffPage() {
  const { t } = useLanguage()
  const [isAddStaffOpen, setIsAddStaffOpen] = useState(false)
  const [roles, setRoles] = useState(initialRoles)
  const [newRoleName, setNewRoleName] = useState("")
  const [selectedRole, setSelectedRole] = useState(roles[0])

  const handleAddRole = () => {
    if (newRoleName) {
      const newRole = {
        id: roles.length + 1,
        name: newRoleName,
        permissions: Object.fromEntries(permissionPages.map((page) => [page, false])),
      }
      setRoles([...roles, newRole])
      setNewRoleName("")
    }
  }

  const handlePermissionChange = (page: string, checked: boolean) => {
    setSelectedRole((prevRole) => ({
      ...prevRole,
      permissions: { ...prevRole.permissions, [page]: checked },
    }))
  }

  const handleRoleChange = (roleName: string) => {
    const role = roles.find((r) => r.name === roleName)
    if (role) {
      setSelectedRole(role)
    }
  }

  const handleSaveRoleChanges = () => {
    setRoles(roles.map((role) => (role.id === selectedRole.id ? selectedRole : role)))
  }

  return (
    <div className="flex-1 space-y-4 p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">{t("staff.title")}</h2>
        <div className="flex items-center space-x-2">
          <Dialog open={isAddStaffOpen} onOpenChange={setIsAddStaffOpen}>
            <DialogTrigger asChild>
              <Button>
                <Plus className="mr-2 h-4 w-4" />
                {t("staff.add")}
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
              <DialogHeader>
                <DialogTitle>{t("staff.addStaff")}</DialogTitle>
                <DialogDescription>{t("staff.addStaffDescription")}</DialogDescription>
              </DialogHeader>
              <div className="grid gap-4 py-4">
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="name" className="text-right">
                    {t("staff.form.name")}
                  </Label>
                  <Input id="name" className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="role" className="text-right">
                    {t("staff.form.role")}
                  </Label>
                  <Select>
                    <SelectTrigger id="role" className="col-span-3">
                      <SelectValue placeholder={t("staff.form.selectRole")} />
                    </SelectTrigger>
                    <SelectContent>
                      {roles.map((role) => (
                        <SelectItem key={role.id} value={role.name}>
                          {role.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="schedule" className="text-right">
                    {t("staff.form.schedule")}
                  </Label>
                  <Input id="schedule" className="col-span-3" />
                </div>
              </div>
              <DialogFooter>
                <Button type="submit" onClick={() => setIsAddStaffOpen(false)}>
                  {t("staff.form.save")}
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </div>
      </div>
      <Tabs defaultValue="staff-list" className="space-y-4">
        <TabsList>
          <TabsTrigger value="staff-list">{t("staff.tabs.staffList")}</TabsTrigger>
          <TabsTrigger value="access-config">{t("staff.tabs.accessConfig")}</TabsTrigger>
        </TabsList>
        <TabsContent value="staff-list" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>{t("staff.staffList")}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex justify-between mb-4">
                <div className="flex w-full max-w-sm items-center space-x-2">
                  <Input placeholder={t("staff.search")} className="w-[300px]" />
                  <Button type="submit" size="icon">
                    <Search className="h-4 w-4" />
                  </Button>
                </div>
              </div>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>{t("staff.table.name")}</TableHead>
                    <TableHead>{t("staff.table.role")}</TableHead>
                    <TableHead>{t("staff.table.schedule")}</TableHead>
                    <TableHead>{t("staff.table.accessLevel")}</TableHead>
                    <TableHead className="text-right">{t("staff.table.actions")}</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {staffMembers.map((staff) => (
                    <TableRow key={staff.id}>
                      <TableCell className="font-medium">{staff.name}</TableCell>
                      <TableCell>{staff.role}</TableCell>
                      <TableCell>{staff.schedule}</TableCell>
                      <TableCell>
                        <Badge
                          variant={
                            staff.accessLevel === "Full"
                              ? "default"
                              : staff.accessLevel === "Standard"
                                ? "secondary"
                                : "outline"
                          }
                        >
                          {staff.accessLevel}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-right">
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" className="h-8 w-8 p-0">
                              <span className="sr-only">{t("staff.actions.open")}</span>
                              <MoreHorizontal className="h-4 w-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuLabel>{t("staff.actions.title")}</DropdownMenuLabel>
                            <DropdownMenuItem>
                              <Edit className="mr-2 h-4 w-4" />
                              {t("staff.actions.edit")}
                            </DropdownMenuItem>
                            <DropdownMenuItem>
                              <Clock className="mr-2 h-4 w-4" />
                              {t("staff.actions.schedule")}
                            </DropdownMenuItem>
                            <DropdownMenuItem>
                              <Shield className="mr-2 h-4 w-4" />
                              {t("staff.actions.permissions")}
                            </DropdownMenuItem>
                            <DropdownMenuSeparator />
                            <DropdownMenuItem>
                              <Trash2 className="mr-2 h-4 w-4" />
                              {t("staff.actions.delete")}
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
        <TabsContent value="access-config" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>{t("staff.accessConfig")}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center space-x-2">
                  <Input
                    placeholder={t("staff.newRolePlaceholder")}
                    value={newRoleName}
                    onChange={(e) => setNewRoleName(e.target.value)}
                  />
                  <Button onClick={handleAddRole}>{t("staff.addRole")}</Button>
                </div>
                <div className="flex items-center space-x-2">
                  <Label>{t("staff.selectRole")}</Label>
                  <Select onValueChange={handleRoleChange} value={selectedRole.name}>
                    <SelectTrigger className="w-[180px]">
                      <SelectValue placeholder={t("staff.selectRolePlaceholder")} />
                    </SelectTrigger>
                    <SelectContent>
                      {roles.map((role) => (
                        <SelectItem key={role.id} value={role.name}>
                          {role.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  {permissionPages.map((page) => (
                    <div key={page} className="flex items-center space-x-2">
                      <Switch
                        checked={selectedRole.permissions[page]}
                        onCheckedChange={(checked) => handlePermissionChange(page, checked)}
                      />
                      <Label>{t(`staff.permissions.${page}`)}</Label>
                    </div>
                  ))}
                </div>
                <Button onClick={handleSaveRoleChanges}>{t("staff.saveChanges")}</Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

