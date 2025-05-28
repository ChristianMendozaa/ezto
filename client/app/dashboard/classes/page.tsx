"use client"

import { useState } from "react"
import { useLanguage } from "@/lib/hooks/use-language"
import { useClasses, ClassDTO, ClassInput, Session } from "@/hooks/useClasses"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { Search, Plus, Edit, Trash2, MoreHorizontal } from "lucide-react"
import { ClassFormDialog, ClassFormData } from "@/app/dashboard/classes/ClassFormDialog"

export default function ClassesPage() {
  const { t } = useLanguage()
  const { classes, loading, error, createClass, updateClass, deleteClass, refetch } = useClasses()

  const [filter, setFilter] = useState<"all"|"active"|"cancelled">("all")
  const [search, setSearch] = useState("")

  const filtered = classes
    .filter(c =>
      (filter === "all" || (c.status ? "active":"cancelled") === filter) &&
      c.name.toLowerCase().includes(search.toLowerCase())
    )

  return (
    <div className="p-8 space-y-4">
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold">{t("classes.title")}</h2>
        <ClassFormDialog
          trigger={<Button><Plus className="mr-2 h-4 w-4"/> {t("classes.add")}</Button>}
          onSave={async (data: ClassFormData) => {
            const ok = await createClass(data)
            if (ok) refetch()
            return ok
          }}
        />
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
                onChange={e => setSearch(e.target.value)}
                className="w-64"
              />
              <Button size="icon"><Search/></Button>
            </div>
            <Select value={filter} onValueChange={setFilter}>
              <SelectTrigger className="w-40"><SelectValue/></SelectTrigger>
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
                <TableHead>{t("classes.table.sessions")}</TableHead>
                <TableHead>{t("classes.table.capacity")}</TableHead>
                <TableHead>{t("classes.table.location")}</TableHead>
                <TableHead>{t("classes.table.status")}</TableHead>
                <TableHead className="text-right">{t("classes.table.actions")}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filtered.map(c => (
                <TableRow key={c.id}>
                  <TableCell className="font-medium">{c.name}</TableCell>
                  <TableCell>{c.instructor}</TableCell>
                  <TableCell>
                    <ul className="space-y-1">
                      {c.sessions?.map((s, i) => (
                        <li key={i}>
                          {t(`days.${s.day.toLowerCase()}`)}: {s.start_time.slice(0,5)}–{s.end_time.slice(0,5)}
                        </li>
                      )) ?? null}
                    </ul>

                  </TableCell>
                  <TableCell>{c.capacity}</TableCell>
                  <TableCell>{c.location}</TableCell>
                  <TableCell>
                    <Badge variant={c.status ? "success":"destructive"}>
                      {t(`classes.status.${c.status?"active":"cancelled"}`)}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right">
                    <div className="flex justify-end space-x-2">
                      <ClassFormDialog
                        initial={{
                          name: c.name,
                          instructor: c.instructor,
                          capacity: c.capacity,
                          location: c.location||"",
                          description: c.description,
                          status: c.status,
                          sessions: c.sessions
                        }}
                        trigger={<Button variant="ghost" size="icon"><Edit/></Button>}
                        onSave={async (data) => {
                          const ok = await updateClass(c.id!, data)
                          if (ok) refetch()
                          return ok
                        }}
                      />
                      <Button variant="ghost" size="icon" onClick={() => deleteClass(c.id!)}>
                        <Trash2 className="h-4 w-4 text-red-600"/>
                      </Button>
                    </div>
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
