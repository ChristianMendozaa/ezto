import { useState, useEffect } from "react";
import { useAuthHeaders } from "@/hooks/use-auth-header";

export interface PurchaseItem {
  product_id: string;
  quantity: number;
  unit_price: number;
  discount: number;
}

export interface Purchase {
  sale_id: string;
  client_id: string;
  items: PurchaseItem[];
  payment_method: string;
  notes: string;
  total_amount: number;
  tax_amount: number;
  sale_date: string; // ISO 8601
  seller_id: string;
  invoice_number: string;
  status: string;
}

const API_URL = "http://localhost";

export const usePurchases = () => {
  const [purchases, setPurchases] = useState<Purchase[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const rawAuth = useAuthHeaders();

  const authHeader: Record<string,string> =
    rawAuth && typeof rawAuth.Authorization === 'string'
      ? { Authorization: rawAuth.Authorization }
      : {};

  const fetchPurchases = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/purchases/`, {
        headers: { ...authHeader }
      });
      if (!res.ok) throw new Error(await res.text());
      const data: Purchase[] = await res.json();
      setPurchases(data);
    } catch (err) {
      console.error('Error fetching purchases', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPurchases();
  }, []);

  return { purchases, loading, fetchPurchases };
};
