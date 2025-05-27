// app/layout.tsx (🚫 sin "use client")
import "./globals.css";
import { Inter } from "next/font/google";
import ClientRootLayout from "./ClientRootLayout";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "EzTo App",
  description: "Plataforma EzTo",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es" suppressHydrationWarning>
      <body className={inter.className}>
        <ClientRootLayout>{children}</ClientRootLayout>
      </body>
    </html>
  );
}
