
// components/SupplierForm.tsx
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
import { Button } from "@/components/ui/button";
import { Supplier } from "../hooks/useSuppliers";

export interface SupplierFormData {
  name: string;
  contact_email: string;
  phone: string;
  address: string;
  tax_id: string;
  payment_terms: string;
  status: string;
}

interface SupplierFormProps {
  onSubmit: (data: Omit<Supplier, 'id' | 'created_at' | 'last_updated' | 'products_offered'>) => Promise<void>;
  defaultValues?: Partial<SupplierFormData>;
  editMode?: boolean;
}

export const SupplierForm: React.FC<SupplierFormProps> = ({ onSubmit, defaultValues, editMode }) => {
  const { t } = useLanguage();
  const [form, setForm] = useState<SupplierFormData>({
    name: "",
    contact_email: "",
    phone: "",
    address: "",
    tax_id: "",
    payment_terms: "",
    status: "",
  });
  const [saving, setSaving] = useState(false);

  React.useEffect(() => {
    if (defaultValues) setForm(prev => ({ ...prev, ...defaultValues }));
  }, [defaultValues]);

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { id, value } = e.target;
    setForm(prev => ({ ...prev, [id]: value }));
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setSaving(true);
    await onSubmit(form as any);
    setSaving(false);
  };

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button>{editMode ? t('store.suppliers.form.edit') : t('store.suppliers.form.add')}</Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>{editMode ? t('store.suppliers.form.editTitle') : t('store.suppliers.form.addTitle')}</DialogTitle>
          <DialogDescription>{t('store.suppliers.form.description')}</DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="grid gap-4 py-4">
          {['name','contact_email','phone','address','tax_id','payment_terms','status'].map(field => (
            <div key={field} className="grid grid-cols-3 items-center gap-4">
              <Label htmlFor={field}>{t(`store.suppliers.form.${field}`)}</Label>
              <Input id={field} value={(form as any)[field]} onChange={handleChange} className="col-span-2" required />
            </div>
          ))}
          <DialogFooter>
            <Button type="submit" disabled={saving}>{editMode ? t('store.suppliers.form.updateBtn') : t('store.suppliers.form.saveBtn')}</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
};
