import { useEffect, useState, useCallback } from "react";
import { useKeycloak } from "@react-keycloak/web";

// Ajusta si tu gateway corre en otro URL/puerto
const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_GATEWAY_URL?.replace(/\/$/, "") ||
  "http://localhost/classes";

export interface ClassDTO {
  id?: string;
  name: string;
  description: string;
  instructor: string;
  start_time: string; // ISO datetime
  end_time: string;   // ISO datetime
  capacity: number;
  location?: string;
  status: boolean;
}

// Omitimos el id al crear
export interface ClassInput extends Omit<ClassDTO, "id"> {}

export function useClasses() {
  const { keycloak, initialized } = useKeycloak();
  const [classes, setClasses] = useState<ClassDTO[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function authHeaders(): Record<string, string> {
    const headers: Record<string, string> = { "Content-Type": "application/json" };
    if (keycloak?.token) {
      headers["Authorization"] = `Bearer ${keycloak.token}`;
    }
    return headers;
  }

  const fetchClasses = useCallback(async () => {
    if (!keycloak?.authenticated) {
      setError("No estás autenticado");
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE_URL}/classes/`, {
        method: "GET",
        headers: authHeaders(),
      });
      if (!res.ok) {
        const details = await res.json().catch(() => ({}));
        throw new Error(details?.detail?.message || "Error obteniendo clases.");
      }
      const payload = await res.json();
      setClasses(payload.data ?? payload);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [keycloak]);

  const createClass = useCallback(
    async (data: ClassInput) => {
      if (!keycloak?.authenticated) {
        setError("No estás autenticado");
        return false;
      }

      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${API_BASE_URL}/classes/create`, {
          method: "POST",
          headers: authHeaders(),
          body: JSON.stringify(data),
        });
        if (!res.ok) {
          const details = await res.json().catch(() => ({}));
          throw new Error(details?.detail?.message || "No se pudo crear la clase.");
        }
        const payload = await res.json();
        const newClass: ClassDTO = payload.data ?? payload;
        setClasses((prev) => [...prev, newClass]);
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

  const deleteClass = useCallback(
    async (id: string) => {
      if (!keycloak?.authenticated) {
        setError("No estás autenticado");
        return;
      }

      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${API_BASE_URL}/classes/delete/${id}`, {
          method: "DELETE",
          headers: authHeaders(),
        });
        if (!res.ok) {
          const details = await res.json().catch(() => ({}));
          throw new Error(details?.detail?.message || "No se pudo eliminar la clase.");
        }
        setClasses((prev) => prev.filter((c) => c.id !== id));
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
      fetchClasses();
    }
  }, [initialized, fetchClasses]);

  return {
    classes,
    loading,
    error,
    createClass,
    deleteClass,
    refetch: fetchClasses,
  };
}
