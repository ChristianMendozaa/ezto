// hooks/useEvents.tsx
import { useEffect, useState, useCallback } from "react";
import { useKeycloak } from "@react-keycloak/web";

// Ajusta si tu gateway corre en otro URL/puerto
const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_GATEWAY_URL?.replace(/\/$/, "") ||
  "http://localhost/events";

// --- DTO TYPES ---
export interface Event {
  id: string;
  name: string;
  description: string;
  organizer: string;
  start_time: string;   // ISO datetime
  end_time: string;     // ISO datetime
  capacity: number;
  location?: string;
  event_type?: string;
  price?: number;
  status: boolean;
}

// Lo que envías al crear o actualizar (omitimos el id)
export type EventInput = Omit<Event, "id">;

// --- HOOK ---
export function useEvents() {
  const { keycloak, initialized } = useKeycloak();
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Construye headers con Bearer token de Keycloak
  const authHeaders = useCallback((): Record<string, string> => {
    const headers: Record<string, string> = { "Content-Type": "application/json" };
    if (keycloak?.token) {
      headers["Authorization"] = `Bearer ${keycloak.token}`;
    }
    return headers;
  }, [keycloak]);

  // 👉 GET /events/
  const fetchEvents = useCallback(async () => {
    if (!keycloak?.authenticated) {
      setError("No estás autenticado");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE_URL}/`, {
        method: "GET",
        headers: authHeaders(),
      });
      if (!res.ok) {
        const details = await res.json().catch(() => ({}));
        throw new Error(details?.detail?.message || "Error obteniendo eventos.");
      }
      const payload = await res.json();
      setEvents(payload.data ?? payload);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [authHeaders, keycloak]);

  // 👉 POST /events/create
  const createEvent = useCallback(
    async (data: EventInput) => {
      if (!keycloak?.authenticated) {
        setError("No estás autenticado");
        return false;
      }
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${API_BASE_URL}/create`, {
          method: "POST",
          headers: authHeaders(),
          body: JSON.stringify(data),
        });
        if (!res.ok) {
          const details = await res.json().catch(() => ({}));
          throw new Error(details?.detail?.message || "No se pudo crear el evento.");
        }
        const payload = await res.json();
        const newEvent: Event = payload.data ?? payload;
        setEvents((prev) => [...prev, newEvent]);
        return true;
      } catch (err: any) {
        setError(err.message);
        return false;
      } finally {
        setLoading(false);
      }
    },
    [authHeaders, keycloak]
  );

  // 👉 DELETE /events/delete/:id
  const deleteEvent = useCallback(
    async (id: string) => {
      if (!keycloak?.authenticated) {
        setError("No estás autenticado");
        return;
      }
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${API_BASE_URL}/delete/${id}`, {
          method: "DELETE",
          headers: authHeaders(),
        });
        if (!res.ok) {
          const details = await res.json().catch(() => ({}));
          throw new Error(details?.detail?.message || "No se pudo eliminar el evento.");
        }
        setEvents((prev) => prev.filter((e) => e.id !== id));
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    },
    [authHeaders, keycloak]
  );

  // Carga inicial cuando Keycloak esté listo
  useEffect(() => {
    if (initialized) {
      fetchEvents();
    }
  }, [initialized, fetchEvents]);

  return {
    events,
    loading,
    error,
    fetchEvents,
    createEvent,
    deleteEvent,
  };
}
