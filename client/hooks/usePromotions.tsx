import { useEffect, useState, useCallback } from "react";

// 1️⃣ Ajusta esto si tu gateway corre en otra URL / puerto
const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_GATEWAY_URL?.replace(/\/$/, "") ||
  "http://localhost/promotions";

// 2️⃣ Helper para el header Authorization
function authHeaders(): Record<string, string> {
  // Ejemplo: JWT guardado en localStorage bajo la clave "token"
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  return headers;
}

// 3️⃣ Tipado — mantén los mismos campos que tu DTO devuelve
export interface Promotion {
  id: string;
  name: string;
  description?: string;
  start_date: string;
  end_date: string;
  discount_type: "percentage" | "fixed" | "free_month";
  discount_value: number;
  promo_code?: string;
  auto_apply: boolean;
  status: "active" | "inactive" | string; // amplía si manejas otros estados
}

export interface PromotionInput
  extends Omit<Promotion, "id" | "status"> {} // lo que envías al crear

export function usePromotions() {
  const [promotions, setPromotions] = useState<Promotion[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // 👉 GET /promotions/promotions/
  const fetchPromotions = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE_URL}/promotions/promotions/`, {
        credentials: "include", // cookies si tu gateway usa sesión
        headers: authHeaders(),
      });

      if (!res.ok) {
        const details = await res.json().catch(() => ({}));
        throw new Error(
          details?.detail?.message || details?.message || "Error obteniendo promociones."
        );
      }

      // La respuesta estándar (SuccessResponse) viene en .data
      const payload = await res.json();
      setPromotions(payload.data ?? payload); // fallback por si no vienen envueltos
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  // 👉 POST /promotions/promotions/create
  const createPromotion = useCallback(
    async (data: PromotionInput) => {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${API_BASE_URL}/promotions/promotions/create`, {
          method: "POST",
          headers: authHeaders(),
          credentials: "include",
          body: JSON.stringify(data),
        });

        if (!res.ok) {
          const details = await res.json().catch(() => ({}));
          throw new Error(
            details?.detail?.message || details?.message || "No se pudo crear la promoción."
          );
        }

        const payload = await res.json();
        const newPromotion: Promotion = payload.data ?? payload;
        setPromotions((prev) => [...prev, newPromotion]);
        return true;
      } catch (err: any) {
        setError(err.message);
        return false;
      } finally {
        setLoading(false);
      }
    },
    []
  );

  // 👉 DELETE /promotions/promotions/delete/:id
  const deletePromotion = useCallback(async (id: string) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(
        `${API_BASE_URL}/promotions/promotions/delete/${id}`,
        {
          method: "DELETE",
          credentials: "include",
          headers: authHeaders(),
        }
      );

      if (!res.ok) {
        const details = await res.json().catch(() => ({}));
        throw new Error(
          details?.detail?.message || details?.message || "No se pudo eliminar la promoción."
        );
      }

      setPromotions((prev) => prev.filter((p) => p.id !== id));
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  // carga inicial
  useEffect(() => {
    fetchPromotions();
  }, [fetchPromotions]);

  return {
    promotions,
    loading,
    error,
    createPromotion,
    deletePromotion,
    refetch: fetchPromotions,
  };
}
