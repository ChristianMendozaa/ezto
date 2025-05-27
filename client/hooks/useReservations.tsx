import { useEffect, useState, useCallback } from "react";
import { useKeycloak } from "@react-keycloak/web";

// Ajusta si tu gateway corre en otro URL/puerto
const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_GATEWAY_URL?.replace(/\/$/, "") ||
  "http://localhost/reservations";

export interface Reservation {
  id: string;
  user_id: string;
  class_id: string;
  reservation_date: string; // ISO string UTC
  status: "active" | "cancelled" | "completed";
}

// Lo que se envía al crear (omitiendo el id)
export interface ReservationInput extends Omit<Reservation, "id"> {}

export function useReservations() {
  const { keycloak, initialized } = useKeycloak();
  const [reservations, setReservations] = useState<Reservation[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  function authHeaders(): Record<string, string> {
    const headers: Record<string, string> = { "Content-Type": "application/json" };
    if (keycloak?.token) {
      headers["Authorization"] = `Bearer ${keycloak.token}`;
    }
    return headers;
  }

  const fetchReservations = useCallback(async () => {
    if (!keycloak?.authenticated) {
      setError("No estás autenticado");
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE_URL}/reservations/`, {
        method: "GET",
        headers: authHeaders(),
      });

      if (!res.ok) {
        const details = await res.json().catch(() => ({}));
        throw new Error(details?.detail?.message || "Error obteniendo reservas.");
      }

      const payload = await res.json();
      setReservations(payload.data ?? payload);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [keycloak]);

  const createReservation = useCallback(
    async (data: ReservationInput) => {
      if (!keycloak?.authenticated) {
        setError("No estás autenticado");
        return false;
      }

      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${API_BASE_URL}/reservations/create`, {
          method: "POST",
          headers: authHeaders(),
          body: JSON.stringify(data),
        });

        if (!res.ok) {
          const details = await res.json().catch(() => ({}));
          throw new Error(details?.detail?.message || "No se pudo crear la reserva.");
        }

        const payload = await res.json();
        const newRes: Reservation = payload.data ?? payload;
        setReservations((prev) => [...prev, newRes]);
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

  const deleteReservation = useCallback(
    async (id: string) => {
      if (!keycloak?.authenticated) {
        setError("No estás autenticado");
        return;
      }

      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${API_BASE_URL}/reservations/delete/${id}`, {
          method: "DELETE",
          headers: authHeaders(),
        });

        if (!res.ok) {
          const details = await res.json().catch(() => ({}));
          throw new Error(details?.detail?.message || "No se pudo eliminar la reserva.");
        }

        setReservations((prev) => prev.filter((r) => r.id !== id));
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
      fetchReservations();
    }
  }, [initialized, fetchReservations]);

  return {
    reservations,
    loading,
    error,
    createReservation,
    deleteReservation,
    refetch: fetchReservations,
  };
}
