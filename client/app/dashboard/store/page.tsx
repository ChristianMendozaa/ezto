"use client";

import React, { useState } from "react";
import { useLanguage } from "@/lib/hooks/use-language";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ProductFormData, ProductForm } from "./components/ProductForm";
import { ProductTable } from "./components/ProductTable";
import { useProducts } from "./hooks/useProducts";
import { useAuthHeaders } from "@/hooks/use-auth-header";

export default function StorePage() {
  const { t } = useLanguage();
  const [activeTab, setActiveTab] = useState("catalog");
  const { products, fetchProducts, updateProduct, deleteProduct } = useProducts();

  const rawAuthHeader = useAuthHeaders();
  const authHeader: Record<string, string> = rawAuthHeader && typeof rawAuthHeader.Authorization === "string"
    ? { Authorization: rawAuthHeader.Authorization }
    : {};

  const [editingProduct, setEditingProduct] = useState<any | null>(null);

  const handleEditProduct = (product: any) => {
    setEditingProduct(product);
  };

  const handleDeleteProduct = async (productId: string) => {
    if (confirm("¿Estás seguro de eliminar este producto?")) {
      await deleteProduct(productId);
    }
  };

  const handleAddProduct = async (data: ProductFormData, image: File | null) => {
    const formData = new FormData();
    Object.entries(data).forEach(([key, value]) => {
      formData.append(key, value);
    });
    if (image) formData.append("product_image", image);

    try {
      const res = await fetch("http://localhost/shop/products/", {
        method: "POST",
        headers: {
          ...authHeader,
        },
        body: formData,
      });

      if (!res.ok) {
        const errorText = await res.text();
        console.error("Error al agregar producto:", errorText);
        alert("No se pudo agregar el producto.");
      } else {
        await fetchProducts();
      }
    } catch (error) {
      console.error("Error en el POST:", error);
    }
  };

  const handleUpdateProduct = async (data: ProductFormData, image: File | null, id?: string) => {
    if (!id) return;
    const formData = new FormData();
    Object.entries(data).forEach(([key, value]) => {
      formData.append(key, value);
    });
    if (image) formData.append("product_image", image);

    try {
      const res = await fetch(`http://localhost/shop/products/${id}`, {
        method: "PUT",
        headers: {
          ...authHeader,
        },
        body: formData,
      });

      if (!res.ok) {
        const errorText = await res.text();
        console.error("Error al actualizar producto:", errorText);
        alert("No se pudo actualizar el producto.");
      } else {
        await fetchProducts();
        setEditingProduct(null);
      }
    } catch (error) {
      console.error("Error en el PUT:", error);
    }
  };

  return (
    <div className="flex-1 space-y-4 p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <CardTitle className="text-3xl font-bold tracking-tight">{t("store.title")}</CardTitle>
      </div>
      <Tabs defaultValue="catalog" className="space-y-4">
        <TabsList>
          <TabsTrigger value="catalog" onClick={() => setActiveTab("catalog")}>{t("store.tabs.catalog")}</TabsTrigger>
          <TabsTrigger value="purchases" onClick={() => setActiveTab("purchases")}>{t("store.tabs.purchases")}</TabsTrigger>
          <TabsTrigger value="inventory" onClick={() => setActiveTab("inventory")}>{t("store.tabs.inventory")}</TabsTrigger>
        </TabsList>
        <TabsContent value="catalog" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>{t("store.catalog.title")}</CardTitle>
            </CardHeader>
            <CardContent>
              <ProductForm onSubmit={handleAddProduct} />
              {editingProduct && (
                <ProductForm
                  onSubmit={(data, image) => handleUpdateProduct(data, image, editingProduct.id)}
                  defaultValues={editingProduct}
                  editMode={true}
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
      </Tabs>
    </div>
  );
}