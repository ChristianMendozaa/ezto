"use client";

import { useState, useEffect } from "react";
import { useLanguage } from "@/lib/hooks/use-language";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Plus, MoreHorizontal, Trash2 } from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

interface Member {
  id: string;
  name: string;
  email: string;
  join_date: string;
  nfc_id: string;
  status: string;
}

export default function MembersPage() {
  const { t } = useLanguage();
  const [members, setMembers] = useState<Member[]>([]);
  const [isAddMemberOpen, setIsAddMemberOpen] = useState(false);
  const [newMember, setNewMember] = useState<Partial<Member>>({ name: "", email: "" });
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const getAuthToken = () => localStorage.getItem("token") || "";

  useEffect(() => {
    const fetchMembers = async () => {
      try {
        setLoading(true);
        const response = await fetch("http://localhost:8005/members", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${getAuthToken()}`,
            "Content-Type": "application/json",
          },
          credentials: "include",
        });
  
        if (!response.ok) throw new Error("Error en la autenticación o petición");
  
        const data = await response.json();
  
        // Asegurar que cada miembro tenga un ID válido
        const membersWithId = data.map((doc: any) => ({
          id: doc.id || crypto.randomUUID(),  // Usa el ID del documento o genera uno temporal
          ...doc
        }));
  
        setMembers(membersWithId);
      } catch (error) {
        console.error("Error fetching members:", error);
        setErrorMessage("Hubo un error al obtener los miembros.");
      } finally {
        setLoading(false);
      }
    };
  
    fetchMembers();
  }, []);
  

  const handleAddMember = async () => {
    try {
      // Si tienes un id específico o quieres que Firebase lo maneje,
      const generatedId = crypto.randomUUID();

      // Crear los datos del nuevo miembro
      const newMemberData = {
        id: generatedId,  // Establecemos el ID generado
        ...newMember,
        status: "activo",  // Valor por defecto
        join_date: new Date().toISOString(),  // Fecha en formato ISO 8601
      };
      const response = await fetch("http://localhost:8005/members", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${getAuthToken()}`,
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify(newMemberData),
      });
  
      if (!response.ok) throw new Error("Error al agregar miembro");
  
      const newEntry: Member = await response.json();
      setMembers((prevMembers) => [...prevMembers, newEntry]);
      setIsAddMemberOpen(false);
      setSuccessMessage("Miembro agregado exitosamente.");
    } catch (error) {
      console.error("Error adding member:", error);
      setErrorMessage("");
    }
  };

  const handleDeleteMember = async (id: string) => {
    try {
      const response = await fetch(`http://localhost:8005/members/${id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${getAuthToken()}`,
          "Content-Type": "application/json",
        },
        credentials: "include",
      });

      if (!response.ok) throw new Error("Error al eliminar miembro");

      setMembers((prevMembers) => prevMembers.filter((member) => member.id !== id));
      setSuccessMessage("Miembro eliminado exitosamente.");
    } catch (error) {
      console.error("Error deleting member:", error);
      setErrorMessage("Hubo un error al eliminar el miembro.");
    }
  };

  return (
    <div className="flex-1 space-y-4 p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">{t("members.title")}</h2>
        <Button onClick={() => setIsAddMemberOpen(true)}>
          <Plus className="mr-2 h-4 w-4" />
          {t("members.add")}
        </Button>
      </div>

      {errorMessage && <p className="text-red-500">{errorMessage}</p>}
      {successMessage && <p className="text-green-500">{successMessage}</p>}
      {loading && <p className="text-center text-gray-500">Cargando miembros...</p>}

      <Dialog open={isAddMemberOpen} onOpenChange={setIsAddMemberOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{t("members.addMember")}</DialogTitle>
            <DialogDescription>{t("members.addMemberDescription")}</DialogDescription>
          </DialogHeader>
          <Input
            placeholder={t("members.form.name")}
            onChange={(e) => setNewMember({ ...newMember, name: e.target.value })}
          />
          <Input
            placeholder={t("members.form.email")}
            onChange={(e) => setNewMember({ ...newMember, email: e.target.value })}
          />
          <DialogFooter>
            <Button onClick={handleAddMember}>{t("members.form.save")}</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    
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
          {members.length > 0 ? (
            members.map((member) => (
              <TableRow key={member.id}>
                <TableCell>{member.name}</TableCell>
                <TableCell>{member.email}</TableCell>
                <TableCell>
                  <Badge
                    className={`
                      ${member.status === "activo" ? "bg-green-500 text-white" : ""}
                      ${member.status === "inactivo" ? "bg-red-500 text-white" : ""}
                      ${member.status === "suspendido" ? "bg-gray-500 text-white" : ""}
                    `}
                  >
                    {t(`${member.status}`)}
                  </Badge>
                </TableCell>
                <TableCell>{new Date(member.join_date).toISOString().split("T")[0]}</TableCell>
                <TableCell className="text-right">
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="ghost" className="h-8 w-8 p-0">
                        <MoreHorizontal className="h-4 w-4" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuLabel>{t("members.actions.title")}</DropdownMenuLabel>
                      <DropdownMenuItem onClick={() => handleDeleteMember(member.id)}>
                        <Trash2 className="mr-2 h-4 w-4" /> {t("members.actions.delete")}
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </TableCell>
              </TableRow>
            ))
          ) : (
            <TableRow>
              <TableCell colSpan={3} className="text-center">
                {t("members.noMembers")}
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </div>
  );
}
