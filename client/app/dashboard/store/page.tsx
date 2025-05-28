// app/dashboard/store/page.tsx
"use client";

import React, { useState, useEffect } from "react";
import { useLanguage } from "@/lib/hooks/use-language";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

// Productos
import { ProductFormData, ProductForm } from "./products/ProductForm";
import { ProductTable } from "./products/ProductTable";
import { Product, useProducts } from "./hooks/useProducts";

// Compras
import { PurchaseForm, PurchaseFormData } from "./purchase/PurchaseForm";
import { PurchaseTable } from "./purchase/PurchaseTable";
import { usePurchases } from "./hooks/usePurchases";

// Inventario
import { InventoryForm } from "./inventory/InventoryForm";
import { InventoryTable } from "./inventory/InventoryTable";
import { useInventory } from "./hooks/useInventory";

// Proveedores
import { SupplierForm, SupplierFormData } from "./suppliers/SupplierForms";
import { SupplierTable } from "./suppliers/SupplierTable";
import { useSuppliers } from "./hooks/useSuppliers";

export default function StorePage() {
  const { t } = useLanguage();
  const [activeTab, setActiveTab] = useState<"catalog" | "purchases" | "inventory" | "suppliers">("catalog");

  // PRODUCTS
  const {
    products,
    loading: prodLoading,
    createProduct,
    updateProduct,
    deleteProduct
  } = useProducts();

  const [isProdFormOpen, setIsProdFormOpen] = useState(false);
  const [editingProduct, setEditingProduct] = useState<Product | undefined>(undefined);

  const onProdSave = async (data: ProductFormData, image: File | null) => {
    if (editingProduct) {
      await updateProduct(editingProduct.id, data, image);
    } else {
      await createProduct(data, image);
    }
    setEditingProduct(undefined);
    setIsProdFormOpen(false);
  };

  const onProdEdit = (prod: Product) => {
    setEditingProduct(prod);
    setIsProdFormOpen(true);
  };

  const onProdDelete = async (id: string) => {
    if (confirm(t("store.catalog.deleteConfirm"))) {
      await deleteProduct(id);
    }
  };

  // PURCHASES
  const {
    purchases,
    loading: purLoading,
    createPurchase,
    updatePurchase,
    deletePurchase
  } = usePurchases();

  const [editingPurchase, setEditingPurchase] = useState<PurchaseFormData & { sale_id: string } | undefined>(undefined);

  const onPurSave = async (data: PurchaseFormData) => {
    if (editingPurchase) {
      await updatePurchase(editingPurchase.sale_id, data);
    } else {
      await createPurchase(data);
    }
    setEditingPurchase(undefined);
  };

  const onPurEdit = (p: PurchaseFormData & { sale_id: string }) => {
    setEditingPurchase(p);
  };

  // INVENTORY
  const { movements, loading: invLoading, addMovement } = useInventory();

  // SUPPLIERS
  const {
    suppliers,
    loading: supLoading,
    createSupplier,
    updateSupplier,
    deleteSupplier
  } = useSuppliers();

  const [editingSupplier, setEditingSupplier] = useState<SupplierFormData & { id: string } | undefined>(undefined);

  const onSupSave = async (data: SupplierFormData) => {
    if (editingSupplier) {
      await updateSupplier(editingSupplier.id, data);
    } else {
      await createSupplier(data);
    }
    setEditingSupplier(undefined);
  };

  const onSupEdit = (s: SupplierFormData & { id: string }) => {
    setEditingSupplier(s);
  };

  return (
    <div className="p-4 space-y-6">
      <Tabs value={activeTab} onValueChange={v => setActiveTab(v as any)}>
        <TabsList>
          <TabsTrigger value="catalog">{t("store.tabs.catalog")}</TabsTrigger>
          <TabsTrigger value="purchases">{t("store.tabs.purchases")}</TabsTrigger>
          <TabsTrigger value="inventory">{t("store.tabs.inventory")}</TabsTrigger>
          <TabsTrigger value="suppliers">{t("store.tabs.suppliers")}</TabsTrigger>
        </TabsList>

        {/* CATALOGO */}
        <TabsContent value="catalog" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>{t("store.catalog.title")}</CardTitle>
            </CardHeader>
            <CardContent>
              {/* Botón para nuevo */}
              <div className="flex justify-end mb-2">
                <ProductForm
                  open={isProdFormOpen}
                  onOpenChange={setIsProdFormOpen}
                  onSubmit={onProdSave}
                  editMode={Boolean(editingProduct)}
                  defaultValues={editingProduct}
                >
                  { !editingProduct && <span>+ {t("store.catalog.addProduct")}</span> }
                </ProductForm>
              </div>

              {/* Tabla */}
              <ProductTable
                products={products}
                onEdit={onProdEdit}
                onDelete={onProdDelete}
              />
            </CardContent>
          </Card>
        </TabsContent>

        {/* COMPRAS */}
        <TabsContent value="purchases" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>{t("store.purchases.title")}</CardTitle>
            </CardHeader>
            <CardContent>
              <PurchaseForm
                onSubmit={onPurSave}
                defaultValues={editingPurchase}
                editMode={Boolean(editingPurchase)}
              />
              <PurchaseTable
                purchases={purchases}
                onEdit={onPurEdit}
                onDelete={deletePurchase}
              />
            </CardContent>
          </Card>
        </TabsContent>

        {/* INVENTARIO */}
        <TabsContent value="inventory" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>{t("store.inventory.title")}</CardTitle>
            </CardHeader>
            <CardContent>
              <InventoryForm onSubmit={addMovement} />
              <InventoryTable movements={movements} loading={invLoading} />
            </CardContent>
          </Card>
        </TabsContent>

        {/* PROVEEDORES */}
        <TabsContent value="suppliers" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>{t("store.suppliers.title")}</CardTitle>
            </CardHeader>
            <CardContent>
              <SupplierForm
                onSubmit={onSupSave}
                defaultValues={editingSupplier}
                editMode={Boolean(editingSupplier)}
              />
              <SupplierTable
                suppliers={suppliers}
                onEdit={onSupEdit}
                onDelete={deleteSupplier}
              />
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
