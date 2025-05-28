// hooks/useAccessAlerts.ts
import { useEffect, useState, useCallback } from "react";

export interface AccessAlert {
  name: string
  type: string
  location: string
  timestamp: string
}

const API_BASE_URL = "https://nfc-ezto.onrender.com/nfc/access";

export function useAccessAlerts() {
  const [alerts, setAlerts] = useState<AccessAlert[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchAlerts = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE_URL}/alerts`, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      });
      if (!res.ok) {
        const details = await res.json().catch(() => ({}));
        throw new Error(details?.detail?.message || "Error obteniendo alertas de acceso.");
      }
      const payload = await res.json();
      setAlerts(payload);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchAlerts();
  }, [fetchAlerts]);

  return {
    alerts,
    loading,
    error,
    refetch: fetchAlerts,
  };
}
