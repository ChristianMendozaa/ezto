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
import { Search, Plus, MoreHorizontal, Edit, Trash2, CreditCard } from "lucide-react"
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

// Mock data for members
const members = [
  { id: 1, name: "John Doe", email: "john@example.com", status: "active", joinDate: "2023-01-15" },
  { id: 2, name: "Jane Smith", email: "jane@example.com", status: "inactive", joinDate: "2023-02-20" },
  { id: 3, name: "Alice Johnson", email: "alice@example.com", status: "active", joinDate: "2023-03-10" },
  { id: 4, name: "Bob Williams", email: "bob@example.com", status: "suspended", joinDate: "2023-04-05" },
  { id: 5, name: "Charlie Brown", email: "charlie@example.com", status: "active", joinDate: "2023-05-12" },
]

export default function MembersPage() {
  const { t } = useLanguage()
  const [filter, setFilter] = useState("all")
  const [isAddMemberOpen, setIsAddMemberOpen] = useState(false)

  const filteredMembers = members.filter((member) => {
    if (filter === "all") return true
    return member.status === filter
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
          <h2 className="text-3xl font-bold tracking-tight">{t("members.title")}</h2>
          <div className="flex items-center space-x-2">
            <Dialog open={isAddMemberOpen} onOpenChange={setIsAddMemberOpen}>
              <DialogTrigger asChild>
                <Button>
                  <Plus className="mr-2 h-4 w-4" />
                  {t("members.add")}
                </Button>
              </DialogTrigger>
              <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                  <DialogTitle>{t("members.addMember")}</DialogTitle>
                  <DialogDescription>{t("members.addMemberDescription")}</DialogDescription>
                </DialogHeader>
                <div className="grid gap-4 py-4">
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="name" className="text-right">
                      {t("members.form.name")}
                    </Label>
                    <Input id="name" className="col-span-3" />
                  </div>
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="email" className="text-right">
                      {t("members.form.email")}
                    </Label>
                    <Input id="email" className="col-span-3" />
                  </div>
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="nfc" className="text-right">
                      {t("members.form.nfcCard")}
                    </Label>
                    <div className="col-span-3 flex items-center space-x-2">
                      <Input id="nfc" placeholder={t("members.form.nfcPlaceholder")} />
                      <Button size="sm">
                        <CreditCard className="mr-2 h-4 w-4" />
                        {t("members.form.scanNFC")}
                      </Button>
                    </div>
                  </div>
                </div>
                <DialogFooter>
                  <Button type="submit" onClick={() => setIsAddMemberOpen(false)}>
                    {t("members.form.save")}
                  </Button>
                </DialogFooter>
              </DialogContent>
            </Dialog>
          </div>
        </div>
        <div className="flex flex-col space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>{t("members.title")}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex justify-between mb-4">
                <div className="flex w-full max-w-sm items-center space-x-2">
                  <Input placeholder={t("members.search")} className="w-[300px]" />
                  <Button type="submit" size="icon">
                    <Search className="h-4 w-4" />
                  </Button>
                </div>
                <Select value={filter} onValueChange={setFilter}>
                  <SelectTrigger className="w-[180px]">
                    <SelectValue placeholder={t("members.filter.all")} />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">{t("members.filter.all")}</SelectItem>
                    <SelectItem value="active">{t("members.filter.active")}</SelectItem>
                    <SelectItem value="inactive">{t("members.filter.inactive")}</SelectItem>
                    <SelectItem value="suspended">{t("members.filter.suspended")}</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>{t("members.table.name")}</TableHead>
                    <TableHead>{t("members.table.email")}</TableHead>
                    <TableHead>{t("members.table.status")}</TableHead>
                    <TableHead>{t("members.table.joinDate")}</TableHead>
                    <TableHead className="text-right">{t("members.table.actions")}</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredMembers.map((member) => (
                    <TableRow key={member.id}>
                      <TableCell className="font-medium">{member.name}</TableCell>
                      <TableCell>{member.email}</TableCell>
                      <TableCell>
                        <Badge
                          variant={
                            member.status === "active"
                              ? "success"
                              : member.status === "inactive"
                                ? "secondary"
                                : "destructive"
                          }
                        >
                          {t(`members.status.${member.status}`)}
                        </Badge>
                      </TableCell>
                      <TableCell>{member.joinDate}</TableCell>
                      <TableCell className="text-right">
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" className="h-8 w-8 p-0">
                              <span className="sr-only">{t("members.actions.open")}</span>
                              <MoreHorizontal className="h-4 w-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuLabel>{t("members.actions.title")}</DropdownMenuLabel>
                            <DropdownMenuItem onClick={() => navigator.clipboard.writeText(member.email)}>
                              {t("members.actions.copyEmail")}
                            </DropdownMenuItem>
                            <DropdownMenuSeparator />
                            <DropdownMenuItem>
                              <Edit className="mr-2 h-4 w-4" />
                              {t("members.actions.edit")}
                            </DropdownMenuItem>
                            <DropdownMenuItem>
                              <CreditCard className="mr-2 h-4 w-4" />
                              {t("members.actions.manageNFC")}
                            </DropdownMenuItem>
                            <DropdownMenuItem>
                              <Trash2 className="mr-2 h-4 w-4" />
                              {t("members.actions.delete")}
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
                  {t("members.pagination.prev")}
                </Button>
                <Button variant="outline" size="sm">
                  {t("members.pagination.next")}
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

