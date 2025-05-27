"use client"

import { useState } from "react"
import { useLanguage } from "@/lib/hooks/use-language"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Search, Plus, Trash2 } from "lucide-react"
import { usePersonal, Personal, PersonalInput } from "@/hooks/usePersonal"

export default function StaffPage() {
  const { t } = useLanguage()
  const { personals, loading, error, createPersonal, deletePersonal, fetchPersonals } = usePersonal()

  const [isAddOpen, setIsAddOpen] = useState(false)
  const [newData, setNewData] = useState<PersonalInput>({
    name: "",
    role: "trainer",
    schedule: "",
    access_level: "standard",
  })

  const handleChange = (field: keyof PersonalInput, value: string | boolean) => {
    setNewData(prev => ({ ...prev, [field]: value }))
  }

  const handleSubmit = async () => {
    const ok = await createPersonal(newData)
    if (ok) {
      setIsAddOpen(false)
      setNewData({ name: "", role: "trainer", schedule: "", access_level: "standard" })
    }
  }

  return (
    <div className="p-8 space-y-4">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">{t("staff.title")}</h1>
        <Dialog open={isAddOpen} onOpenChange={setIsAddOpen}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="mr-2 h-4 w-4" /> {t("staff.add")}
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-md">
            <DialogHeader>
              <DialogTitle>{t("staff.addStaff")}</DialogTitle>
              <DialogDescription>{t("staff.addStaffDescription")}</DialogDescription>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              <div className="grid grid-cols-3 gap-4 items-center">
                <Label htmlFor="name" className="text-right">{t("staff.form.name")}</Label>
                <Input id="name" value={newData.name}
                  onChange={e => handleChange("name", e.target.value)} className="col-span-2" />
              </div>
              <div className="grid grid-cols-3 gap-4 items-center">
                <Label htmlFor="role" className="text-right">{t("staff.form.role")}</Label>
                <select id="role" value={newData.role}
                  onChange={e => handleChange("role", e.target.value)}
                  className="col-span-2 border rounded p-2">
                  {["trainer","receptionist","manager","maintenance"].map(r =>
                    <option key={r} value={r}>{t(`staff.roles.${r}`)}</option>
                  )}
                </select>
              </div>
              <div className="grid grid-cols-3 gap-4 items-center">
                <Label htmlFor="schedule" className="text-right">{t("staff.form.schedule")}</Label>
                <Input id="schedule" value={newData.schedule}
                  onChange={e => handleChange("schedule", e.target.value)} className="col-span-2" />
              </div>
              <div className="grid grid-cols-3 gap-4 items-center">
                <Label htmlFor="access_level" className="text-right">{t("staff.form.accessLevel")}</Label>
                <select id="access_level" value={newData.access_level}
                  onChange={e => handleChange("access_level", e.target.value)}
                  className="col-span-2 border rounded p-2">
                  {["full","standard","limited"].map(l =>
                    <option key={l} value={l}>{t(`staff.accessLevels.${l}`)}</option>
                  )}
                </select>
              </div>
            </div>
            <DialogFooter>
              <Button onClick={handleSubmit}>{t("staff.form.save")}</Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>

      <div className="flex items-center space-x-2">
        <Input
          placeholder={t("staff.search")}
          className="max-w-sm"
          onChange={e => {
            // opcional: podrías filtrar localmente
          }}
        />
        <Button onClick={() => fetchPersonals()}>
          {t("staff.refresh")}
        </Button>
      </div>

      {error && <div className="text-red-600">{error}</div>}
      {loading
        ? <div>{t("staff.loading")}</div>
        : (
          <Card>
            <CardHeader><CardTitle>{t("staff.staffList")}</CardTitle></CardHeader>
            <CardContent>
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
                  {personals.map((p: Personal) => (
                    <TableRow key={p.id}>
                      <TableCell className="font-medium">{p.name}</TableCell>
                      <TableCell>{t(`staff.roles.${p.role}`)}</TableCell>
                      <TableCell>{p.schedule}</TableCell>
                      <TableCell>
                        <Badge variant={p.access_level === "full" ? "default"
                          : p.access_level === "standard" ? "secondary" : "outline"}>
                          {t(`staff.accessLevels.${p.access_level}`)}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-right">
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={() => deletePersonal(p.id)}
                        >
                          <Trash2 className="h-4 w-4 text-red-600" />
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        )
      }
    </div>
  )
}
