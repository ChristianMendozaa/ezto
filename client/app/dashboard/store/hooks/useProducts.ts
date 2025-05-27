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

const API_URL =  "http://localhost";

export const useProducts = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const rawAuthHeader = useAuthHeaders();

  const authHeader: Record<string, string> = rawAuthHeader && typeof rawAuthHeader.Authorization === "string"
    ? { Authorization: rawAuthHeader.Authorization }
    : {};

  const fetchProducts = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/shop/products/`, {
        headers: {
          ...authHeader,
        },
      });
      if (res.ok) {
        const data = await res.json();
        setProducts(data);
      } else {
        console.error("Error al obtener productos", await res.text());
      }
    } catch (error) {
      console.error("Error fetching products", error);
    } finally {
      setLoading(false);
    }
  };

  const updateProduct = async (productId: string, updateData: Partial<Product>) => {
    try {
      const formData = new FormData();
      Object.entries(updateData).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          formData.append(key, String(value));
        }
      });
      const res = await fetch(`${API_URL}/shop/products/${productId}`, {
        method: "PUT",
        headers: {
          ...authHeader,
        },
        body: formData,
      });
      if (!res.ok) throw new Error(await res.text());
      await fetchProducts();
    } catch (error) {
      console.error("Error al actualizar producto", error);
    }
  };

  const deleteProduct = async (productId: string) => {
    try {
      const res = await fetch(`${API_URL}/shop/products/${productId}`, {
        method: "DELETE",
        headers: {
          ...authHeader,
        },
      });
      if (!res.ok) throw new Error(await res.text());
      await fetchProducts();
    } catch (error) {
      console.error("Error al eliminar producto", error);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  return { products, loading, fetchProducts, updateProduct, deleteProduct };
};
