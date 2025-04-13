import { cookies } from "next/headers";
import { NextResponse } from "next/server";

export async function GET() {
  try {
    // 🔍 Intentar leer la cookie directamente desde Next.js
    const authToken = cookies().get("authToken")?.value;

    const res = await fetch(process.env.NEXT_PUBLIC_BACKEND_URL + "/auth/me", {
      method: "GET",
      credentials: "include", //   Asegura que las cookies se envíen
      headers: {
        "Content-Type": "application/json",
        "Cookie": `authToken=${authToken}`, //   Forzar el envío manual
      },
      cache: "no-store", //   Evita caché en la solicitud
    });


    if (!res.ok) {
      return NextResponse.json({ error: "No autenticado" }, { status: res.status });
    }

    const user = await res.json();
    return NextResponse.json(user);
  } catch (error) {

    return NextResponse.json({ error: "Error de autenticación" }, { status: 500 });
  }
}
