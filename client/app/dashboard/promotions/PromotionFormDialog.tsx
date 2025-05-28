// PromotionFormDialog.tsx
import React, { useState, useEffect } from "react";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { PromotionInput } from "@/hooks/usePromotions";

interface PromotionFormDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  initialData?: PromotionInput;
  onSave: (data: PromotionInput) => Promise<boolean>;
  title: string;
  description?: string;
}

export function PromotionFormDialog({
  open,
  onOpenChange,
  initialData,
  onSave,
  title,
  description,
}: PromotionFormDialogProps) {
  // Estados del formulario
  const [name, setName] = useState(initialData?.name ?? "");
  const [descriptionText, setDescriptionText] = useState(initialData?.description ?? "");
  const [startDate, setStartDate] = useState(initialData?.start_date ?? "");
  const [endDate, setEndDate] = useState(initialData?.end_date ?? "");
  const [discountType, setDiscountType] = useState<"percentage" | "fixed" | "free_month">(
    initialData?.discount_type ?? "percentage"
  );
  const [discountValue, setDiscountValue] = useState<number>(initialData?.discount_value ?? 0);
  const [promoCode, setPromoCode] = useState(initialData?.promo_code ?? "");
  const [autoApply, setAutoApply] = useState(initialData?.auto_apply ?? false);
  const [applicableTo, setApplicableTo] = useState<"all_users" | "new_users" | "loyal_users" | "specific_plan">(
    initialData?.applicable_to ?? "all_users"
  );
  const [status, setStatus] = useState<boolean>(initialData?.status ?? true);

  // Reset form cuando initialData cambia
  useEffect(() => {
    setName(initialData?.name ?? "");
    setDescriptionText(initialData?.description ?? "");
    setStartDate(initialData?.start_date ?? "");
    setEndDate(initialData?.end_date ?? "");
    setDiscountType(initialData?.discount_type ?? "percentage");
    setDiscountValue(initialData?.discount_value ?? 0);
    setPromoCode(initialData?.promo_code ?? "");
    setAutoApply(initialData?.auto_apply ?? false);
    setApplicableTo(initialData?.applicable_to ?? "all_users");
    setStatus(initialData?.status ?? true);
  }, [initialData]);

  const handleSave = async () => {
    const data: PromotionInput = {
      name,
      description: descriptionText,
      start_date: startDate,
      end_date: endDate,
      discount_type: discountType,
      discount_value: discountValue,
      promo_code: promoCode || undefined,
      auto_apply: autoApply,
      applicable_to: applicableTo,
      status,
    };
    const ok = await onSave(data);
    if (ok) {
      onOpenChange(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[30vw] max-h-[80vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
          {description && <DialogDescription>{description}</DialogDescription>}
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <Label>Nombre</Label>
          <Input value={name} onChange={(e) => setName(e.target.value)} />
          
          <Label>Descripción</Label>
          <Textarea value={descriptionText} onChange={(e) => setDescriptionText(e.target.value)} />
          
          <Label>Fecha de inicio</Label>
          <Input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
          
          <Label>Fecha de fin</Label>
          <Input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
          
          <Label>Tipo de descuento</Label>
          <Select value={discountType} onValueChange={(v) => setDiscountType(v as any)}>
            <SelectTrigger><SelectValue placeholder="Seleccionar" /></SelectTrigger>
            <SelectContent>
              <SelectItem value="percentage">Porcentaje</SelectItem>
              <SelectItem value="fixed">Fijo</SelectItem>
              <SelectItem value="free_month">Mes gratis</SelectItem>
            </SelectContent>
          </Select>
          
          <Label>Valor de descuento</Label>
          <Input type="number" value={discountValue} onChange={(e) => setDiscountValue(Number(e.target.value))} />
          
          <Label>Código promo</Label>
          <Input value={promoCode} onChange={(e) => setPromoCode(e.target.value)} />
          
          <Label>Aplicación automática</Label>
          <Select value={autoApply.toString()} onValueChange={(v) => setAutoApply(v === "true")}>
            <SelectTrigger><SelectValue placeholder="Seleccionar" /></SelectTrigger>
            <SelectContent>
              <SelectItem value="true">Sí</SelectItem>
              <SelectItem value="false">No</SelectItem>
            </SelectContent>
          </Select>
          
          <Label>Aplicable a</Label>
          <Select value={applicableTo} onValueChange={(v) => setApplicableTo(v as any)}>
            <SelectTrigger><SelectValue placeholder="Seleccionar" /></SelectTrigger>
            <SelectContent>
              <SelectItem value="all_users">Todos los usuarios</SelectItem>
              <SelectItem value="new_users">Nuevos usuarios</SelectItem>
              <SelectItem value="loyal_users">Usuarios leales</SelectItem>
              <SelectItem value="specific_plan">Plan específico</SelectItem>
            </SelectContent>
          </Select>
          
          <Label>Estado</Label>
          <Select value={status ? "true" : "false"} onValueChange={(v) => setStatus(v === "true")}> 
            <SelectTrigger><SelectValue placeholder="Seleccionar" /></SelectTrigger>
            <SelectContent>
              <SelectItem value="true">Activo</SelectItem>
              <SelectItem value="false">Inactivo</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <DialogFooter>
          <Button onClick={handleSave}>{initialData ? "Actualizar" : "Crear"}</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}