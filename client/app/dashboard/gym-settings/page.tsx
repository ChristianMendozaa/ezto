// app/dashboard/gym-settings/page.tsx
"use client";

import { useState } from "react";
import { useLanguage } from "@/lib/hooks/use-language";
import { useMembershipPlans, MembershipPlanInput } from "@/hooks/useMembershipPlans";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Plus, Edit, Trash2, Search } from "lucide-react";

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

export default function GymSettingsPage() {
  const { t } = useLanguage();
  const { plans, loading, error, createPlan, deletePlan, refetch } = useMembershipPlans();

  // pestaña memberships
  const [search, setSearch] = useState("");
  const [isAddOpen, setIsAddOpen] = useState(false);

  // formulario controlado para new plan
  const [form, setForm] = useState<MembershipPlanInput>({
    name: "",
    description: "",
    capacity: 1,
    duration_months: 1,
    price: 0,
    services_offered: [],
  });
  const [servicesInput, setServicesInput] = useState("");

  const filtered = plans.filter(p =>
    p.name.toLowerCase().includes(search.toLowerCase())
  );

  const onAddSubmit = async () => {
    const services = servicesInput
      .split(",")
      .map(s => s.trim())
      .filter(Boolean);

    const data: MembershipPlanInput = {
      ...form,
      services_offered: services,
    };

    if (await createPlan(data)) {
      setIsAddOpen(false);
      refetch();
      setForm({
        name: "",
        description: "",
        capacity: 1,
        duration_months: 1,
        price: 0,
        services_offered: [],
      });
      setServicesInput("");
    }
  };

  return (
    <div className="flex-1 space-y-4 p-8 pt-6">
      <h2 className="text-3xl font-bold tracking-tight">
        {t("gymSettings.title", "Configuración del Gimnasio")}
      </h2>
      <Tabs defaultValue="profile" className="space-y-4">
        <TabsList>
          <TabsTrigger value="profile">
            {t("gymSettings.tabs.profile", "Perfil del Gimnasio")}
          </TabsTrigger>
          <TabsTrigger value="memberships">
            {t("gymSettings.tabs.memberships", "Membresías")}
          </TabsTrigger>
        </TabsList>

        {/* PERFIL */}
        <TabsContent value="profile">
          <Card>
            <CardHeader>
              <CardTitle>
                {t("gymSettings.profile.title", "Perfil del Gimnasio")}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <form className="space-y-4">
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="gymName" className="text-right">
                    {t("gymSettings.profile.gymName", "Nombre")}
                  </Label>
                  <Input id="gymName" className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="logo" className="text-right">
                    {t("gymSettings.profile.logo", "Logo")}
                  </Label>
                  <Input id="logo" type="file" className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="address" className="text-right">
                    {t("gymSettings.profile.address", "Dirección")}
                  </Label>
                  <Textarea id="address" className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="openingHours" className="text-right">
                    {t("gymSettings.profile.openingHours", "Horario")}
                  </Label>
                  <Textarea
                    id="openingHours"
                    className="col-span-3"
                    placeholder={t(
                      "gymSettings.profile.openingHoursPlaceholder",
                      "Lun-Vie: 6am-10pm\nSáb-Dom: 8am-8pm"
                    )}
                  />
                </div>
                <div className="flex justify-end">
                  <Button type="submit">
                    {t("gymSettings.profile.save", "Guardar")}
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        </TabsContent>

        {/* MEMBRESÍAS */}
        <TabsContent value="memberships">
          <Card>
            <CardHeader className="flex justify-between items-center">
              <CardTitle>
                {t("gymSettings.memberships.title", "Membresías")}
              </CardTitle>
              <Button onClick={() => setIsAddOpen(true)}>
                <Plus className="mr-2 h-4 w-4" />
                {t("gymSettings.memberships.add", "Agregar")}
              </Button>
            </CardHeader>

            <CardContent>
              <div className="flex justify-between mb-4">
                <Input
                  placeholder={t("gymSettings.memberships.search", "Buscar...")}
                  value={search}
                  onChange={e => setSearch(e.target.value)}
                  className="max-w-sm"
                />
                <Button
                  variant="outline"
                  size="icon"
                  onClick={() => { setSearch(""); refetch(); }}
                >
                  <Search className="h-4 w-4" />
                </Button>
              </div>

              {loading && <p>{t("loading", "Cargando…")}</p>}
              {error && <p className="text-destructive">{error}</p>}
              {!loading && filtered.length === 0 && (
                <p>{t("gymSettings.memberships.empty", "Sin resultados")}</p>
              )}

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
                      <TableCell>{plan.duration_months} {t("month", "month")}</TableCell>
                      <TableCell>{plan.services_offered.join(", ")}</TableCell>
                      <TableCell className="text-right space-x-2">
                        <Button variant="ghost" size="icon">
                          <Edit className="h-4 w-4" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={() => deletePlan(plan.id!).then(refetch)}
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>

          {/* DIALOG AGREGAR NUEVA MEMBERSHIP */}
          <Dialog open={isAddOpen} onOpenChange={setIsAddOpen}>
            <DialogTrigger />
            <DialogContent className="sm:max-w-lg">
              <DialogHeader>
                <DialogTitle>
                  {t("gymSettings.memberships.addTitle", "Nueva Membresía")}
                </DialogTitle>
                <DialogDescription>
                  {t(
                    "gymSettings.memberships.addDescription",
                    "Completa los datos"
                  )}
                </DialogDescription>
              </DialogHeader>

              <div className="grid gap-4">
                {[
                  { key: "name", label: t("gymSettings.memberships.form.name", "Nombre"), type: "text" },
                  { key: "description", label: t("gymSettings.memberships.form.description", "Descripción"), type: "text" },
                  { key: "capacity", label: t("gymSettings.memberships.form.capacity", "Capacidad"), type: "number" },
                  { key: "duration_months", label: t("gymSettings.memberships.form.duration", "Duración (meses)"), type: "number" },
                  { key: "price", label: t("gymSettings.memberships.form.price", "Precio"), type: "number" },
                ].map(({ key, label, type }) => (
                  <div key={key} className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor={key} className="text-right">{label}</Label>
                    <Input
                      id={key}
                      type={type}
                      className="col-span-3"
                      value={(form as any)[key]}
                      onChange={e =>
                        setForm(f => ({
                          ...f,
                          [key]: type === "number" ? Number(e.target.value) : e.target.value
                        }))
                      }
                    />
                  </div>
                ))}

                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="services" className="text-right">
                    {t("gymSettings.memberships.form.services", "Características")}
                  </Label>
                  <Textarea
                    id="services"
                    className="col-span-3"
                    placeholder="Gym, Pool, Spa"
                    value={servicesInput}
                    onChange={e => setServicesInput(e.target.value)}
                  />
                </div>
              </div>

              <DialogFooter>
                <Button onClick={onAddSubmit} disabled={loading}>
                  {loading
                    ? t("gymSettings.memberships.form.saving", "Guardando…")
                    : t("gymSettings.memberships.form.save", "Guardar")}
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </TabsContent>
      </Tabs>
    </div>
  );
}
