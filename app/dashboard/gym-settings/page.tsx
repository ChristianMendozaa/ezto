"use client"

import { useState } from "react"
import { useLanguage } from "@/lib/hooks/use-language"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { MainNav } from "@/components/main-nav"
import { UserNav } from "@/components/user-nav"
import { ThemeToggle } from "@/components/theme-toggle"
import { LanguageToggle } from "@/components/language-toggle"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Plus, Edit, Trash2 } from "lucide-react"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

// Mock data for memberships
const memberships = [
  { id: 1, name: "Basic", price: 29.99, duration: "1 month", features: "Access to gym" },
  { id: 2, name: "Standard", price: 49.99, duration: "1 month", features: "Access to gym, classes" },
  { id: 3, name: "Premium", price: 79.99, duration: "1 month", features: "Access to gym, classes, personal trainer" },
]

export default function GymSettingsPage() {
  const { t } = useLanguage()
  const [isAddMembershipOpen, setIsAddMembershipOpen] = useState(false)

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
          <h2 className="text-3xl font-bold tracking-tight">{t("gymSettings.title")}</h2>
        </div>
        <Tabs defaultValue="profile" className="space-y-4">
          <TabsList>
            <TabsTrigger value="profile">{t("gymSettings.tabs.profile")}</TabsTrigger>
            <TabsTrigger value="memberships">{t("gymSettings.tabs.memberships")}</TabsTrigger>
          </TabsList>
          <TabsContent value="profile" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>{t("gymSettings.profile.title")}</CardTitle>
              </CardHeader>
              <CardContent>
                <form className="space-y-4">
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="gymName" className="text-right">
                      {t("gymSettings.profile.gymName")}
                    </Label>
                    <Input id="gymName" className="col-span-3" />
                  </div>
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="logo" className="text-right">
                      {t("gymSettings.profile.logo")}
                    </Label>
                    <Input id="logo" type="file" className="col-span-3" />
                  </div>
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="address" className="text-right">
                      {t("gymSettings.profile.address")}
                    </Label>
                    <Textarea id="address" className="col-span-3" />
                  </div>
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="openingHours" className="text-right">
                      {t("gymSettings.profile.openingHours")}
                    </Label>
                    <Textarea
                      id="openingHours"
                      className="col-span-3"
                      placeholder="Monday-Friday: 6am-10pm&#10;Saturday-Sunday: 8am-8pm"
                    />
                  </div>
                  <div className="flex justify-end">
                    <Button type="submit">{t("gymSettings.profile.save")}</Button>
                  </div>
                </form>
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="memberships" className="space-y-4">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between">
                <CardTitle>{t("gymSettings.memberships.title")}</CardTitle>
                <Dialog open={isAddMembershipOpen} onOpenChange={setIsAddMembershipOpen}>
                  <DialogTrigger asChild>
                    <Button>
                      <Plus className="mr-2 h-4 w-4" />
                      {t("gymSettings.memberships.add")}
                    </Button>
                  </DialogTrigger>
                  <DialogContent className="sm:max-w-[425px]">
                    <DialogHeader>
                      <DialogTitle>{t("gymSettings.memberships.addMembership")}</DialogTitle>
                      <DialogDescription>{t("gymSettings.memberships.addMembershipDescription")}</DialogDescription>
                    </DialogHeader>
                    <div className="grid gap-4 py-4">
                      <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="name" className="text-right">
                          {t("gymSettings.memberships.form.name")}
                        </Label>
                        <Input id="name" className="col-span-3" />
                      </div>
                      <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="price" className="text-right">
                          {t("gymSettings.memberships.form.price")}
                        </Label>
                        <Input id="price" type="number" className="col-span-3" />
                      </div>
                      <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="duration" className="text-right">
                          {t("gymSettings.memberships.form.duration")}
                        </Label>
                        <Select>
                          <SelectTrigger id="duration" className="col-span-3">
                            <SelectValue placeholder={t("gymSettings.memberships.form.selectDuration")} />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="1-month">1 {t("gymSettings.memberships.form.month")}</SelectItem>
                            <SelectItem value="3-months">3 {t("gymSettings.memberships.form.months")}</SelectItem>
                            <SelectItem value="6-months">6 {t("gymSettings.memberships.form.months")}</SelectItem>
                            <SelectItem value="1-year">1 {t("gymSettings.memberships.form.year")}</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="features" className="text-right">
                          {t("gymSettings.memberships.form.features")}
                        </Label>
                        <Textarea id="features" className="col-span-3" />
                      </div>
                    </div>
                    <DialogFooter>
                      <Button type="submit" onClick={() => setIsAddMembershipOpen(false)}>
                        {t("gymSettings.memberships.form.save")}
                      </Button>
                    </DialogFooter>
                  </DialogContent>
                </Dialog>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>{t("gymSettings.memberships.table.name")}</TableHead>
                      <TableHead>{t("gymSettings.memberships.table.price")}</TableHead>
                      <TableHead>{t("gymSettings.memberships.table.duration")}</TableHead>
                      <TableHead>{t("gymSettings.memberships.table.features")}</TableHead>
                      <TableHead className="text-right">{t("gymSettings.memberships.table.actions")}</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {memberships.map((membership) => (
                      <TableRow key={membership.id}>
                        <TableCell className="font-medium">{membership.name}</TableCell>
                        <TableCell>${membership.price}</TableCell>
                        <TableCell>{membership.duration}</TableCell>
                        <TableCell>{membership.features}</TableCell>
                        <TableCell className="text-right">
                          <Button variant="ghost" size="icon">
                            <Edit className="h-4 w-4" />
                          </Button>
                          <Button variant="ghost" size="icon">
                            <Trash2 className="h-4 w-4" />
                          </Button>
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
    </div>
  )
}

