import { useEffect, useState, useCallback } from "react";
import { useKeycloak } from "@react-keycloak/web";

// Ajusta si tu gateway corre en otro URL/puerto
const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_GATEWAY_URL?.replace(/\/$/, "") ||
  "http://localhost/personal";

export interface Personal {
  id: string;
  name: string;
  role: "trainer" | "receptionist" | "manager" | "maintenance";
  schedule: string;
  access_level: "full" | "standard" | "limited";
}

export type PersonalInput = Omit<Personal, "id">;

export function usePersonal() {
  const { keycloak, initialized } = useKeycloak();
  const [personals, setPersonals] = useState<Personal[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function authHeaders(): Record<string, string> {
    const headers: Record<string, string> = { "Content-Type": "application/json" };
    if (keycloak?.token) {
      headers["Authorization"] = `Bearer ${keycloak.token}`;
    }
    return headers;
  }

  const fetchPersonals = useCallback(async () => {
    if (!keycloak?.authenticated) {
      setError("No estás autenticado");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE_URL}/personal/`, {
        method: "GET",
        headers: authHeaders(),
      });
      if (!res.ok) {
        const details = await res.json().catch(() => ({}));
        throw new Error(details?.detail?.message || "Error obteniendo personal.");
      }
      const payload = await res.json();
      setPersonals(payload.data ?? payload);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [keycloak]);

  const createPersonal = useCallback(
    async (data: PersonalInput) => {
      if (!keycloak?.authenticated) {
        setError("No estás autenticado");
        return false;
      }
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${API_BASE_URL}/personal/create`, {
          method: "POST",
          headers: authHeaders(),
          body: JSON.stringify(data),
        });
        if (!res.ok) {
          const details = await res.json().catch(() => ({}));
          throw new Error(details?.detail?.message || "No se pudo crear el registro de personal.");
        }
        const payload = await res.json();
        const newItem: Personal = payload.data ?? payload;
        setPersonals(prev => [...prev, newItem]);
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

  const deletePersonal = useCallback(
    async (id: string) => {
      if (!keycloak?.authenticated) {
        setError("No estás autenticado");
        return;
      }
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${API_BASE_URL}/personal/delete/${id}`, {
          method: "DELETE",
          headers: authHeaders(),
        });
        if (!res.ok) {
          const details = await res.json().catch(() => ({}));
          throw new Error(details?.detail?.message || "No se pudo eliminar el registro de personal.");
        }
        setPersonals(prev => prev.filter(item => item.id !== id));
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
      fetchPersonals();
    }
  }, [initialized, fetchPersonals]);

  return {
    personals,
    loading,
    error,
    fetchPersonals,
    createPersonal,
    deletePersonal,
  };
}
