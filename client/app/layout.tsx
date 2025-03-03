import { Inter } from "next/font/google"
import "./globals.css"
import { ThemeProvider } from "@/components/theme-provider"
import { LanguageProvider } from "@/components/language-provider"
import type React from "react"
import { AuthProvider } from "@/lib/auth-context";

const inter = Inter({ subsets: ["latin"] })

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <AuthProvider>
      <html lang="es" suppressHydrationWarning>
        <body className={inter.className}>
          <LanguageProvider>
            <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
              {children}
            </ThemeProvider>
          </LanguageProvider>
        </body>
      </html>
    </AuthProvider>
  )
}



import './globals.css'

export const metadata = {
  generator: 'v0.dev'
};
