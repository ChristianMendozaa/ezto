"use client";

import React, { useState } from "react";
import { useLanguage } from "@/lib/hooks/use-language";
import { useMembershipPlans, MembershipPlanInput } from "@/hooks/useMembershipPlans";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Plus, Edit, Trash2, Search } from "lucide-react";
import { PlanFormDialog } from "./PlanFormDialog";

export default function GymSettingsPage() {
  const { t } = useLanguage();
  const { plans, loading, error, createPlan, deletePlan, updatePlan, refetch } = useMembershipPlans();
  const [search, setSearch] = useState("");
  const [dialogOpen, setDialogOpen] = useState(false);
  const [selectedPlan, setSelectedPlan] = useState<MembershipPlanInput & { id?: string } | undefined>(undefined);

  const filtered = plans.filter(p => p.name.toLowerCase().includes(search.toLowerCase()));

  const openAdd = () => {
    setSelectedPlan(undefined);
    setDialogOpen(true);
  };

  const openEdit = (plan: any) => {
    setSelectedPlan(plan);
    setDialogOpen(true);
  };

  const onSave = async (data: MembershipPlanInput) => {
    if (selectedPlan && (selectedPlan as any).id) {
      await updatePlan((selectedPlan as any).id, data);
    } else {
      await createPlan(data);
    }
    refetch();
    return true;
  };

  return (
    <div className="flex-1 space-y-4 p-8 pt-6">
      <h2 className="text-3xl font-bold tracking-tight">{t("gymSettings.title", "Configuración del Gimnasio")}</h2>
      <Tabs defaultValue="memberships" className="space-y-4">
        <TabsList>
          <TabsTrigger value="profile">{t("gymSettings.tabs.profile", "Perfil")}</TabsTrigger>
          <TabsTrigger value="memberships">{t("gymSettings.tabs.memberships", "Membresías")}</TabsTrigger>
        </TabsList>
        <TabsContent value="profile">{/* ... perfil unchanged ... */}</TabsContent>
        <TabsContent value="memberships">
          <Card>
            <CardHeader className="flex justify-between items-center">
              <CardTitle>{t("gymSettings.memberships.title", "Membresías")}</CardTitle>
              <Button onClick={openAdd}><Plus className="mr-2 h-4 w-4" />{t("gymSettings.memberships.add", "Agregar")}</Button>
            </CardHeader>
            <CardContent>
              <div className="flex justify-between mb-4">
                <Input placeholder={t("gymSettings.memberships.search", "Buscar...")} value={search} onChange={e => setSearch(e.target.value)} className="max-w-sm" />
                <Button variant="outline" size="icon" onClick={() => { setSearch(""); refetch(); }}><Search className="h-4 w-4" /></Button>
              </div>
              {loading && <p>{t("loading", "Cargando…")}</p>}
              {error && <p className="text-destructive">{error}</p>}
              {filtered.length === 0 && !loading && <p>{t("gymSettings.memberships.empty", "Sin resultados")}</p>}
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>{t("gymSettings.memberships.table.name", "Nombre")}</TableHead>
                    <TableHead>{t("gymSettings.memberships.table.price", "Precio")}</TableHead>
                    <TableHead>{t("gymSettings.memberships.table.duration", "Duración")}</TableHead>
                    <TableHead>{t("gymSettings.memberships.table.features", "Características")}</TableHead>
                    <TableHead className="text-right">{t("actions", "Acciones")}</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filtered.map(plan => (
                    <TableRow key={plan.id}>
                      <TableCell>{plan.name}</TableCell>
                      <TableCell>${plan.price.toFixed(2)}</TableCell>
                      <TableCell>{plan.duration_months} {t("month", "mes(es)")}</TableCell>
                      <TableCell>{plan.services_offered.join(", ")}</TableCell>
                      <TableCell className="text-right space-x-2">
                        <Button variant="ghost" size="icon" onClick={() => openEdit(plan)}><Edit className="h-4 w-4" /></Button>
                        <Button variant="ghost" size="icon" onClick={() => deletePlan(plan.id).then(refetch)}><Trash2 className="h-4 w-4" /></Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>

          <PlanFormDialog
            open={dialogOpen}
            onOpenChange={setDialogOpen}
            initialData={selectedPlan}
            onSave={onSave}
            title={selectedPlan ? t("gymSettings.memberships.editTitle", "Editar Membresía") : t("gymSettings.memberships.addTitle", "Nueva Membresía")}
            description={selectedPlan ? t("gymSettings.memberships.editDescription", "Modifica los datos") : t("gymSettings.memberships.addDescription", "Completa los datos")}
          />
        </TabsContent>
      </Tabs>
    </div>
  );
}