"use client"

import React, { useState } from "react";
import { useLanguage } from "@/lib/hooks/use-language";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Search, Plus, Edit, Trash2 } from "lucide-react";
import { usePersonal, Personal, PersonalInput } from "@/hooks/usePersonal";
import { StaffFormDialog } from "./StaffFormDialog";

export default function StaffPage() {
  const { t } = useLanguage();
  const { personals, loading, error, createPersonal, updatePersonal, deletePersonal, fetchPersonals } = usePersonal();

  const [dialogOpen, setDialogOpen] = useState(false);
  const [selectedStaff, setSelectedStaff] = useState<Personal | undefined>(undefined);

  const openAdd = () => {
    setSelectedStaff(undefined);
    setDialogOpen(true);
  };
  const openEdit = (p: Personal) => {
    setSelectedStaff(p);
    setDialogOpen(true);
  };
  const onSave = async (data: PersonalInput) => {
    if (selectedStaff) {
      return await updatePersonal(selectedStaff.id, data);
    }
    return await createPersonal(data);
  };

  return (
    <div className="p-8 space-y-4">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">{t("staff.title")}</h1>
        <Button onClick={openAdd}>
          <Plus className="mr-2 h-4 w-4" /> {t("staff.add")}
        </Button>
      </div>
      <div className="flex items-center space-x-2">
        <Input placeholder={t("staff.search")} className="max-w-sm" />
        <Button onClick={() => fetchPersonals()}>{t("staff.refresh")}</Button>
      </div>
      <StaffFormDialog
        open={dialogOpen}
        onOpenChange={setDialogOpen}
        initialData={selectedStaff}
        onSave={onSave}
        title={selectedStaff ? t("staff.editStaff") : t("staff.addStaff")}
        description={selectedStaff ? t("staff.editStaffDescription") : t("staff.addStaffDescription")}
      />
      {error && <div className="text-red-600">{error}</div>}
      {loading ? (
        <div>{t("staff.loading")}</div>
      ) : (
        <Card>
          <CardHeader>
            <CardTitle>{t("staff.staffList")}</CardTitle>
          </CardHeader>
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
                      <Badge variant={
                        p.access_level === "full" ? "default" :
                        p.access_level === "standard" ? "secondary" : "outline"
                      }>
                        {t(`staff.accessLevels.${p.access_level}`)}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-right">
                      <Button variant="ghost" size="icon" onClick={() => openEdit(p)}>
                        <Edit className="h-4 w-4 text-blue-600" />
                      </Button>
                      <Button variant="ghost" size="icon" onClick={() => deletePersonal(p.id)}>
                        <Trash2 className="h-4 w-4 text-red-600" />
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
