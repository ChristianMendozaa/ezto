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

const API_URL = "http://localhost";

export const useInventory = () => {
  const [movements, setMovements] = useState<InventoryMovement[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const rawAuth = useAuthHeaders();

  const authHeader: Record<string, string> =
    rawAuth && typeof rawAuth.Authorization === 'string'
      ? { Authorization: rawAuth.Authorization }
      : {};

  const fetchInventory = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/inventory/`, {
        headers: { ...authHeader },
      });
      if (!res.ok) throw new Error(await res.text());
      const data: InventoryMovement[] = await res.json();
      setMovements(data);
    } catch (err) {
      console.error('Error fetching inventory movements', err);
    } finally {
      setLoading(false);
    }
  };

  const addMovement = async (mv: Omit<InventoryMovement, 'id'>) => {
    try {
      const res = await fetch(`${API_URL}/inventory/`, {
        method: 'POST',
        headers: {
          ...authHeader,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(mv),
      });
      if (!res.ok) throw new Error(await res.text());
      await fetchInventory();
    } catch (err) {
      console.error('Error adding inventory movement', err);
    }
  };

  useEffect(() => {
    fetchInventory();
  }, []);

  return { movements, loading, fetchInventory, addMovement };
};
