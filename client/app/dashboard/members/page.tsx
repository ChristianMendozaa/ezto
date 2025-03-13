"use client";

import { useState, useEffect } from "react";
import { useLanguage } from "@/lib/hooks/use-language";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
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

export default function MembersPage() {
  const { t } = useLanguage();
  const [members, setMembers] = useState([]);
  const [isAddMemberOpen, setIsAddMemberOpen] = useState(false);
  const [newMember, setNewMember] = useState({ name: "", email: "" });

  // Obtener el token desde localStorage (o usar cookies si es necesario)
  const getAuthToken = () => {
    return localStorage.getItem("token") || "";
  };

  useEffect(() => {
    const fetchMembers = async () => {
      try {
        const response = await fetch("http://localhost:8005/members", {
          method: "GET",
          headers: {
            "Authorization": `Bearer ${getAuthToken()}`,
            "Content-Type": "application/json",
          },
          credentials: "include", // Si el backend usa cookies para autenticación
        });

        if (!response.ok) {
          throw new Error("Error en la autenticación o petición");
        }

        const data = await response.json();
        setMembers(Array.isArray(data) ? data : []); // Evita `map is not a function`
      } catch (error) {
        console.error("Error fetching members:", error);
      }
    };

    fetchMembers();
  }, []);

  const handleAddMember = async () => {
    try {
      const response = await fetch("http://localhost:8005/members", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${getAuthToken()}`,
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify(newMember),
      });

      if (!response.ok) throw new Error("Error al agregar miembro");

      const newEntry = await response.json();
      setMembers([...members, newEntry]);
      setIsAddMemberOpen(false);
    } catch (error) {
      console.error("Error adding member:", error);
    }
  };

  const handleDeleteMember = async (id) => {
    try {
      const response = await fetch(`http://localhost:8005/members/${id}`, {
        method: "DELETE",
        headers: {
          "Authorization": `Bearer ${getAuthToken()}`,
          "Content-Type": "application/json",
        },
        credentials: "include",
      });

      if (!response.ok) throw new Error("Error al eliminar miembro");

      setMembers(members.filter((member) => member.id !== id));
    } catch (error) {
      console.error("Error deleting member:", error);
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

      {/* Modal para agregar miembro */}
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

      {/* Tabla de miembros */}
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>{t("members.table.name")}</TableHead>
            <TableHead>{t("members.table.email")}</TableHead>
            <TableHead className="text-right">{t("members.table.actions")}</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {members.length > 0 ? (
            members.map((member) => (
              <TableRow key={member.id}>
                <TableCell>{member.name}</TableCell>
                <TableCell>{member.email}</TableCell>
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
