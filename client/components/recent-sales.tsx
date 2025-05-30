import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { format } from "date-fns"
import { AccessData } from "@/hooks/use-realtime-dashboard"

interface Props {
  accesses: AccessData[]
}

export function RecentSales({ accesses }: Props) {
  return (
    <div className="space-y-8">
      {accesses.slice(0, 5).map((access) => {
        const initials = access.name
          .split(" ")
          .map((n) => n[0])
          .join("")
          .slice(0, 2)
          .toUpperCase()

        const formattedEntrada = access.entrada
          ? format(new Date(access.entrada), "hh:mm a")
          : "—"

        const formattedSalida = access.salida
          ? format(new Date(access.salida), "hh:mm a")
          : null

        return (
          <div key={access.id} className="flex items-center">
            <Avatar className="h-9 w-9">
              <AvatarFallback>{initials}</AvatarFallback>
            </Avatar>
            <div className="ml-4 space-y-1">
              <p className="text-sm font-medium leading-none">{access.name}</p>
              <p className="text-sm text-muted-foreground">
                Acceso: {formattedEntrada}
                {formattedSalida && ` · Salió: ${formattedSalida}`}
              </p>
            </div>
            <div className="ml-auto font-medium">{access.plan || "Área General"}</div>
          </div>
        )
      })}
    </div>
  )
}
