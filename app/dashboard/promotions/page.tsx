"use client"

import { useState } from "react"
import { useLanguage } from "@/lib/hooks/use-language"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { MainNav } from "@/components/main-nav"
import { UserNav } from "@/components/user-nav"
import { Search, Plus, MoreHorizontal, Edit, Trash2, Calendar } from "lucide-react"
import { ThemeToggle } from "@/components/theme-toggle"
import { LanguageToggle } from "@/components/language-toggle"
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
import { Textarea } from "@/components/ui/textarea"

// Mock data for promotions
const promotions = [
  {
    id: 1,
    name: "Summer Special",
    description: "20% off on all annual memberships",
    startDate: "2023-06-01",
    endDate: "2023-08-31",
    status: "active",
  },
  {
    id: 2,
    name: "Refer a Friend",
    description: "Get one month free when you refer a friend",
    startDate: "2023-01-01",
    endDate: "2023-12-31",
    status: "active",
  },
  {
    id: 3,
    name: "New Year's Resolution",
    description: "50% off on the first month for new members",
    startDate: "2024-01-01",
    endDate: "2024-01-31",
    status: "inactive",
  },
]

export default function PromotionsPage() {
  const { t } = useLanguage()
  const [filter, setFilter] = useState("all")
  const [isAddPromotionOpen, setIsAddPromotionOpen] = useState(false)

  const filteredPromotions = promotions.filter((promotion) => {
    if (filter === "all") return true
    return promotion.status === filter
  })

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
          <h2 className="text-3xl font-bold tracking-tight">{t("promotions.title")}</h2>
          <div className="flex items-center space-x-2">
            <Dialog open={isAddPromotionOpen} onOpenChange={setIsAddPromotionOpen}>
              <DialogTrigger asChild>
                <Button>
                  <Plus className="mr-2 h-4 w-4" />
                  {t("promotions.add")}
                </Button>
              </DialogTrigger>
              <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                  <DialogTitle>{t("promotions.addPromotion")}</DialogTitle>
                  <DialogDescription>{t("promotions.addPromotionDescription")}</DialogDescription>
                </DialogHeader>
                <div className="grid gap-4 py-4">
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="name" className="text-right">
                      {t("promotions.form.name")}
                    </Label>
                    <Input id="name" className="col-span-3" />
                  </div>
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="description" className="text-right">
                      {t("promotions.form.description")}
                    </Label>
                    <Textarea id="description" className="col-span-3" />
                  </div>
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="startDate" className="text-right">
                      {t("promotions.form.startDate")}
                    </Label>
                    <Input id="startDate" type="date" className="col-span-3" />
                  </div>
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="endDate" className="text-right">
                      {t("promotions.form.endDate")}
                    </Label>
                    <Input id="endDate" type="date" className="col-span-3" />
                  </div>
                </div>
                <DialogFooter>
                  <Button type="submit" onClick={() => setIsAddPromotionOpen(false)}>
                    {t("promotions.form.save")}
                  </Button>
                </DialogFooter>
              </DialogContent>
            </Dialog>
          </div>
        </div>
        <div className="flex flex-col space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>{t("promotions.title")}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex justify-between mb-4">
                <div className="flex w-full max-w-sm items-center space-x-2">
                  <Input placeholder={t("promotions.search")} className="w-[300px]" />
                  <Button type="submit" size="icon">
                    <Search className="h-4 w-4" />
                  </Button>
                </div>
                <Select value={filter} onValueChange={setFilter}>
                  <SelectTrigger className="w-[180px]">
                    <SelectValue placeholder={t("promotions.filter.all")} />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">{t("promotions.filter.all")}</SelectItem>
                    <SelectItem value="active">{t("promotions.filter.active")}</SelectItem>
                    <SelectItem value="inactive">{t("promotions.filter.inactive")}</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>{t("promotions.table.name")}</TableHead>
                    <TableHead>{t("promotions.table.description")}</TableHead>
                    <TableHead>{t("promotions.table.startDate")}</TableHead>
                    <TableHead>{t("promotions.table.endDate")}</TableHead>
                    <TableHead>{t("promotions.table.status")}</TableHead>
                    <TableHead className="text-right">{t("promotions.table.actions")}</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredPromotions.map((promotion) => (
                    <TableRow key={promotion.id}>
                      <TableCell className="font-medium">{promotion.name}</TableCell>
                      <TableCell>{promotion.description}</TableCell>
                      <TableCell>{promotion.startDate}</TableCell>
                      <TableCell>{promotion.endDate}</TableCell>
                      <TableCell>
                        <Badge variant={promotion.status === "active" ? "success" : "secondary"}>
                          {t(`promotions.status.${promotion.status}`)}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-right">
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" className="h-8 w-8 p-0">
                              <span className="sr-only">{t("promotions.actions.open")}</span>
                              <MoreHorizontal className="h-4 w-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuLabel>{t("promotions.actions.title")}</DropdownMenuLabel>
                            <DropdownMenuItem>
                              <Edit className="mr-2 h-4 w-4" />
                              {t("promotions.actions.edit")}
                            </DropdownMenuItem>
                            <DropdownMenuItem>
                              <Calendar className="mr-2 h-4 w-4" />
                              {t("promotions.actions.schedule")}
                            </DropdownMenuItem>
                            <DropdownMenuSeparator />
                            <DropdownMenuItem>
                              <Trash2 className="mr-2 h-4 w-4" />
                              {t("promotions.actions.delete")}
                            </DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
              <div className="flex items-center justify-end space-x-2 py-4">
                <Button variant="outline" size="sm">
                  {t("promotions.pagination.prev")}
                </Button>
                <Button variant="outline" size="sm">
                  {t("promotions.pagination.next")}
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

