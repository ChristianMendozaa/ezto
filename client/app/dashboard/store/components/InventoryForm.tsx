"use client";

import React, { useState, ChangeEvent, FormEvent } from "react";
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
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "@/components/ui/select";
import { InventoryMovement } from "../hooks/useInventory";

interface InventoryFormProps {
  onSubmit: (m: Omit<InventoryMovement, 'id'>) => Promise<void>;
}

export const InventoryForm: React.FC<InventoryFormProps> = ({ onSubmit }) => {
  const { t } = useLanguage();
  const [form, setForm] = useState<Omit<InventoryMovement, 'id'>>({
    product_id: "",
    movement_type: 'entrada',
    quantity: 0,
    reason: "",
    reference_id: "",
    movement_date: new Date().toISOString(),
    responsible_id: "",
  });
  const [saving, setSaving] = useState<boolean>(false);

  const handleChange = (
    e: ChangeEvent<HTMLInputElement>
  ) => {
    const { id, value } = e.target;
    setForm(f => ({
      ...f,
      [id]: id === 'quantity' ? Number(value) : value,
    }));
  };

  const handleType = (v: string) => {
    setForm(f => ({ ...f, movement_type: v as 'entrada' | 'salida' }));
  };

  const handleDate = (e: ChangeEvent<HTMLInputElement>) => {
    setForm(f => ({
      ...f,
      movement_date: new Date(e.target.value).toISOString(),
    }));
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setSaving(true);
    await onSubmit(form);
    setSaving(false);
  };

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button>{t('store.inventory.form.add')}</Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>{t('store.inventory.form.addTitle')}</DialogTitle>
          <DialogDescription>{t('store.inventory.form.addDesc')}</DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="grid gap-4 py-4">
          <div className="grid grid-cols-3 gap-4 items-center">
            <Label htmlFor="product_id">{t('store.inventory.form.productId')}</Label>
            <Input id="product_id" value={form.product_id} onChange={handleChange} className="col-span-2" required />
          </div>
          <div className="grid grid-cols-3 gap-4 items-center">
            <Label htmlFor="movement_type">{t('store.inventory.form.type')}</Label>
            <Select value={form.movement_type} onValueChange={handleType}>
              <SelectTrigger className="col-span-2"><SelectValue /></SelectTrigger>
              <SelectContent>
                <SelectItem value="entrada">{t('store.inventory.movement.entrada')}</SelectItem>
                <SelectItem value="salida">{t('store.inventory.movement.salida')}</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div className="grid grid-cols-3 gap-4 items-center">
            <Label htmlFor="quantity">{t('store.inventory.form.qty')}</Label>
            <Input id="quantity" type="number" value={form.quantity} onChange={handleChange} className="col-span-2" required />
          </div>
          <div className="grid grid-cols-3 gap-4 items-center">
            <Label htmlFor="reason">{t('store.inventory.form.reason')}</Label>
            <Input id="reason" value={form.reason} onChange={handleChange} className="col-span-2" required />
          </div>
          <div className="grid grid-cols-3 gap-4 items-center">
            <Label htmlFor="reference_id">{t('store.inventory.form.reference')}</Label>
            <Input id="reference_id" value={form.reference_id} onChange={handleChange} className="col-span-2" required />
          </div>
          <div className="grid grid-cols-3 gap-4 items-center">
            <Label htmlFor="movement_date">{t('store.inventory.form.date')}</Label>
            <Input
              id="movement_date"
              type="datetime-local"
              value={form.movement_date.slice(0,16)}
              onChange={handleDate}
              className="col-span-2"
              required
            />
          </div>
          <div className="grid grid-cols-3 gap-4 items-center">
            <Label htmlFor="responsible_id">{t('store.inventory.form.responsible')}</Label>
            <Input id="responsible_id" value={form.responsible_id} onChange={handleChange} className="col-span-2" required />
          </div>

          <DialogFooter>
            <Button type="submit" disabled={saving}>{t('store.inventory.form.saveBtn')}</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
};
