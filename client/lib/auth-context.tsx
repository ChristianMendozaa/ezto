"use client";

import { createContext, useContext, useEffect, useState } from "react";
import { useRouter, usePathname } from "next/navigation";
import { useKeycloak } from "@react-keycloak/web";

interface User {
  user_id: string;
  email: string;
  role: "gym_owner" | "gym_member";
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const { keycloak, initialized } = useKeycloak();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    if (!initialized || !keycloak) return;

    if (!keycloak.authenticated) {
      // 🔐 Solo forzamos login en rutas protegidas
      const protectedRoutes = ["/dashboard", "/client"];
      const isProtected = protectedRoutes.some((route) => pathname.startsWith(route));
      if (isProtected) {
        keycloak.login();
        return;
      }

      // No está autenticado y no está en ruta protegida → continuar como visitante
      setLoading(false);
      return;
    }

    // ✅ Usuario autenticado → extraemos datos
    const parsed = keycloak.tokenParsed as any;
    setUser({
      user_id: parsed.sub,
      email: parsed.email,
      role: parsed.realm_access.roles.includes("gym_owner")
        ? "gym_owner"
        : "gym_member",
    });

    setLoading(false);
  }, [initialized, keycloak, pathname]);

  // redirige automáticamente tras login exitoso
  useEffect(() => {
    if (loading || !user) return;

    if (pathname === "/" || pathname === "/login") {
      if (user.role === "gym_owner") router.replace("/dashboard");
      else router.replace("/client");
    }
  }, [loading, user, pathname, router]);

  const logout = async () => {
    keycloak.logout({
      redirectUri: window.location.origin,
    });
  };

  return (
    <AuthContext.Provider value={{ user, loading, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be inside an AuthProvider");
  return ctx;
};
