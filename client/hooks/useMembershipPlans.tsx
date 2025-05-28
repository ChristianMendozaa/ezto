"use client";

import { useEffect, useState, useCallback } from "react";
import { useKeycloak } from "@react-keycloak/web";

// Ajusta si tu gateway corre en otro URL/puerto
const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_GATEWAY_URL?.replace(/\/$/, "") ||
  "http://localhost/memberships-plans";

export interface MembershipPlan {
  id: string;
  name: string;
  description: string;
  capacity: number;
  duration_months: number;
  price: number;
  services_offered: string[];
}

// Para crear un plan, omitimos el id
export interface MembershipPlanInput extends Omit<MembershipPlan, "id"> {}

export function useMembershipPlans() {
  const { keycloak, initialized } = useKeycloak();
  const [plans, setPlans] = useState<MembershipPlan[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function authHeaders(): Record<string, string> {
    const headers: Record<string, string> = { "Content-Type": "application/json" };
    if (keycloak?.token) {
      headers["Authorization"] = `Bearer ${keycloak.token}`;
    }
    return headers;
  }

  const fetchPlans = useCallback(async () => {
    if (!keycloak?.authenticated) {
      setError("No estás autenticado");
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE_URL}/memberships-plans/`, {
        method: "GET",
        headers: authHeaders(),
      });
      if (!res.ok) {
        const details = await res.json().catch(() => ({}));
        throw new Error(details?.detail?.message || "Error obteniendo planes.");
      }
      const payload = await res.json();
      setPlans(payload.data ?? payload);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [keycloak]);

  const createPlan = useCallback(
    async (data: MembershipPlanInput) => {
      if (!keycloak?.authenticated) {
        setError("No estás autenticado");
        return false;
      }

      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${API_BASE_URL}/memberships-plans/create`, {
          method: "POST",
          headers: authHeaders(),
          body: JSON.stringify(data),
        });
        if (!res.ok) {
          const details = await res.json().catch(() => ({}));
          throw new Error(details?.detail?.message || "No se pudo crear el plan.");
        }
        const payload = await res.json();
        const newPlan: MembershipPlan = payload.data ?? payload;
        setPlans((prev) => [...prev, newPlan]);
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
  const updatePlan = useCallback(
    async (id: string, data: MembershipPlanInput) => {
      if (!keycloak?.authenticated) {
        setError("No estás autenticado");
        return false;
      }

      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${API_BASE_URL}/memberships-plans/update/${id}`, {
          method: "PATCH",
          headers: authHeaders(),
          body: JSON.stringify(data),
        });
        if (!res.ok) {
          const details = await res.json().catch(() => ({}));
          throw new Error(details?.detail?.message || "No se pudo actualizar el plan.");
        }
        const payload = await res.json();
        const updated: MembershipPlan = payload.data ?? payload;
        setPlans((prev) => prev.map((p) => (p.id === id ? updated : p)));
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
  const deletePlan = useCallback(
    async (id: string) => {
      if (!keycloak?.authenticated) {
        setError("No estás autenticado");
        return;
      }

      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${API_BASE_URL}/memberships-plans/delete/${id}`, {
          method: "DELETE",
          headers: authHeaders(),
        });
        if (!res.ok) {
          const details = await res.json().catch(() => ({}));
          throw new Error(details?.detail?.message || "No se pudo eliminar el plan.");
        }
        setPlans((prev) => prev.filter((p) => p.id !== id));
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    },
    [keycloak]
  );

  // Sólo lanza fetch una vez Keycloak esté listo
  useEffect(() => {
    if (initialized) {
      console.log("monté el componente, voy a fetchear");
      fetchPlans();
    }
  }, [initialized, fetchPlans]);

  return {
    plans,
    loading,
    error,
    createPlan,
    updatePlan,
    deletePlan,
    refetch: fetchPlans,
  };
}
