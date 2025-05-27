import { useState, useEffect } from "react";
import { useAuthHeaders } from "@/hooks/use-auth-header";

export interface Supplier {
  id: string;
  name: string;
  contact_email: string;
  phone: string;
  address: string;
  tax_id: string;
  payment_terms: string;
  status: string;
  created_at: string; // YYYY-MM-DD
  last_updated: string; // YYYY-MM-DD
  products_offered: number;
}

const API_URL_SUP = "http://localhost";

export const useSuppliers = () => {
  const [suppliers, setSuppliers] = useState<Supplier[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const rawAuth = useAuthHeaders();

  const authHeader: Record<string,string> =
    rawAuth && typeof rawAuth.Authorization === 'string'
      ? { Authorization: rawAuth.Authorization }
      : {};

  const fetchSuppliers = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_URL_SUP}/suppliers/`, {
        headers: { ...authHeader }
      });
      if (!res.ok) throw new Error(await res.text());
      const data: Supplier[] = await res.json();
      setSuppliers(data);
    } catch (err) {
      console.error('Error fetching suppliers', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSuppliers();
  }, []);

  return { suppliers, loading, fetchSuppliers };
};

