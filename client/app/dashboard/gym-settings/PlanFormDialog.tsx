import React, { useState, useEffect } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { MembershipPlanInput } from "@/hooks/useMembershipPlans";

interface PlanFormDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  initialData?: MembershipPlanInput;
  onSave: (data: MembershipPlanInput) => Promise<boolean>;
  title: string;
  description?: string;
}

export function PlanFormDialog({
  open,
  onOpenChange,
  initialData,
  onSave,
  title,
  description,
}: PlanFormDialogProps) {
  const [form, setForm] = useState<MembershipPlanInput>({
    name: "",
    description: "",
    capacity: 1,
    duration_months: 1,
    price: 0,
    services_offered: [],
  });
  const [servicesInput, setServicesInput] = useState("");

  useEffect(() => {
    if (initialData) {
      setForm(initialData);
      setServicesInput(initialData.services_offered.join(", "));
    } else {
      setForm({ name: "", description: "", capacity: 1, duration_months: 1, price: 0, services_offered: [] });
      setServicesInput("");
    }
  }, [initialData]);

  const handleChange = (field: keyof MembershipPlanInput, value: string | number) => {
    setForm(prev => ({ ...prev, [field]: value }));
  };

  const handleSave = async () => {
    const services = servicesInput.split(",").map(s => s.trim()).filter(Boolean);
    const data: MembershipPlanInput = { ...form, services_offered: services };
    const ok = await onSave(data);
    if (ok) onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-lg">
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
          {description && <DialogDescription>{description}</DialogDescription>}
        </DialogHeader>
        <div className="grid gap-4 py-4">
          {[
            { key: "name", label: "Nombre", type: "text" },
            { key: "description", label: "Descripción", type: "text" },
            { key: "capacity", label: "Capacidad", type: "number" },
            { key: "duration_months", label: "Duración (meses)", type: "number" },
            { key: "price", label: "Precio", type: "number" },
          ].map(({ key, label, type }) => (
            <div key={key} className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor={key} className="text-right">{label}</Label>
              <Input
                id={key}
                type={type}
                className="col-span-3"
                value={(form as any)[key]}
                onChange={e => handleChange(key as any, type === "number" ? Number(e.target.value) : e.target.value)}
              />
            </div>
          ))}
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="services" className="text-right">Características</Label>
            <Textarea
              id="services"
              className="col-span-3"
              placeholder="Servicio1, Servicio2, ..."
              value={servicesInput}
              onChange={e => setServicesInput(e.target.value)}
            />
          </div>
        </div>
        <DialogFooter>
          <Button onClick={handleSave}>{initialData ? "Actualizar" : "Crear"}</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}