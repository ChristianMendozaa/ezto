"use client"

import type React from "react"

import { useState } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { useLanguage } from "@/lib/hooks/use-language"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { ThemeToggle } from "@/components/theme-toggle"
import { LanguageToggle } from "@/components/language-toggle"
import { Dumbbell } from "lucide-react"
import { auth } from "@/lib/firebaseConfig";
import { signInWithEmailAndPassword } from "firebase/auth";
import { useAuth } from "@/lib/auth-context";

export default function LoginPage() {
  const { t } = useLanguage()
  const router = useRouter()
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [loading, setLoading] = useState(false);
  const { setUser } = useAuth(); //  Usamos AuthContext para actualizar el usuario

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!email || !password) {
      alert("Por favor, completa todos los campos.");
      return;
    }

    setLoading(true);
    try {

      //  1. Borrar cualquier cookie de sesión previa antes de autenticarse
      await fetch(process.env.NEXT_PUBLIC_BACKEND_URL + "/auth/logout", {
        method: "POST",
        credentials: "include",
      });

      const userCredential = await signInWithEmailAndPassword(auth, email, password);
      console.log(userCredential);
      const token = await userCredential.user.getIdToken(true);
      console.log(token)
      console.log(Math.floor(Date.now() / 1000)); // Muestra la hora en segundos desde UNIX epoch
      if (auth.currentUser) {
        auth.currentUser.getIdTokenResult()
          .then((idTokenResult) => {
            console.log("Hora de emisión del token (iat):", idTokenResult.claims.iat);
            console.log("Hora actual en el cliente:", Math.floor(Date.now() / 1000));
          })
          .catch((error) => {
            console.error("Error obteniendo el token:", error);
          });
      } else {
        console.error("No hay usuario autenticado.");
      }


      const response = await fetch(process.env.NEXT_PUBLIC_BACKEND_URL + "/auth/login", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        credentials: "include",
      });

      if (!response.ok) {
        throw new Error("Error en la autenticación. Revisa tu usuario o contraseña.");
      }

      const data = await response.json();

      //  Actualizar el estado global del usuario
      setUser(data);

      //  Redirigir según el rol
      if (data.role === "gym_owner") {
        router.replace("/dashboard");
      } else {
        router.replace("/client");
      }

    } catch (error: any) {
      
      alert(error.message);
      //  1. Borrar cualquier cookie de sesión previa antes de autenticarse
      await fetch(process.env.NEXT_PUBLIC_BACKEND_URL + "/auth/logout", {
        method: "POST",
        credentials: "include",
      });

    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-100 dark:bg-gray-900">
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-2">
            <Dumbbell className="h-6 w-6 text-orange-500" />
            <span className="text-xl font-bold">EzTo</span>
          </div>
          <nav className="hidden md:flex gap-6">
            <Link href="/#features" className="text-sm font-medium hover:text-orange-500">
              {t("nav.features")}
            </Link>
            <Link href="/#pricing" className="text-sm font-medium hover:text-orange-500">
              {t("nav.pricing")}
            </Link>
            <Link href="/#testimonials" className="text-sm font-medium hover:text-orange-500">
              {t("nav.testimonials")}
            </Link>
            <Link href="/#blog" className="text-sm font-medium hover:text-orange-500">
              {t("nav.blog")}
            </Link>
          </nav>
          <div className="flex items-center gap-2">
            <LanguageToggle />
            <ThemeToggle />
          </div>
        </div>
      </header>
      <main className="flex-grow flex items-center justify-center">
        <Card className="w-full max-w-md">
          <CardHeader>
            <CardTitle className="text-2xl font-bold">{t("auth.login.title")}</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email">{t("auth.login.emailLabel")}</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="name@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="password">{t("auth.login.passwordLabel")}</Label>
                <Input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
              <Button type="submit" className="w-full">
                {t("auth.login.loginButton")}
              </Button>
            </form>
          </CardContent>
          <CardFooter className="flex flex-col space-y-2">
            <Link href="/forgot-password" className="text-sm text-blue-500 hover:underline">
              {t("auth.login.forgotPassword")}
            </Link>
            <div className="text-sm">
              {t("auth.login.noAccount")}{" "}
              <Link href="/register" className="text-blue-500 hover:underline">
                {t("auth.login.signUp")}
              </Link>
            </div>
          </CardFooter>
        </Card>
      </main>
    </div>
  )
}