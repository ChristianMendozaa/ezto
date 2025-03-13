// store/components/ProductForm.tsx
"use client";

import React, { ChangeEvent, FormEvent, useState } from "react";
import { useLanguage } from "@/lib/hooks/use-language";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

export interface ProductFormData {
  name: string;
  sku: string;
  category: string;
  purchase_price: string;
  sale_price: string;
  current_stock: string;
  min_stock: string;
  supplier_id: string;
  description: string;
  expiration_date: string;
  barcode: string;
  status: string;
}

interface ProductFormProps {
  onSubmit: (data: ProductFormData, productImage: File | null) => Promise<void>;
}

export const ProductForm: React.FC<ProductFormProps> = ({ onSubmit }) => {
  const { t } = useLanguage();
  const [formData, setFormData] = useState<ProductFormData>({
    name: "",
    sku: "",
    category: "",
    purchase_price: "",
    sale_price: "",
    current_stock: "",
    min_stock: "",
    supplier_id: "",
    description: "",
    expiration_date: "",
    barcode: "",
    status: "activo",
  });
  const [productImage, setProductImage] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { id, value } = e.target;
    setFormData(prev => ({ ...prev, [id]: value }));
  };

  const handleCategoryChange = (value: string) => {
    setFormData(prev => ({ ...prev, category: value }));
  };

  const handleImageChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setProductImage(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    await onSubmit(formData, productImage);
    setLoading(false);
  };

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button>
          {t("store.catalog.addProduct")}
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>{t("store.catalog.addProductTitle")}</DialogTitle>
          <DialogDescription>{t("store.catalog.addProductDescription")}</DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit}>
          <div className="grid gap-4 py-4">
            {/* Nombre */}
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="name" className="text-right">{t("store.catalog.form.name")}</Label>
              <Input id="name" value={formData.name} onChange={handleInputChange} className="col-span-3" required />
            </div>
            {/* SKU */}
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="sku" className="text-right">SKU</Label>
              <Input id="sku" value={formData.sku} onChange={handleInputChange} className="col-span-3" required />
            </div>
            {/* Categoría */}
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="category" className="text-right">{t("store.catalog.form.category")}</Label>
              <Select value={formData.category} onValueChange={handleCategoryChange}>
                <SelectTrigger className="col-span-3">
                  <SelectValue placeholder={t("store.catalog.form.selectCategory")} />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="suplementos">{t("store.catalog.categories.suplementos")}</SelectItem>
                  <SelectItem value="ropa">{t("store.catalog.categories.ropa")}</SelectItem>
                  <SelectItem value="equipo">{t("store.catalog.categories.equipo")}</SelectItem>
                  <SelectItem value="accesorios">{t("store.catalog.categories.accesorios")}</SelectItem>
                  <SelectItem value="bebidas">{t("store.catalog.categories.bebidas")}</SelectItem>
                  <SelectItem value="otros">{t("store.catalog.categories.otros")}</SelectItem>
                </SelectContent>
              </Select>
            </div>
            {/* Supplier ID */}
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="supplier_id" className="text-right">Supplier ID</Label>
              <Input id="supplier_id" value={formData.supplier_id} onChange={handleInputChange} className="col-span-3" required />
            </div>
            {/* Precio Compra */}
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="purchase_price" className="text-right">{t("store.catalog.form.purchasePrice")}</Label>
              <Input id="purchase_price" type="number" value={formData.purchase_price} onChange={handleInputChange} className="col-span-3" required />
            </div>
            {/* Precio Venta */}
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="sale_price" className="text-right">{t("store.catalog.form.price")}</Label>
              <Input id="sale_price" type="number" value={formData.sale_price} onChange={handleInputChange} className="col-span-3" required />
            </div>
            {/* Stock actual */}
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="current_stock" className="text-right">{t("store.catalog.form.stock")}</Label>
              <Input id="current_stock" type="number" value={formData.current_stock} onChange={handleInputChange} className="col-span-3" required />
            </div>
            {/* Stock Mínimo */}
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="min_stock" className="text-right">{t("store.catalog.form.minStock")}</Label>
              <Input id="min_stock" type="number" value={formData.min_stock} onChange={handleInputChange} className="col-span-3" required />
            </div>
            {/* Descripción */}
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="description" className="text-right">{t("store.catalog.form.description")}</Label>
              <Textarea id="description" value={formData.description} onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))} className="col-span-3" />
            </div>
            {/* Expiration Date */}
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="expiration_date" className="text-right">{t("store.catalog.form.expirationDate")}</Label>
              <Input id="expiration_date" type="date" value={formData.expiration_date} onChange={handleInputChange} className="col-span-3" />
            </div>
            {/* Imagen */}
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="product_image" className="text-right">{t("store.catalog.form.image")}</Label>
              <Input id="product_image" type="file" onChange={handleImageChange} className="col-span-3" accept="image/*" />
            </div>
          </div>
          <DialogFooter>
            <Button type="submit" disabled={loading}>{t("store.catalog.form.save")}</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
};
