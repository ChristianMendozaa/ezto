// store/StorePage.tsx
"use client";

import React, { useState } from "react";
import { useLanguage } from "@/lib/hooks/use-language";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ProductForm } from "./components/ProductForm";
import { ProductTable } from "./components/ProductTable";
import { useProducts } from "./hooks/useProducts";

export default function StorePage() {
  const { t } = useLanguage();
  const [activeTab, setActiveTab] = useState("catalog");
  const { products, loading, fetchProducts, updateProduct, deleteProduct } = useProducts();

  const handleEditProduct = (product: any) => {
    // Aquí podrías implementar la lógica para editar un producto
    console.log("Editar producto:", product);
  };

  const handleDeleteProduct = async (productId: string) => {
    if (confirm("¿Estás seguro de eliminar este producto?")) {
      await deleteProduct(productId);
    }
  };

  return (
    <div className="flex-1 space-y-4 p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <CardTitle className="text-3xl font-bold tracking-tight">{t("store.title")}</CardTitle>
      </div>
      <Tabs defaultValue="catalog" className="space-y-4">
        <TabsList>
          <TabsTrigger value="catalog" onClick={() => setActiveTab("catalog")}>
            {t("store.tabs.catalog")}
          </TabsTrigger>
          <TabsTrigger value="purchases" onClick={() => setActiveTab("purchases")}>
            {t("store.tabs.purchases")}
          </TabsTrigger>
          <TabsTrigger value="inventory" onClick={() => setActiveTab("inventory")}>
            {t("store.tabs.inventory")}
          </TabsTrigger>
        </TabsList>
        <TabsContent value="catalog" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>{t("store.catalog.title")}</CardTitle>
            </CardHeader>
            <CardContent>
              <ProductForm onSubmit={async (data, image) => {
                const formData = new FormData();
                Object.entries(data).forEach(([key, value]) => {
                  formData.append(key, value);
                });
                if (image) {
                  formData.append("product_image", image);
                }
                const res = await fetch("http://localhost:8001/products/", {
                  method: "POST",
                  credentials: "include",
                  body: formData,
                });
                if (res.ok) {
                  await fetchProducts();
                } else {
                  console.error("Error al agregar producto", await res.text());
                }
              }} />
              <ProductTable products={products} onEdit={handleEditProduct} onDelete={handleDeleteProduct} />
            </CardContent>
          </Card>
        </TabsContent>
        {/* Puedes agregar TabsContent para purchases e inventory según lo necesites */}
      </Tabs>
    </div>
  );
}
