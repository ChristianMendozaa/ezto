"use client"

import { useState } from "react"
import { useLanguage } from "@/lib/hooks/use-language"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { Search, Plus, MoreHorizontal, Edit, Trash2, Calendar } from "lucide-react"
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

// Mock data for classes
const classes = [
  {
    id: 1,
    name: "Yoga",
    instructor: "Jane Doe",
    schedule: "Mon, Wed, Fri 10:00 AM",
    capacity: "20/25",
    status: "active",
  },
  {
    id: 2,
    name: "Spinning",
    instructor: "John Smith",
    schedule: "Tue, Thu 6:00 PM",
    capacity: "15/15",
    status: "full",
  },
  {
    id: 3,
    name: "Zumba",
    instructor: "Maria Garcia",
    schedule: "Mon, Wed 7:00 PM",
    capacity: "18/30",
    status: "active",
  },
  {
    id: 4,
    name: "Pilates",
    instructor: "Sarah Johnson",
    schedule: "Tue, Thu 9:00 AM",
    capacity: "12/20",
    status: "active",
  },
  { id: 5, name: "Boxing", instructor: "Mike Tyson", schedule: "Fri 5:00 PM", capacity: "0/10", status: "cancelled" },
]

export default function ClassesPage() {
  const { t } = useLanguage()
  const [filter, setFilter] = useState("all")
  const [isAddClassOpen, setIsAddClassOpen] = useState(false)

  const filteredClasses = classes.filter((classItem) => {
    if (filter === "all") return true
    return classItem.status === filter
  })

  return (
    <div className="flex-1 space-y-4 p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">{t("classes.title")}</h2>
        <div className="flex items-center space-x-2">
          <Dialog open={isAddClassOpen} onOpenChange={setIsAddClassOpen}>
            <DialogTrigger asChild>
              <Button>
                <Plus className="mr-2 h-4 w-4" />
                {t("classes.add")}
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
              <DialogHeader>
                <DialogTitle>{t("classes.addClass")}</DialogTitle>
                <DialogDescription>{t("classes.addClassDescription")}</DialogDescription>
              </DialogHeader>
              <div className="grid gap-4 py-4">
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="name" className="text-right">
                    {t("classes.form.name")}
                  </Label>
                  <Input id="name" className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="instructor" className="text-right">
                    {t("classes.form.instructor")}
                  </Label>
                  <Input id="instructor" className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="schedule" className="text-right">
                    {t("classes.form.schedule")}
                  </Label>
                  <Input id="schedule" className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="capacity" className="text-right">
                    {t("classes.form.capacity")}
                  </Label>
                  <Input id="capacity" type="number" className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="description" className="text-right">
                    {t("classes.form.description")}
                  </Label>
                  <Textarea id="description" className="col-span-3" />
                </div>
              </div>
              <DialogFooter>
                <Button type="submit" onClick={() => setIsAddClassOpen(false)}>
                  {t("classes.form.save")}
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </div>
      </div>
      <div className="flex flex-col space-y-4">
        <Card>
          <CardHeader>
            <CardTitle>{t("classes.title")}</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex justify-between mb-4">
              <div className="flex w-full max-w-sm items-center space-x-2">
                <Input placeholder={t("classes.search")} className="w-[300px]" />
                <Button type="submit" size="icon">
                  <Search className="h-4 w-4" />
                </Button>
              </div>
              <Select value={filter} onValueChange={setFilter}>
                <SelectTrigger className="w-[180px]">
                  <SelectValue placeholder={t("classes.filter.all")} />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">{t("classes.filter.all")}</SelectItem>
                  <SelectItem value="active">{t("classes.filter.active")}</SelectItem>
                  <SelectItem value="cancelled">{t("classes.filter.cancelled")}</SelectItem>
                  <SelectItem value="full">{t("classes.filter.full")}</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>{t("classes.table.name")}</TableHead>
                  <TableHead>{t("classes.table.instructor")}</TableHead>
                  <TableHead>{t("classes.table.schedule")}</TableHead>
                  <TableHead>{t("classes.table.capacity")}</TableHead>
                  <TableHead>{t("classes.table.status")}</TableHead>
                  <TableHead className="text-right">{t("classes.table.actions")}</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredClasses.map((classItem) => (
                  <TableRow key={classItem.id}>
                    <TableCell className="font-medium">{classItem.name}</TableCell>
                    <TableCell>{classItem.instructor}</TableCell>
                    <TableCell>{classItem.schedule}</TableCell>
                    <TableCell>{classItem.capacity}</TableCell>
                    <TableCell>
                      <Badge
                        variant={
                          classItem.status === "active"
                            ? "success"
                            : classItem.status === "cancelled"
                              ? "destructive"
                              : "secondary"
                        }
                      >
                        {t(`classes.status.${classItem.status}`)}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-right">
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant="ghost" className="h-8 w-8 p-0">
                            <span className="sr-only">{t("classes.actions.open")}</span>
                            <MoreHorizontal className="h-4 w-4" />
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                          <DropdownMenuLabel>{t("classes.actions.title")}</DropdownMenuLabel>
                          <DropdownMenuItem>
                            <Edit className="mr-2 h-4 w-4" />
                            {t("classes.actions.edit")}
                          </DropdownMenuItem>
                          <DropdownMenuItem>
                            <Calendar className="mr-2 h-4 w-4" />
                            {t("classes.actions.schedule")}
                          </DropdownMenuItem>
                          <DropdownMenuSeparator />
                          <DropdownMenuItem>
                            <Trash2 className="mr-2 h-4 w-4" />
                            {t("classes.actions.delete")}
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
                {t("classes.pagination.prev")}
              </Button>
              <Button variant="outline" size="sm">
                {t("classes.pagination.next")}
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

