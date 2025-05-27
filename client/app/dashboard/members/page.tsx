// app/members/MembersPage.tsx
"use client"

import { useEffect, useState } from "react"
import { useLanguage } from "@/lib/hooks/use-language"
import { Member, useMembers } from "@/hooks/useMembers"
import { useNfcPairing } from "@/hooks/useNfcPairing"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { Search, Plus, MoreHorizontal, Edit, Trash2, CreditCard } from "lucide-react"
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

export default function MembersPage() {
  const { t } = useLanguage()
  const [filter, setFilter] = useState("all")
  const [isAddMemberOpen, setIsAddMemberOpen] = useState(false)
  const [isPairNfcOpen, setIsPairNfcOpen] = useState(false)
  const [lastCreatedMember, setLastCreatedMember] = useState<Member | null>(null)
  const [isEditOpen, setIsEditOpen] = useState(false)
  const [editMember, setEditMember] = useState<Member | null>(null)
  const [localPairingCode, setLocalPairingCode] = useState<string | null>(null)

  const { generatePairingCode, pairingCode, loading: pairingLoading, error: pairingError } = useNfcPairing()

  const {
    members,
    fetchMembers,
    createMember,
    deleteMember,
    updateMember,
    loading,
    error
  } = useMembers()

  useEffect(() => {
    fetchMembers()
  }, [fetchMembers])

  useEffect(() => {
    if (pairingCode) {
      setLocalPairingCode(pairingCode);
    }
  }, [pairingCode])

  const filteredMembers = members.filter((member) => {
    if (filter === "all") return true
    return member.status === filter
  })

  const handleEdit = (member: Member) => {
    setEditMember(member)
    setIsEditOpen(true)
  }

  const handleUpdate = async () => {
    if (!editMember) return
    await updateMember(editMember.id, editMember)
    setIsEditOpen(false)
  }

  return (
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
              </div>
              <DialogFooter>
                <Button
                  type="submit"
                  onClick={async () => {
                    const newMember: Member = {
                      id: "",
                      name: (document.getElementById("name") as HTMLInputElement).value,
                      email: (document.getElementById("email") as HTMLInputElement).value,
                      nfc_id: "",
                      status: "activo",
                      join_date: new Date().toISOString(),
                    };

                    const created = await createMember(newMember);
                    console.log("🧾 Miembro creado:", created);
                    setLastCreatedMember(created.data);
                    setLocalPairingCode(null);
                    setIsAddMemberOpen(false);
                    setTimeout(() => setIsPairNfcOpen(true), 100);
                  }}
                >
                  {t("members.form.save")}
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>

          <Dialog open={isPairNfcOpen} onOpenChange={setIsPairNfcOpen}>
            <DialogContent className="sm:max-w-[425px]">
              <DialogHeader>
                <DialogTitle>Emparejar tarjeta NFC</DialogTitle>
                <DialogDescription>
                  Genera un código de emparejamiento para el miembro y úsalo en la app móvil.
                </DialogDescription>
              </DialogHeader>
              <div className="grid gap-4 py-4">
                {lastCreatedMember ? (
                  <>
                    <p><strong>Miembro:</strong> {lastCreatedMember.name}</p>
                    <p><strong>Email:</strong> {lastCreatedMember.email}</p>
                    <Button
                      onClick={async () => {
                        await generatePairingCode(lastCreatedMember.id);
                        if (pairingError) {
                          alert("Error al generar el código: " + pairingError);
                        }
                      }}
                    >
                      {pairingLoading ? "Generando..." : "Generar código de emparejamiento"}
                    </Button>
                    {localPairingCode && (
                      <p className="text-green-600 font-semibold mt-2">Código generado: {localPairingCode}</p>
                    )}
                  </>
                ) : (
                  <p className="text-sm text-muted">No se pudo obtener el miembro recién creado.</p>
                )}
              </div>
            </DialogContent>
          </Dialog>

          {/* Editar miembro */}
          <Dialog open={isEditOpen} onOpenChange={setIsEditOpen}>
            <DialogContent className="sm:max-w-[425px]">
              <DialogHeader>
                <DialogTitle>{t("members.editMember")}</DialogTitle>
              </DialogHeader>
              {editMember && (
                <div className="grid gap-4 py-4">
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="edit-name" className="text-right">
                      {t("members.form.name")}
                    </Label>
                    <Input
                      id="edit-name"
                      className="col-span-3"
                      value={editMember.name}
                      onChange={(e) => setEditMember({ ...editMember, name: e.target.value })}
                    />
                  </div>
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="edit-email" className="text-right">
                      {t("members.form.email")}
                    </Label>
                    <Input
                      id="edit-email"
                      className="col-span-3"
                      value={editMember.email}
                      onChange={(e) => setEditMember({ ...editMember, email: e.target.value })}
                    />
                  </div>
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="edit-nfc" className="text-right">
                      {t("members.form.nfcCard")}
                    </Label>
                    <Input
                      id="edit-nfc"
                      className="col-span-3"
                      value={editMember.nfc_id || ""}
                      onChange={(e) => setEditMember({ ...editMember, nfc_id: e.target.value })}
                    />
                  </div>
                </div>
              )}
              <DialogFooter>
                <Button onClick={handleUpdate}>{t("members.form.save")}</Button>
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
                  <SelectItem value="activo">{t("members.filter.active")}</SelectItem>
                  <SelectItem value="inactivo">{t("members.filter.inactive")}</SelectItem>
                  <SelectItem value="suspendido">{t("members.filter.suspended")}</SelectItem>
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
                          member.status === "activo"
                            ? "success"
                            : member.status === "inactivo"
                              ? "secondary"
                              : "destructive"
                        }
                      >
                        {t(`members.status.${member.status}`)}
                      </Badge>
                    </TableCell>
                    <TableCell>{new Date(member.join_date).toLocaleDateString()}</TableCell>
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
                          <DropdownMenuItem onClick={() => handleEdit(member)}>
                            <Edit className="mr-2 h-4 w-4" />
                            {t("members.actions.edit")}
                          </DropdownMenuItem>
                          <DropdownMenuItem onClick={() => handleEdit(member)}>
                            <CreditCard className="mr-2 h-4 w-4" />
                            {t("members.actions.manageNFC")}
                          </DropdownMenuItem>
                          <DropdownMenuItem onClick={() => deleteMember(member.id)}>
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
          </CardContent>
        </Card>
      </div>
    </div>
  )
}