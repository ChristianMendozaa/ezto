// app/dashboard/store/page.tsx
"use client";

import React, { useState, useEffect } from "react";
import { useLanguage } from "@/lib/hooks/use-language";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useAuthHeaders } from "@/hooks/use-auth-header";

// Products
import { ProductFormData, ProductForm } from "./components/ProductForm";
import { ProductTable } from "./components/ProductTable";
import { Product, useProducts } from "./hooks/useProducts";

// Purchases

import { PurchaseForm, PurchaseFormData } from "./components/PurchaseForm";
import { PurchaseTable } from "./components/PurchaseTable";
import { usePurchases } from "./hooks/usePurchases";

// Inventory
import { InventoryForm } from "./components/InventoryForm";
import { InventoryTable } from "./components/InventoryTable";
import { useInventory } from "./hooks/useInventory";

// Suppliers

import { useSuppliers } from "./hooks/useSuppliers";
import { SupplierForm, SupplierFormData } from "./components/SupplierForms";
import { SupplierTable } from "./components/SupplierTable";

export default function StorePage() {
  const { t } = useLanguage();
  const [activeTab, setActiveTab] = useState<
    "catalog" | "purchases" | "inventory" | "suppliers"
  >("catalog");

  // Auth headers
  const rawAuth = useAuthHeaders();
  const authHeader: HeadersInit = rawAuth?.Authorization
    ? { Authorization: rawAuth.Authorization }
    : {};

  // Products
  const { products, fetchProducts, updateProduct, deleteProduct } = useProducts();
  const [editingProduct, setEditingProduct] = useState<
    ProductFormData & { id: string }
  >();

  // Purchases
  const { purchases, fetchPurchases } = usePurchases();
  const [editingPurchase, setEditingPurchase] = useState<
    PurchaseFormData & { sale_id: string }
  >();

  // Inventory
  const { movements, loading: invLoading, fetchInventory, addMovement } = useInventory();

  // Suppliers
  const { suppliers, fetchSuppliers} = useSuppliers();
  const [editingSupplier, setEditingSupplier] = useState<
    SupplierFormData & { id: string }
  >();

  // Load all on mount
  useEffect(() => {
    fetchProducts();
    fetchPurchases();
    fetchInventory();
    fetchSuppliers();
  }, []);

  // Handlers Products
  const handleAddProduct = async (data: ProductFormData, image: File | null) => {
    const form = new FormData();
    Object.entries(data).forEach(([k, v]) => form.append(k, v));
    if (image) form.append("product_image", image);
    try {
      const res = await fetch("http://localhost/shop/products/", {
        method: "POST",
        headers: authHeader,
        body: form,
      });
      if (!res.ok) throw new Error(await res.text());
      fetchProducts();
    } catch (err) {
      console.error("Error creating product:", err);
    }
  };

  const handleEditProduct = (product: Product) => {
    // Convert Product to ProductFormData & { id: string }
    const {
      id,
      name,
      description,
      purchase_price,
      sale_price,
      current_stock,
      min_stock,
      expiration_date,
      ...rest
    } = product;
    setEditingProduct({
      id,
      name,
      description: description ?? "",
      purchase_price: purchase_price.toString(),
      sale_price: sale_price.toString(),
      current_stock: current_stock?.toString?.() ?? "",
      min_stock: min_stock?.toString?.() ?? "",
      expiration_date: expiration_date ?? "",
      barcode: product.barcode ?? "",
      ...rest
    });
  };

  const handleUpdateProduct = async (
    data: ProductFormData,
    image: File | null,
    id?: string
  ) => {
    if (!id) return;
    const form = new FormData();
    Object.entries(data).forEach(([k, v]) => form.append(k, v));
    if (image) form.append("product_image", image);
    try {
      const res = await fetch(`http://localhost/shop/products/${id}`, {
        method: "PUT",
        headers: authHeader,
        body: form,
      });
      if (!res.ok) throw new Error(await res.text());
      setEditingProduct(undefined);
      fetchProducts();
    } catch (err) {
      console.error("Error updating product:", err);
    }
  };

  const handleDeleteProduct = async (id: string) => {
    if (!confirm(t("store.catalog.deleteConfirm"))) return;
    try {
      await deleteProduct(id);
    } catch {}
  };

  // Handlers Purchases
  const handleAddPurchase = async (data: PurchaseFormData) => {
    try {
      const res = await fetch("http://localhost/purchases/", {
        method: "POST",
        headers: { ...authHeader, "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (!res.ok) throw new Error(await res.text());
      fetchPurchases();
    } catch (err) {
      console.error("Error adding purchase:", err);
    }
  };

  const handleEditPurchase = (p: PurchaseFormData & { sale_id: string }) => {
    setEditingPurchase(p);
  };

  const handleUpdatePurchase = async (
    data: PurchaseFormData,
    sale_id?: string
  ) => {
    if (!sale_id) return;
    try {
      const res = await fetch(`http://localhost/purchases/${sale_id}`, {
        method: "PUT",
        headers: { ...authHeader, "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (!res.ok) throw new Error(await res.text());
      setEditingPurchase(undefined);
      fetchPurchases();
    } catch (err) {
      console.error("Error updating purchase:", err);
    }
  };

  const handleDeletePurchase = async (sale_id: string) => {
    if (!confirm(t("store.purchases.deleteConfirm"))) return;
    try {
      await deletePurchase(sale_id);
    } catch {}
  };

  // Handlers Suppliers
  const handleAddSupplier = async (data: SupplierFormData) => {
    try {
      const res = await fetch("http://localhost/suppliers/", {
        method: "POST",
        headers: { ...authHeader, "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (!res.ok) throw new Error(await res.text());
      fetchSuppliers();
    } catch (err) {
      console.error("Error adding supplier:", err);
    }
  };

  const handleEditSupplier = (s: SupplierFormData & { id: string }) => {
    setEditingSupplier(s);
  };

  const handleUpdateSupplier = async (
    data: SupplierFormData,
    id?: string
  ) => {
    if (!id) return;
    try {
      const res = await fetch(`http://localhost/suppliers/${id}`, {
        method: "PUT",
        headers: { ...authHeader, "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (!res.ok) throw new Error(await res.text());
      setEditingSupplier(undefined);
      fetchSuppliers();
    } catch (err) {
      console.error("Error updating supplier:", err);
    }
  };

  const handleDeleteSupplier = async (id: string) => {
    if (!confirm(t("store.suppliers.deleteConfirm"))) return;
    try {
      await deleteSupplier(id);
    } catch {}
  };

  return (
    <div className="p-4">
      <Tabs value={activeTab} onValueChange={v => setActiveTab(v as any)}>
        <TabsList>
          <TabsTrigger value="catalog">{t("store.tabs.catalog")}</TabsTrigger>
          <TabsTrigger value="purchases">{t("store.tabs.purchases")}</TabsTrigger>
          <TabsTrigger value="inventory">{t("store.tabs.inventory")}</TabsTrigger>
          <TabsTrigger value="suppliers">{t("store.tabs.suppliers")}</TabsTrigger>
        </TabsList>

        {/* Catalog */}
        <TabsContent value="catalog" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>{t("store.catalog.title")}</CardTitle>
            </CardHeader>
            <CardContent>
              <ProductForm onSubmit={handleAddProduct} />
              {editingProduct && (
                <ProductForm
                  defaultValues={editingProduct}
                  editMode
                  onSubmit={(d, img) => handleUpdateProduct(d, img, editingProduct.id)}
                />
              )}
              <ProductTable
                products={products}
                onEdit={handleEditProduct}
                onDelete={handleDeleteProduct}
              />
            </CardContent>
          </Card>
        </TabsContent>

        {/* Purchases */}
        <TabsContent value="purchases" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>{t("store.purchases.title")}</CardTitle>
            </CardHeader>
            <CardContent>
              <PurchaseForm
                onSubmit={data =>
                  handleAddPurchase({
                    ...data,
                    total_amount: parseFloat(data.total_amount as any),
                  } as any)
                }
              />
              {editingPurchase && (
                <PurchaseForm
                  defaultValues={editingPurchase}
                  editMode
                  onSubmit={d => handleUpdatePurchase(
                    { ...d, total_amount: d.total_amount.toString(), tax_amount: d.tax_amount.toString() },
                    editingPurchase.sale_id
                  )}
                />
              )}
              <PurchaseTable
                purchases={purchases}
              />
            </CardContent>
          </Card>
        </TabsContent>

        {/* Inventory */}
        <TabsContent value="inventory" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>{t("store.inventory.title")}</CardTitle>
            </CardHeader>
            <CardContent>
              <InventoryForm onSubmit={addMovement} />
              {invLoading
                ? <p>{t("store.inventory.loading")}</p>
                : <InventoryTable movements={movements} />
              }
            </CardContent>
          </Card>
        </TabsContent>

        {/* Suppliers */}
        <TabsContent value="suppliers" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>{t("store.suppliers.title")}</CardTitle>
            </CardHeader>
            <CardContent>
              <SupplierForm onSubmit={handleAddSupplier} />
              {editingSupplier && (
                <SupplierForm
                  defaultValues={editingSupplier}
                  editMode
                  onSubmit={d => handleUpdateSupplier(d, editingSupplier.id)}
                />
              )}
              <SupplierTable
                suppliers={suppliers}
              />
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
function deletePurchase(sale_id: string) {
  throw new Error("Function not implemented.");
}

function deleteSupplier(id: string) {
  throw new Error("Function not implemented.");
}

