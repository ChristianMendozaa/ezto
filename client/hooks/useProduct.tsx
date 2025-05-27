// hooks/useProducts.tsx
import { useEffect, useState, useCallback } from "react";
import { useKeycloak } from "@react-keycloak/web";

// Base URL de tu API Gateway (sin slash final)
const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_GATEWAY_URL?.replace(/\/$/, "") ||
  "http://localhost/products";

// --- INTERFACES ---
export interface Product {
  id: string;
  name: string;
  sku: string;
  category: "suplementos" | "ropa" | "equipo" | "accesorios" | "bebidas" | "otros";
  description?: string;
  purchase_price: number;
  sale_price: number;
  current_stock: number;
  min_stock: number;
  expiration_date?: string; // ISO date
  supplier_id: string;
  barcode?: string;
  status: "activo" | "descontinuado" | "agotado";
  image_base64?: string;
  // campos extra de respuesta
  created_at?: string;
  last_updated?: string;
  profit_margin?: number;
}

// Lo que envias al crear o actualizar (sin id ni timestamps ni profit_margin)
export type ProductInput = Omit<
  Product,
  "id" | "created_at" | "last_updated" | "profit_margin"
>;

// --- HOOK ---
export function useProducts() {
  const { keycloak, initialized } = useKeycloak();
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Construye headers con Bearer token de Keycloak
  const authHeaders = useCallback((): Record<string, string> => {
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
    };
    if (keycloak?.token) {
      headers["Authorization"] = `Bearer ${keycloak.token}`;
    }
    return headers;
  }, [keycloak]);

  // 👉 GET /products/
  const fetchProducts = useCallback(async () => {
    if (!keycloak?.authenticated) {
      setError("No estás autenticado");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE_URL}/`, {
        method: "GET",
        headers: authHeaders(),
      });
      if (!res.ok) {
        const details = await res.json().catch(() => ({}));
        throw new Error(
          details?.detail?.message || "Error obteniendo productos."
        );
      }
      const payload = await res.json();
      setProducts(payload.data ?? payload);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [authHeaders, keycloak]);

  // 👉 POST /products/create
  const createProduct = useCallback(
    async (data: ProductInput) => {
      if (!keycloak?.authenticated) {
        setError("No estás autenticado");
        return false;
      }
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${API_BASE_URL}/create`, {
          method: "POST",
          headers: authHeaders(),
          body: JSON.stringify(data),
        });
        if (!res.ok) {
          const details = await res.json().catch(() => ({}));
          throw new Error(
            details?.detail?.message || "No se pudo crear el producto."
          );
        }
        const payload = await res.json();
        const newProd: Product = payload.data ?? payload;
        setProducts((prev) => [...prev, newProd]);
        return true;
      } catch (err: any) {
        setError(err.message);
        return false;
      } finally {
        setLoading(false);
      }
    },
    [authHeaders, keycloak]
  );

  // 👉 DELETE /products/delete/:id
  const deleteProduct = useCallback(
    async (id: string) => {
      if (!keycloak?.authenticated) {
        setError("No estás autenticado");
        return;
      }
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${API_BASE_URL}/delete/${id}`, {
          method: "DELETE",
          headers: authHeaders(),
        });
        if (!res.ok) {
          const details = await res.json().catch(() => ({}));
          throw new Error(
            details?.detail?.message || "No se pudo eliminar el producto."
          );
        }
        setProducts((prev) => prev.filter((p) => p.id !== id));
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    },
    [authHeaders, keycloak]
  );

  // Carga inicial cuando Keycloak está listo
  useEffect(() => {
    if (initialized) {
      fetchProducts();
    }
  }, [initialized, fetchProducts]);

  return {
    products,
    loading,
    error,
    fetchProducts,
    createProduct,
    deleteProduct,
  };
}
