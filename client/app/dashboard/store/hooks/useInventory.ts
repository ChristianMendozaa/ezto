// hooks/useInventory.ts
import { useState, useEffect } from "react";
import { useAuthHeaders } from "@/hooks/use-auth-header";

export interface InventoryMovement {
  id: string;
  product_id: string;
  movement_type: "entrada" | "salida";
  quantity: number;
  reason: string;
  reference_id: string;
  movement_date: string; // ISO 8601
  responsible_id: string;
}

export type NewInventoryMovement = Omit<InventoryMovement, "id">;

const API_BASE = "http://localhost/inventory";

export function useInventory() {
  const [movements, setMovements] = useState<InventoryMovement[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const rawAuth = useAuthHeaders();
  const authHeader: Record<string, string> =
    rawAuth?.Authorization && typeof rawAuth.Authorization === "string"
      ? { Authorization: rawAuth.Authorization }
      : {};

  /** Trae todos los movimientos */
  const fetchInventory = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/`, {
        headers: authHeader,
      });
      if (!res.ok) throw new Error(await res.text());
      const data: InventoryMovement[] = await res.json();
      setMovements(data);
    } catch (err) {
      console.error("Error fetching inventory movements:", err);
    } finally {
      setLoading(false);
    }
  };

  /** Añade un nuevo movimiento */
  const addMovement = async (mv: NewInventoryMovement) => {
    try {
      const res = await fetch(`${API_BASE}/`, {
        method: "POST",
        headers: {
          ...authHeader,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(mv),
      });
      if (!res.ok) throw new Error(await res.text());
      await fetchInventory();
    } catch (err) {
      console.error("Error adding inventory movement:", err);
    }
  };

  /** Actualiza un movimiento existente */
  const updateMovement = async (id: string, mv: Partial<NewInventoryMovement>) => {
    try {
      const res = await fetch(`${API_BASE}/${id}`, {
        method: "PUT",
        headers: {
          ...authHeader,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(mv),
      });
      if (!res.ok) throw new Error(await res.text());
      await fetchInventory();
    } catch (err) {
      console.error("Error updating inventory movement:", err);
    }
  };

  /** Elimina un movimiento */
  const deleteMovement = async (id: string) => {
    try {
      const res = await fetch(`${API_BASE}/${id}`, {
        method: "DELETE",
        headers: authHeader,
      });
      if (!res.ok) throw new Error(await res.text());
      await fetchInventory();
    } catch (err) {
      console.error("Error deleting inventory movement:", err);
    }
  };

  useEffect(() => {
    fetchInventory();
  }, []);

  return {
    movements,
    loading,
    fetchInventory,
    addMovement,
    updateMovement,
    deleteMovement,
  };
}
