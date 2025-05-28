// hooks/useSuppliers.ts
import { useState, useEffect } from "react";
import { useAuthHeaders } from "@/hooks/use-auth-header";

export interface Supplier {
  id: string;
  name: string;
  contact_email: string;
  phone: string;
  address: string;
  tax_id: string;
  payment_terms: string;
  status: string;
  created_at: string;     // YYYY-MM-DD
  last_updated: string;   // YYYY-MM-DD
  products_offered: number;
}

export type SupplierFormData = Omit<Supplier, "id" | "created_at" | "last_updated">;

const API_BASE = "http://localhost/suppliers";

export function useSuppliers() {
  const [suppliers, setSuppliers] = useState<Supplier[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const rawAuth = useAuthHeaders();
  const authHeader: Record<string, string> =
    rawAuth?.Authorization && typeof rawAuth.Authorization === "string"
      ? { Authorization: rawAuth.Authorization }
      : {};

  /** Carga la lista de proveedores */
  const fetchSuppliers = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/`, {
        headers: authHeader,
      });
      if (!res.ok) throw new Error(await res.text());
      const data: Supplier[] = await res.json();
      setSuppliers(data);
    } catch (err) {
      console.error("Error fetching suppliers:", err);
    } finally {
      setLoading(false);
    }
  };

  /** Crea un nuevo proveedor */
  const createSupplier = async (data: SupplierFormData) => {
    try {
      const res = await fetch(`${API_BASE}/`, {
        method: "POST",
        headers: { ...authHeader, "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (!res.ok) throw new Error(await res.text());
      await fetchSuppliers();
    } catch (err) {
      console.error("Error creating supplier:", err);
    }
  };

  /** Actualiza un proveedor existente */
  const updateSupplier = async (id: string, data: Partial<SupplierFormData>) => {
    try {
      const res = await fetch(`${API_BASE}/${id}`, {
        method: "PUT",
        headers: { ...authHeader, "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (!res.ok) throw new Error(await res.text());
      await fetchSuppliers();
    } catch (err) {
      console.error("Error updating supplier:", err);
    }
  };

  /** Elimina un proveedor */
  const deleteSupplier = async (id: string) => {
    try {
      const res = await fetch(`${API_BASE}/${id}`, {
        method: "DELETE",
        headers: authHeader,
      });
      if (!res.ok) throw new Error(await res.text());
      await fetchSuppliers();
    } catch (err) {
      console.error("Error deleting supplier:", err);
    }
  };

  useEffect(() => {
    fetchSuppliers();
  }, []);

  return {
    suppliers,
    loading,
    fetchSuppliers,
    createSupplier,
    updateSupplier,
    deleteSupplier,
  };
}
