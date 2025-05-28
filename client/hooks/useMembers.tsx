// hooks/useMembers.ts
import { useState, useCallback, useEffect } from "react";
import axios from "axios";
import { useKeycloak } from "@react-keycloak/web";

export interface Member {
    id: string;
    name: string;
    email: string;
    nfc_id?: string;
    status: "activo" | "inactivo" | "suspendido";
    join_date: string; // ISO format
}

interface MembersResponse {
    status: string;
    message: string | null;
    data: Member[];
}

const API_BASE = `${process.env.NEXT_PUBLIC_BACKEND_URL?.replace(/\/$/, "")}/members/api`;

export function useMembers() {
    const { keycloak, initialized } = useKeycloak();
    const [members, setMembers] = useState<Member[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    async function getAuthHeaders(): Promise<Record<string, string>> {
        if (!keycloak.authenticated) throw new Error("Usuario no autenticado");

        await keycloak.updateToken(60).catch(() => {
            throw new Error("No se pudo actualizar el token");
        });

        return {
            Authorization: `Bearer ${keycloak.token}`,
            "Content-Type": "application/json",
        };
    }

    const fetchMembers = useCallback(async () => {
        if (!keycloak?.authenticated) {
            setError("No estás autenticado");
            return;
        }

        setLoading(true);
        setError(null);
        try {
            const headers = await getAuthHeaders();
            const res = await axios.get<MembersResponse>(`${API_BASE}`, { headers });

            if (res.data?.status === "success" && Array.isArray(res.data.data)) {
                setMembers(res.data.data);
            } else {
                setError("Respuesta inesperada del servidor");
                setMembers([]);
            }
        } catch (err: any) {
            setError(err.message || "Error al obtener miembros");
        } finally {
            setLoading(false);
        }
    }, [keycloak]);

    const getMemberById = useCallback(async (id: string) => {
        try {
            const headers = await getAuthHeaders();
            const res = await axios.get<Member>(`${API_BASE}/${id}`, { headers });
            return res.data;
        } catch (err: any) {
            throw new Error(err.message || "Error al obtener miembro por ID");
        }
    }, [keycloak]);

    const createMember = useCallback(async (data: Member) => {
        try {
            const headers = await getAuthHeaders();
            const res = await axios.post<Member>(`${API_BASE}/create`, data, { headers });
            await fetchMembers();
            return res.data; // ✅ aquí se devuelve el miembro con su ID real generado por Firestore
        } catch (err: any) {
            throw new Error(err.message || "Error al registrar miembro");
        }
    }, [keycloak, fetchMembers]);


    const updateMember = useCallback(async (id: string, updates: Partial<Member>) => {
        try {
            const headers = await getAuthHeaders();
            const res = await axios.patch<Member>(`${API_BASE}/update/${id}`, updates, { headers });
            await fetchMembers();
            return res.data;
        } catch (err: any) {
            throw new Error(err.message || "Error al actualizar miembro");
        }
    }, [keycloak, fetchMembers]);

    const deleteMember = useCallback(async (id: string) => {
        try {
            const headers = await getAuthHeaders();
            await axios.delete(`${API_BASE}/delete/${id}`, { headers });
            await fetchMembers();
        } catch (err: any) {
            throw new Error(err.message || "Error al eliminar miembro");
        }
    }, [keycloak, fetchMembers]);

    useEffect(() => {
        if (initialized) {
            fetchMembers();
        }
    }, [initialized, fetchMembers]);

    return {
        members,
        loading,
        error,
        fetchMembers,
        getMemberById,
        createMember,
        updateMember,
        deleteMember,
    };
}
