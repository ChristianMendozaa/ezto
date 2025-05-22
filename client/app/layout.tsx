// client/app/layout.tsx
"use client"

import React from "react";
import { Inter } from "next/font/google";
import "./globals.css";
import { ThemeProvider } from "@/components/theme-provider";
import { LanguageProvider } from "@/components/language-provider";

import { ReactKeycloakProvider } from "@react-keycloak/web";
import keycloak from "@/src/keycloak";
import { AuthProvider } from "@/lib/auth-context";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "EzTo App",
  description: "Plataforma EzTo",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es" suppressHydrationWarning>
      <body className={inter.className}>
        <ReactKeycloakProvider
          authClient={keycloak}
          initOptions={{
            onLoad: "login-required",
            checkLoginIframe: false,
          }}
          // opcional: guarda el token en memory o state
        >
          <AuthProvider>
            <LanguageProvider>
              <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
                {children}
              </ThemeProvider>
            </LanguageProvider>
          </AuthProvider>
        </ReactKeycloakProvider>
      </body>
    </html>
  );
}
