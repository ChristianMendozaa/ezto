// components/PurchaseForm.tsx
"use client";

import React, { ChangeEvent, FormEvent, useState } from "react";
import { useLanguage } from "@/lib/hooks/use-language";
import {
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Purchase, PurchaseItem } from "../hooks/usePurchases";

export interface PurchaseFormData {
  client_id: string;
  items: PurchaseItem[]; // Simple JSON string input
  payment_method: string;
  notes: string;
  total_amount: string;
  tax_amount: string;
  sale_date: string;
  seller_id: string;
  invoice_number: string;
  status: string;
}

interface PurchaseFormProps {
  onSubmit: (data: Omit<Purchase, 'sale_id'>) => Promise<void>;
  defaultValues?: Partial<PurchaseFormData>;
  editMode?: boolean;
}

export const PurchaseForm: React.FC<PurchaseFormProps> = ({ onSubmit, defaultValues, editMode }) => {
  const { t } = useLanguage();
  const [form, setForm] = useState<PurchaseFormData>({
    client_id: "",
    items: [],
    payment_method: "",
    notes: "",
    total_amount: "",
    tax_amount: "",
    sale_date: new Date().toISOString(),
    seller_id: "",
    invoice_number: "",
    status: "",
  });
  const [saving, setSaving] = useState(false);

  React.useEffect(() => {
    if (defaultValues) {
      setForm(prev => ({ ...prev, ...defaultValues }));
    }
  }, [defaultValues]);

  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { id, value } = e.target;
    setForm(prev => ({ ...prev, [id]: value }));
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setSaving(true);
    // If items edited manually, parse JSON
    const data: Omit<Purchase, 'sale_id'> = {
      ...form,
      items: typeof form.items === 'string' ? JSON.parse(form.items as any) : form.items,
      total_amount: parseFloat(form.total_amount),
      tax_amount: parseFloat(form.tax_amount),
    } as any;
    await onSubmit(data);
    setSaving(false);
  };

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button>{editMode ? t('store.purchases.form.edit') : t('store.purchases.form.add')}</Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-lg">
        <DialogHeader>
          <DialogTitle>{editMode ? t('store.purchases.form.editTitle') : t('store.purchases.form.addTitle')}</DialogTitle>
          <DialogDescription>{t('store.purchases.form.description')}</DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="grid gap-4 py-4">
          <div className="grid grid-cols-3 items-center gap-4">
            <Label htmlFor="client_id">{t('store.purchases.form.clientId')}</Label>
            <Input id="client_id" value={form.client_id} onChange={handleChange} className="col-span-2" required />
          </div>
          <div className="grid grid-cols-3 items-center gap-4">
            <Label htmlFor="items">{t('store.purchases.form.items')}</Label>
            <Textarea id="items" value={JSON.stringify(form.items)} onChange={handleChange} className="col-span-2" required />
          </div>
          {/* Repeat similar blocks for payment_method, notes, total_amount, tax_amount, sale_date, seller_id, invoice_number, status */}
          <DialogFooter>
            <Button type="submit" disabled={saving}>{editMode ? t('store.purchases.form.updateBtn') : t('store.purchases.form.saveBtn')}</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
};