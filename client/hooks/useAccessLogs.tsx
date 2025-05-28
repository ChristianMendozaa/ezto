// hooks/useAccessLogs.ts
import { useEffect, useState, useCallback } from "react";

export interface AccessLog {
  user_id: string | null
  name: string
  nfc_id: string
  timestamp: string
  status: "granted" | "denied"
  reason?: string
  device_type: string
}

const API_BASE_URL = "https://nfc-ezto.onrender.com/nfc/access";

export function useAccessLogs() {
  const [logs, setLogs] = useState<AccessLog[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchLogs = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE_URL}/logs`, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      });
      if (!res.ok) {
        const details = await res.json().catch(() => ({}));
        throw new Error(details?.detail?.message || "Error obteniendo logs de acceso.");
      }
      const payload = await res.json();
      setLogs(payload);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchLogs();
  }, [fetchLogs]);

  return {
    logs,
    loading,
    error,
    refetch: fetchLogs,
  };
}