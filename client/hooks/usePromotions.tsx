import { useEffect, useState, useCallback } from "react";
import { useKeycloak } from "@react-keycloak/web";

// Ajusta si tu gateway corre en otro URL/puerto
const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_GATEWAY_URL?.replace(/\/$/, "") ||
  "http://localhost/promotions";

export interface Promotion {
  id: string;
  name: string;
  description: string;
  start_date: string;
  end_date: string;
  discount_type: "percentage" | "fixed" | "free_month";
  discount_value: number;
  promo_code?: string;
  auto_apply: boolean;
  applicable_to: "all_users" | "new_users" | "loyal_users" | "specific_plan";
  status: boolean;
}

// Omitimos solo el id, para poder enviar status también si tu DTO lo requiere
export interface PromotionInput extends Omit<Promotion, "id"> {}

export function usePromotions() {
  const { keycloak, initialized } = useKeycloak();
  const [promotions, setPromotions] = useState<Promotion[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Construye headers con Bearer token de Keycloak
  function authHeaders(): Record<string, string> {
    const headers: Record<string, string> = { "Content-Type": "application/json" };
    if (keycloak?.token) {
      headers["Authorization"] = `Bearer ${keycloak.token}`;
    }
    return headers;
  }

  const fetchPromotions = useCallback(async () => {
    if (!keycloak?.authenticated) {
      setError("No estás autenticado");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE_URL}/promotions/`, {
        method: "GET",
        headers: authHeaders(),
      });

      if (!res.ok) {
        const details = await res.json().catch(() => ({}));
        throw new Error(details?.detail?.message || "Error obteniendo promociones.");
      }

      const payload = await res.json();
      setPromotions(payload.data ?? payload);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [keycloak]);

  const createPromotion = useCallback(
    async (data: PromotionInput) => {
      if (!keycloak?.authenticated) {
        setError("No estás autenticado");
        return false;
      }

      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${API_BASE_URL}/promotions/create`, {
          method: "POST",
          headers: authHeaders(),
          body: JSON.stringify(data),
        });

        if (!res.ok) {
          const details = await res.json().catch(() => ({}));
          throw new Error(details?.detail?.message || "No se pudo crear la promoción.");
        }

        const payload = await res.json();
        const newPromo: Promotion = payload.data ?? payload;
        setPromotions((prev) => [...prev, newPromo]);
        return true;
      } catch (err: any) {
        setError(err.message);
        return false;
      } finally {
        setLoading(false);
      }
    },
    [keycloak]
  );
  const updatePromotion = useCallback(
    async (id: string, data: PromotionInput) => {
      if (!keycloak?.authenticated) {
        setError("No estás autenticado");
        return false;
      }

      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${API_BASE_URL}/promotions/update/${id}`, {
          method: "PATCH",
          headers: authHeaders(),
          body: JSON.stringify(data),
        });

        if (!res.ok) {
          const details = await res.json().catch(() => ({}));
          throw new Error(details?.detail?.message || "No se pudo actualizar la promoción.");
        }

        const payload = await res.json();
        const updated: Promotion = payload.data ?? payload;
        setPromotions((prev) =>
          prev.map((p) => (p.id === id ? updated : p))
        );
        return true;
      } catch (err: any) {
        setError(err.message);
        return false;
      } finally {
        setLoading(false);
      }
    },
    [keycloak]
  );
  const deletePromotion = useCallback(
    async (id: string) => {
      if (!keycloak?.authenticated) {
        setError("No estás autenticado");
        return;
      }

      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${API_BASE_URL}/promotions/delete/${id}`, {
          method: "DELETE",
          headers: authHeaders(),
        });

        if (!res.ok) {
          const details = await res.json().catch(() => ({}));
          throw new Error(details?.detail?.message || "No se pudo eliminar la promoción.");
        }

        setPromotions((prev) => prev.filter((p) => p.id !== id));
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    },
    [keycloak]
  );

  // Solo lanza fetch una vez Keycloak esté listo
  useEffect(() => {
    if (initialized) {
      fetchPromotions();
    }
  }, [initialized, fetchPromotions]);

  return {
    promotions,
    loading,
    error,
    createPromotion,
    updatePromotion,
    deletePromotion,
    refetch: fetchPromotions,
  };
}
