import { Avatar, AvatarFallback } from "@/components/ui/avatar"

export function RecentSales() {
  return (
    <div className="space-y-8">
      <div className="flex items-center">
        <Avatar className="h-9 w-9">
          <AvatarFallback>JD</AvatarFallback>
        </Avatar>
        <div className="ml-4 space-y-1">
          <p className="text-sm font-medium leading-none">Juan Díaz</p>
          <p className="text-sm text-muted-foreground">Acceso: 09:45 AM</p>
        </div>
        <div className="ml-auto font-medium">Sala Principal</div>
      </div>
      <div className="flex items-center">
        <Avatar className="h-9 w-9">
          <AvatarFallback>MR</AvatarFallback>
        </Avatar>
        <div className="ml-4 space-y-1">
          <p className="text-sm font-medium leading-none">María Rodríguez</p>
          <p className="text-sm text-muted-foreground">Acceso: 09:30 AM</p>
        </div>
        <div className="ml-auto font-medium">Área Cardio</div>
      </div>
      <div className="flex items-center">
        <Avatar className="h-9 w-9">
          <AvatarFallback>CL</AvatarFallback>
        </Avatar>
        <div className="ml-4 space-y-1">
          <p className="text-sm font-medium leading-none">Carlos López</p>
          <p className="text-sm text-muted-foreground">Acceso: 09:15 AM</p>
        </div>
        <div className="ml-auto font-medium">Sala de Pesas</div>
      </div>
      <div className="flex items-center">
        <Avatar className="h-9 w-9">
          <AvatarFallback>AG</AvatarFallback>
        </Avatar>
        <div className="ml-4 space-y-1">
          <p className="text-sm font-medium leading-none">Ana García</p>
          <p className="text-sm text-muted-foreground">Acceso: 09:00 AM</p>
        </div>
        <div className="ml-auto font-medium">Sala de Yoga</div>
      </div>
    </div>
  )
}

