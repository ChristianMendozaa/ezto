// client/hooks/useKeycloakAuth.tsx
"use client";

import { useKeycloak } from "@react-keycloak/web";
import Keycloak from "keycloak-js";

export function useKeycloakAuth() {
  // Sin genéricos
  const { keycloak, initialized } = useKeycloak();

  if (!initialized || !keycloak) {
    return { isReady: false, isAuthenticated: false };
  }

  return {
    isReady: true,
    isAuthenticated: keycloak.authenticated,
    token: keycloak.token!,
    login: () => keycloak.login(),
    logout: () => keycloak.logout({ redirectUri: window.location.origin }),
    username: (keycloak.tokenParsed as any)?.preferred_username as string,
  };
}
