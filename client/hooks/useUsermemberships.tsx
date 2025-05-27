import { useEffect, useState, useCallback } from "react";
import { useKeycloak } from "@react-keycloak/web";

// Ajusta si tu gateway corre en otro URL/puerto
type MembershipStatus = "active" | "expired" | "cancelled";

export interface UserMembership {
  id: string;
  user_id: string;
  plan_id: string;
  start_date: string; // ISO date string
  end_date: string;   // ISO date string
  status: MembershipStatus;
  promotion_id?: string;
  final_price: number;
  auto_renew: boolean;
}

export interface UserMembershipInput extends Omit<UserMembership, "id"> {}

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_GATEWAY_URL?.replace(/\/$/, "") ||
  "http://localhost/usermemberships";

export function useUserMemberships() {
  const { keycloak, initialized } = useKeycloak();
  const [memberships, setMemberships] = useState<UserMembership[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function authHeaders(): Record<string, string> {
    const headers: Record<string, string> = { "Content-Type": "application/json" };
    if (keycloak?.token) {
      headers["Authorization"] = `Bearer ${keycloak.token}`;
    }
    return headers;
  }

  const fetchMemberships = useCallback(async () => {
    if (!keycloak?.authenticated) {
      setError("No estás autenticado");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE_URL}/usermemberships`, {
        method: "GET",
        headers: authHeaders(),
        credentials: "include",
      });
      if (!res.ok) {
        const details = await res.json().catch(() => ({}));
        throw new Error(details?.detail?.message || "Error obteniendo membresías.");
      }
      const payload = await res.json();
      setMemberships(payload.data ?? payload);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [keycloak]);

  const createMembership = useCallback(
    async (data: UserMembershipInput) => {
      if (!keycloak?.authenticated) {
        setError("No estás autenticado");
        return false;
      }
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${API_BASE_URL}/usermemberships/create`, {
          method: "POST",
          headers: authHeaders(),
          credentials: "include",
          body: JSON.stringify(data),
        });
        if (!res.ok) {
          const details = await res.json().catch(() => ({}));
          throw new Error(details?.detail?.message || "No se pudo crear la membresía.");
        }
        const payload = await res.json();
        const newItem: UserMembership = payload.data ?? payload;
        setMemberships((prev) => [...prev, newItem]);
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

  const deleteMembership = useCallback(
    async (id: string) => {
      if (!keycloak?.authenticated) {
        setError("No estás autenticado");
        return;
      }
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${API_BASE_URL}/usermemberships/delete/${id}`, {
          method: "DELETE",
          headers: authHeaders(),
          credentials: "include",
        });
        if (!res.ok) {
          const details = await res.json().catch(() => ({}));
          throw new Error(details?.detail?.message || "No se pudo eliminar la membresía.");
        }
        setMemberships((prev) => prev.filter((m) => m.id !== id));
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    },
    [keycloak]
  );

  useEffect(() => {
    if (initialized) {
      fetchMemberships();
    }
  }, [initialized, fetchMemberships]);

  return {
    memberships,
    loading,
    error,
    createMembership,
    deleteMembership,
    refetch: fetchMemberships,
  };
}
