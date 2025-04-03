import { useState, useEffect } from "react";
import axios from "axios";

const API_URL = "http://localhost:8000/promotions"; // Backend está en 8000


// Definimos el tipo de promoción según tu backend
interface Promotion {
  id: string;
  name: string;
  description: string;
  start_date: string;
  end_date: string;
  discount_type: string;
  discount_value: string;
  applicable_to: string;
  auto_apply: boolean;
  promo_code?: string;
  status: string;
}

export function usePromotions() {
  const [promotions, setPromotions] = useState<Promotion[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchPromotions();
  }, []);

  // Obtener todas las promociones
  const fetchPromotions = async () => {
    setLoading(true);
    console.log("🔹 Enviando solicitud GET a:", `${API_URL}/list`);
  
    try {
      const response = await axios.get<Promotion[]>(`${API_URL}/list`, {
        headers: { "Content-Type": "application/json" },
        withCredentials: false,  // 🔹 Intenta cambiar esto a `false`
      });
  
      console.log("✅ Respuesta de la API:", response.data);
      setPromotions(response.data);
    } catch (err) {
      console.error("❌ Error al obtener promociones:", err);
    } finally {
      setLoading(false);
    }
  };
  

  // Crear una nueva promoción
  const createPromotion = async (promotionData: Omit<Promotion, "id">) => {
    try {
      const formattedData = {
        ...promotionData,
        start_date: new Date(promotionData.start_date).toISOString().split("T")[0],
        end_date: new Date(promotionData.end_date).toISOString().split("T")[0],
      };
      const response = await axios.post<Promotion>(`${API_URL}/create`, formattedData);
      
      // ⚡ ACTUALIZAR LISTA EN TIEMPO REAL
      setPromotions((prevPromotions) => [...prevPromotions, response.data]);
  
    } catch (err) {
      setError((err as Error).message);
    }
  };
  
  

  // Actualizar una promoción existente
  const updatePromotion = async (id: string, updatedData: Partial<Promotion>) => {
    try {
      await axios.put(`${API_URL}/update/${id}`, { id, ...updatedData });
      setPromotions(promotions.map((promo) => (promo.id === id ? { ...promo, ...updatedData } : promo)));
    } catch (err) {
      setError((err as Error).message);
    }
  };

  // Eliminar una promoción
  const deletePromotion = async (id: string) => {
    try {
      await axios.delete(`${API_URL}/delete/${id}`);
      setPromotions(promotions.filter((promo) => promo.id !== id));
    } catch (err) {
      setError((err as Error).message);
    }
  };

  return { promotions, loading, error, fetchPromotions, createPromotion, updatePromotion, deletePromotion };
}
