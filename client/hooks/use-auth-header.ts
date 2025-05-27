// lib/hooks/use-auth-header.ts
import { useKeycloak } from "@react-keycloak/web"

export function useAuthHeaders() {
  const { keycloak } = useKeycloak()

  const isAuthenticated = keycloak?.authenticated
  const token = keycloak?.token

  const authHeader = isAuthenticated && token
    ? { Authorization: `Bearer ${token}` }
    : {}

  return authHeader
}
