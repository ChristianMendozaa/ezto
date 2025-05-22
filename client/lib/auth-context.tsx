// client/app/lib/auth-context.tsx
"use client";

import { createContext, useContext, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
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

  // Cuando Keycloak ya esté listo:
  useEffect(() => {
    if (!initialized) return;
    if (!keycloak?.authenticated) {
      keycloak.login();
      return;
    }
    // extraemos datos del token
    const parsed = keycloak.tokenParsed as any;
    setUser({
      user_id: parsed.sub,
      email: parsed.email,
      role: parsed.realm_access.roles.includes("gym_owner")
        ? "gym_owner"
        : "gym_member",
    });
    setLoading(false);
  }, [initialized, keycloak]);

  // redirige según rol
  useEffect(() => {
    if (loading || !user) return;
    if (user.role === "gym_owner") router.replace("/dashboard");
    else router.replace("/client");
  }, [loading, user, router]);

  const logout = async () => {
    // 1) llamas a tu endpoint backend para borrar la cookie
    await fetch(process.env.NEXT_PUBLIC_BACKEND_URL + "/auth/logout", {
      method: "POST",
      credentials: "include",
    });
    // 2) luego logout Keycloak
    keycloak.logout({ redirectUri: window.location.origin });
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
