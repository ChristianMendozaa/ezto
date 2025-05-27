// app/ClientRootLayout.tsx
"use client";

import React from "react";
import { ThemeProvider } from "@/components/theme-provider";
import { LanguageProvider } from "@/components/language-provider";
import { ReactKeycloakProvider } from "@react-keycloak/web";
import keycloak from "@/src/keycloak";
import { AuthProvider } from "@/lib/auth-context";

export default function ClientRootLayout({ children }: { children: React.ReactNode }) {
  return (
    <ReactKeycloakProvider
      authClient={keycloak}
      initOptions={{
        onLoad: "check-sso",
        checkLoginIframe: false,
      }}
    >
      <AuthProvider>
        <LanguageProvider>
          <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
            {children}
          </ThemeProvider>
        </LanguageProvider>
      </AuthProvider>
    </ReactKeycloakProvider>
  );
}
