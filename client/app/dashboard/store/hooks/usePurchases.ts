// hooks/usePurchases.ts
import { useState, useEffect } from "react";
import { useAuthHeaders } from "@/hooks/use-auth-header";

export interface PurchaseItem {
  product_id: string;
  quantity: number;
  unit_price: number;
  discount: number;
}

export interface Purchase {
  sale_id: string;
  client_id: string;
  items: PurchaseItem[];
  payment_method: string;
  notes: string;
  total_amount: number;
  tax_amount: number;
  sale_date: string; // ISO 8601
  seller_id: string;
  invoice_number: string;
  status: string;
}

export type PurchaseFormData = Omit<Purchase, "sale_id">;

const API_BASE = "http://localhost/purchases";

export function usePurchases() {
  const [purchases, setPurchases] = useState<Purchase[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const rawAuth = useAuthHeaders();
  const authHeader: Record<string, string> =
    rawAuth?.Authorization && typeof rawAuth.Authorization === "string"
      ? { Authorization: rawAuth.Authorization }
      : {};

  /** Carga todas las compras */
  const fetchPurchases = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/`, {
        headers: authHeader,
      });
      if (!res.ok) throw new Error(await res.text());
      const data: Purchase[] = await res.json();
      setPurchases(data);
    } catch (err) {
      console.error("Error fetching purchases:", err);
    } finally {
      setLoading(false);
    }
  };

  /** Crea una nueva compra */
  const createPurchase = async (data: PurchaseFormData) => {
    try {
      const res = await fetch(`${API_BASE}/`, {
        method: "POST",
        headers: { ...authHeader, "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (!res.ok) throw new Error(await res.text());
      await fetchPurchases();
    } catch (err) {
      console.error("Error creating purchase:", err);
    }
  };

  /** Actualiza una compra existente */
  const updatePurchase = async (
    sale_id: string,
    data: Partial<PurchaseFormData>
  ) => {
    try {
      const res = await fetch(`${API_BASE}/${sale_id}`, {
        method: "PUT",
        headers: { ...authHeader, "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (!res.ok) throw new Error(await res.text());
      await fetchPurchases();
    } catch (err) {
      console.error("Error updating purchase:", err);
    }
  };

  /** Elimina una compra */
  const deletePurchase = async (sale_id: string) => {
    try {
      const res = await fetch(`${API_BASE}/${sale_id}`, {
        method: "DELETE",
        headers: authHeader,
      });
      if (!res.ok) throw new Error(await res.text());
      await fetchPurchases();
    } catch (err) {
      console.error("Error deleting purchase:", err);
    }
  };

  useEffect(() => {
    fetchPurchases();
  }, []);

  return {
    purchases,
    loading,
    fetchPurchases,
    createPurchase,
    updatePurchase,
    deletePurchase,
  };
}
