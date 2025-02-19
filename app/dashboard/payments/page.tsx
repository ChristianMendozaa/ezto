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
import { Search, Plus, MoreHorizontal, Edit, Trash2, FileText, DollarSign } from "lucide-react"
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

// Mock data for payments
const payments = [
  { id: "PAY001", member: "John Doe", amount: "$50.00", date: "2023-07-01", status: "completed" },
  { id: "PAY002", member: "Jane Smith", amount: "$75.00", date: "2023-07-02", status: "pending" },
  { id: "PAY003", member: "Alice Johnson", amount: "$100.00", date: "2023-07-03", status: "completed" },
  { id: "PAY004", member: "Bob Williams", amount: "$60.00", date: "2023-07-04", status: "failed" },
  { id: "PAY005", member: "Charlie Brown", amount: "$80.00", date: "2023-07-05", status: "completed" },
]

export default function PaymentsPage() {
  const { t } = useLanguage()
  const [filter, setFilter] = useState("all")
  const [isAddPaymentOpen, setIsAddPaymentOpen] = useState(false)

  const filteredPayments = payments.filter((payment) => {
    if (filter === "all") return true
    return payment.status === filter
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
          <h2 className="text-3xl font-bold tracking-tight">{t("payments.title")}</h2>
          <div className="flex items-center space-x-2">
            <Dialog open={isAddPaymentOpen} onOpenChange={setIsAddPaymentOpen}>
              <DialogTrigger asChild>
                <Button>
                  <Plus className="mr-2 h-4 w-4" />
                  {t("payments.add")}
                </Button>
              </DialogTrigger>
              <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                  <DialogTitle>{t("payments.addPayment")}</DialogTitle>
                  <DialogDescription>{t("payments.addPaymentDescription")}</DialogDescription>
                </DialogHeader>
                <div className="grid gap-4 py-4">
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="member" className="text-right">
                      {t("payments.form.member")}
                    </Label>
                    <Input id="member" className="col-span-3" />
                  </div>
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="amount" className="text-right">
                      {t("payments.form.amount")}
                    </Label>
                    <div className="col-span-3 flex items-center">
                      <DollarSign className="mr-2 h-4 w-4 text-muted-foreground" />
                      <Input id="amount" type="number" step="0.01" min="0" />
                    </div>
                  </div>
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="date" className="text-right">
                      {t("payments.form.date")}
                    </Label>
                    <Input id="date" type="date" className="col-span-3" />
                  </div>
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="status" className="text-right">
                      {t("payments.form.status")}
                    </Label>
                    <Select>
                      <SelectTrigger id="status" className="col-span-3">
                        <SelectValue placeholder={t("payments.form.selectStatus")} />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="completed">{t("payments.status.completed")}</SelectItem>
                        <SelectItem value="pending">{t("payments.status.pending")}</SelectItem>
                        <SelectItem value="failed">{t("payments.status.failed")}</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="notes" className="text-right">
                      {t("payments.form.notes")}
                    </Label>
                    <Textarea id="notes" className="col-span-3" />
                  </div>
                </div>
                <DialogFooter>
                  <Button type="submit" onClick={() => setIsAddPaymentOpen(false)}>
                    {t("payments.form.save")}
                  </Button>
                </DialogFooter>
              </DialogContent>
            </Dialog>
          </div>
        </div>
        <div className="flex flex-col space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>{t("payments.title")}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex justify-between mb-4">
                <div className="flex w-full max-w-sm items-center space-x-2">
                  <Input placeholder={t("payments.search")} className="w-[300px]" />
                  <Button type="submit" size="icon">
                    <Search className="h-4 w-4" />
                  </Button>
                </div>
                <Select value={filter} onValueChange={setFilter}>
                  <SelectTrigger className="w-[180px]">
                    <SelectValue placeholder={t("payments.filter.all")} />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">{t("payments.filter.all")}</SelectItem>
                    <SelectItem value="completed">{t("payments.filter.completed")}</SelectItem>
                    <SelectItem value="pending">{t("payments.filter.pending")}</SelectItem>
                    <SelectItem value="failed">{t("payments.filter.failed")}</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>{t("payments.table.id")}</TableHead>
                    <TableHead>{t("payments.table.member")}</TableHead>
                    <TableHead>{t("payments.table.amount")}</TableHead>
                    <TableHead>{t("payments.table.date")}</TableHead>
                    <TableHead>{t("payments.table.status")}</TableHead>
                    <TableHead className="text-right">{t("payments.table.actions")}</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredPayments.map((payment) => (
                    <TableRow key={payment.id}>
                      <TableCell className="font-medium">{payment.id}</TableCell>
                      <TableCell>{payment.member}</TableCell>
                      <TableCell>{payment.amount}</TableCell>
                      <TableCell>{payment.date}</TableCell>
                      <TableCell>
                        <Badge
                          variant={
                            payment.status === "completed"
                              ? "success"
                              : payment.status === "pending"
                                ? "secondary"
                                : "destructive"
                          }
                        >
                          {t(`payments.status.${payment.status}`)}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-right">
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" className="h-8 w-8 p-0">
                              <span className="sr-only">{t("payments.actions.open")}</span>
                              <MoreHorizontal className="h-4 w-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuLabel>{t("payments.actions.title")}</DropdownMenuLabel>
                            <DropdownMenuItem>
                              <FileText className="mr-2 h-4 w-4" />
                              {t("payments.actions.viewDetails")}
                            </DropdownMenuItem>
                            <DropdownMenuItem>
                              <Edit className="mr-2 h-4 w-4" />
                              {t("payments.actions.edit")}
                            </DropdownMenuItem>
                            <DropdownMenuSeparator />
                            <DropdownMenuItem>
                              <Trash2 className="mr-2 h-4 w-4" />
                              {t("payments.actions.delete")}
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
                  {t("payments.pagination.prev")}
                </Button>
                <Button variant="outline" size="sm">
                  {t("payments.pagination.next")}
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

