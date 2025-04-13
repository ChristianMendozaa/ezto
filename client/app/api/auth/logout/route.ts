import { NextResponse } from "next/server";

export async function POST() {
  try {
    //   Elimina la cookie en la respuesta
    const response = NextResponse.json({ message: "Logout exitoso" });
    response.headers.set("Set-Cookie", "authToken=; Path=/; HttpOnly; Secure=False; SameSite=Lax; Max-Age=0");

    return response;
  } catch (error) {
    return NextResponse.json({ error: "Error en logout" }, { status: 500 });
  }
}
