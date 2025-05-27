"use client"

import { useState } from "react"
import { useLanguage } from "@/lib/hooks/use-language"
import { useClasses, ClassDTO, ClassInput } from "@/hooks/useClasses"
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
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"

export default function ClassesPage() {
  const { t } = useLanguage()
  const { classes, loading, error, createClass, deleteClass, refetch } = useClasses()

  const [filter, setFilter] = useState<"all" | "active" | "cancelled">("all")
  const [search, setSearch] = useState("")
  const [isAddClassOpen, setIsAddClassOpen] = useState(false)
  const [form, setForm] = useState<ClassInput>({
    name: "",
    description: "",
    instructor: "",
    start_time: "",
    end_time: "",
    capacity: 0,
    location: "",
    status: true,
  })

  const onSubmit = async () => {
    const ok = await createClass(form)
    if (ok) {
      setIsAddClassOpen(false)
      refetch()
      setForm({ name: "", description: "", instructor: "", start_time: "", end_time: "", capacity: 0, location: "", status: true })
    }
  }

  const filtered = classes
    .filter((c) =>
      (filter === "all" || (c.status ? "active" : "cancelled") === filter) &&
      c.name.toLowerCase().includes(search.toLowerCase())
    )

  return (
    <div className="flex-1 space-y-4 p-8 pt-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold">{t("classes.title")}</h2>
        <Dialog open={isAddClassOpen} onOpenChange={setIsAddClassOpen}>
          <DialogTrigger asChild>
            <Button><Plus className="mr-2 h-4 w-4" />{t("classes.add")}</Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-lg">
            <DialogHeader>
              <DialogTitle>{t("classes.addClass")}</DialogTitle>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              {[
                { key: "name", label: t("classes.form.name"), type: "text" },
                { key: "description", label: t("classes.form.description"), type: "textarea" },
                { key: "instructor", label: t("classes.form.instructor"), type: "text" },
                { key: "start_time", label: t("classes.form.startTime"), type: "datetime-local" },
                { key: "end_time", label: t("classes.form.endTime"), type: "datetime-local" },
                { key: "capacity", label: t("classes.form.capacity"), type: "number" },
                { key: "location", label: t("classes.form.location"), type: "text" },
              ].map(({ key, label, type }) => (
                <div key={key} className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor={key} className="text-right">{label}</Label>
                  {type === "textarea" ? (
                    <Textarea
                      id={key}
                      className="col-span-3"
                      value={(form as any)[key] as string}
                      onChange={(e) => setForm(f => ({ ...f, [key]: e.target.value }))}
                    />
                  ) : (
                    <Input
                      id={key}
                      type={type}
                      className="col-span-3"
                      value={(form as any)[key] as string | number}
                      onChange={(e) => setForm(f => ({ ...f, [key]: type === "number" ? +e.target.value : e.target.value }))}
                    />
                  )}
                </div>
              ))}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="status" className="text-right">{t("classes.form.status")}</Label>
                <Select
                  value={form.status ? "active" : "cancelled"}
                  onValueChange={(v) => setForm(f => ({ ...f, status: v === "active" }))}
                  className="col-span-3"
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="active">{t("classes.status.active")}</SelectItem>
                    <SelectItem value="cancelled">{t("classes.status.cancelled")}</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
            <DialogFooter>
              <Button onClick={onSubmit}>{t("classes.form.save")}</Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>{t("classes.list")}</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex justify-between mb-4">
            <div className="flex space-x-2">
              <Input
                placeholder={t("classes.search")}
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
              <Button size="icon"><Search /></Button>
            </div>
            <Select value={filter} onValueChange={setFilter}>
              <SelectTrigger className="w-[150px]">
                <SelectValue placeholder={t("classes.filter.all")} />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">{t("classes.filter.all")}</SelectItem>
                <SelectItem value="active">{t("classes.filter.active")}</SelectItem>
                <SelectItem value="cancelled">{t("classes.filter.cancelled")}</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {loading && <p>{t("loading")}…</p>}
          {error && <p className="text-destructive">{error}</p>}

          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>{t("classes.table.name")}</TableHead>
                <TableHead>{t("classes.table.instructor")}</TableHead>
                <TableHead>{t("classes.table.schedule")}</TableHead>
                <TableHead>{t("classes.table.capacity")}</TableHead>
                <TableHead>{t("classes.table.location")}</TableHead>
                <TableHead>{t("classes.table.status")}</TableHead>
                <TableHead className="text-right">{t("classes.table.actions")}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filtered.map((c) => (
                <TableRow key={c.id}>
                  <TableCell className="font-medium">{c.name}</TableCell>
                  <TableCell>{c.instructor}</TableCell>
                  <TableCell>
                    {new Date(c.start_time).toLocaleString()} –{" "}
                    {new Date(c.end_time).toLocaleString()}
                  </TableCell>
                  <TableCell>{c.capacity}</TableCell>
                  <TableCell>{c.location}</TableCell>
                  <TableCell>
                    <Badge variant={c.status ? "success" : "destructive"}>
                      {t(`classes.status.${c.status ? "active" : "cancelled"}`)}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right">
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" className="h-8 w-8 p-0">
                          <MoreHorizontal />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuLabel>{t("classes.actions.title")}</DropdownMenuLabel>
                        <DropdownMenuItem onClick={() => {/* editar */}}>
                          <Edit className="mr-2 h-4 w-4" />
                          {t("classes.actions.edit")}
                        </DropdownMenuItem>
                        <DropdownMenuItem onClick={() => deleteClass(c.id!)}>
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
        </CardContent>
      </Card>
    </div>
  )
}
