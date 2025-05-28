import { useState, useEffect } from "react";
import { useAuthHeaders } from "@/hooks/use-auth-header";

export interface Product {
  id: string;
  name: string;
  sku: string;
  category: string;
  description?: string;
  purchase_price: number;
  sale_price: number;
  current_stock: number;
  min_stock: number;
  expiration_date?: string;
  supplier_id: string;
  barcode?: string;
  status: string;
  image_base64?: string;
  created_at: string;
  last_updated: string;
  profit_margin: number;
}

export interface ProductFormData {
  name: string;
  sku: string;
  category: string;
  description: string;
  purchase_price: string;
  sale_price: string;
  current_stock: string;
  min_stock: string;
  expiration_date: string;
  supplier_id: string;
  barcode: string;
  status: string;
}

const API_BASE = "http://localhost/shop/products";

export function useProducts() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const rawAuth = useAuthHeaders();
  const authHeader: Record<string, string> =
    rawAuth?.Authorization && typeof rawAuth.Authorization === "string"
      ? { Authorization: rawAuth.Authorization }
      : {};

  const fetchProducts = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/`, {
        headers: authHeader,
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      setProducts(data);
    } catch (err) {
      console.error("Error fetching products:", err);
    } finally {
      setLoading(false);
    }
  };

  const createProduct = async (data: ProductFormData, imageFile: File | null) => {
    const form = new FormData();
    Object.entries(data).forEach(([key, value]) => {
      form.append(key, value);
    });
    if (imageFile) {
      form.append("product_image", imageFile);
    }
    try {
      const res = await fetch(`${API_BASE}/`, {
        method: "POST",
        headers: authHeader,
        body: form,
      });
      if (!res.ok) throw new Error(await res.text());
      await fetchProducts();
    } catch (err) {
      console.error("Error creating product:", err);
    }
  };

  const updateProduct = async (
    productId: string,
    data: Partial<ProductFormData>,
    imageFile: File | null
  ) => {
    const form = new FormData();
    Object.entries(data).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        form.append(key, value);
      }
    });
    if (imageFile) {
      form.append("product_image", imageFile);
    }
    try {
      const res = await fetch(`${API_BASE}/${productId}`, {
        method: "PUT",
        headers: authHeader,
        body: form,
      });
      if (!res.ok) throw new Error(await res.text());
      await fetchProducts();
    } catch (err) {
      console.error("Error updating product:", err);
    }
  };

  const deleteProduct = async (productId: string) => {
    try {
      const res = await fetch(`${API_BASE}/${productId}`, {
        method: "DELETE",
        headers: authHeader,
      });
      if (!res.ok) throw new Error(await res.text());
      await fetchProducts();
    } catch (err) {
      console.error("Error deleting product:", err);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  return {
    products,
    loading,
    fetchProducts,
    createProduct,
    updateProduct,
    deleteProduct,
  };
}
