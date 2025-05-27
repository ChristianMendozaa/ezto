// hooks/useNfcPairing.ts
import { useState, useCallback } from "react";
import axios from "axios";
import { useKeycloak } from "@react-keycloak/web";

const NFC_API_BASE = "https://nfc-ezto.onrender.com/nfc";

export interface PairingCodeResponse {
    pairing_code: string;
    message: string;
}

export function useNfcPairing() {
    const { keycloak } = useKeycloak();
    const [pairingCode, setPairingCode] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const generatePairingCode = useCallback(async (memberId: string) => {
        if (!keycloak.authenticated) {
            setError("No autenticado");
            return;
        }

        setLoading(true);
        setError(null);
        setPairingCode(null);

        try {
            const headers = {
                Authorization: `Bearer ${keycloak.token}`,
                "Content-Type": "application/json",
            };

            const body = { member_id: memberId };

            // 🔍 Este es el log que te dirá exactamente qué se está enviando
            console.log("Enviando al backend para pairing-code:", {
                url: `${NFC_API_BASE}/pairing-code`,
                headers,
                body
            });

            const response = await axios.post<PairingCodeResponse>(
                `${NFC_API_BASE}/pairing-code`,
                body,
                { headers }
            );

            setPairingCode(response.data.pairing_code);
        } catch (err: any) {
            setError(err.response?.data?.detail || err.message || "Error al generar código de emparejamiento");
        } finally {
            setLoading(false);
        }
    }, [keycloak]);


    return {
        pairingCode,
        loading,
        error,
        generatePairingCode,
    };
}
