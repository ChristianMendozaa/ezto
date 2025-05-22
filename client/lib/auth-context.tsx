"use client";
import { createContext, useContext, useEffect, useState } from "react";
import { useRouter } from "next/navigation";

interface User {
  user_id: string;
  email: string;
  role: "gym_owner" | "gym_member";
}

interface AuthContextType {
  user: User | null;
  setUser: (user: User | null) => void;
  loading: boolean;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await fetch(process.env.NEXT_PUBLIC_BACKEND_URL +"/auth/me", { credentials: "include" });

        if (!res.ok) throw new Error("No autenticado");
        
        const data = await res.json();
        
        setUser(data);
      } catch (error) {
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  useEffect(() => {
    if (!loading && user) {
      if (user.role === "gym_owner") {
        router.replace("/dashboard");
      } else {
        router.replace("/client");
      }
    }
  }, [loading, user, router]);

  const logout = async () => {
    //  1. Borrar cualquier cookie de sesión previa antes de autenticarse
    await fetch(process.env.NEXT_PUBLIC_BACKEND_URL + "/auth/logout", {
      method: "POST",
      credentials: "include",
    });
    setUser(null);
    router.replace("/login");
  };

  return (
    <AuthContext.Provider value={{ user, setUser, loading, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within an AuthProvider");
  return context;
};
