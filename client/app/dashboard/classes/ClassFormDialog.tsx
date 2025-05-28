// components/ClassFormDialog.tsx
"use client"

import { useState, useEffect } from "react"
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from "@/components/ui/select"
import { Label } from "@/components/ui/label"
import { Plus, Trash2 } from "lucide-react"
import { Session } from "@/hooks/useClasses"
import { useLanguage } from "@/lib/hooks/use-language"

const weekDays: Session["day"][] = [
  "Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"
]

export interface ClassFormData {
  name: string
  instructor: string
  capacity: number
  location: string
  description: string
  status: boolean
  sessions: Session[]
}

export interface ClassFormDialogProps {
  initial?: ClassFormData & { tmpSession?: Session }
  trigger: React.ReactNode
  onSave: (data: ClassFormData) => Promise<boolean>
}

export function ClassFormDialog({ initial, trigger, onSave }: ClassFormDialogProps) {
  const { t } = useLanguage()
  const [open, setOpen] = useState(false)
  const [form, setForm] = useState<Required<ClassFormData> & { tmpSession: Session }>({
    name: "",
    instructor: "",
    capacity: 0,
    location: "",
    description: "",
    status: true,
    sessions: [],
    tmpSession: { day: "Monday", start_time: "09:00:00", end_time: "10:00:00" },
  })

  useEffect(() => {
    if (initial) {
      setForm({
        ...initial,
        tmpSession: initial.tmpSession ?? {
          day: "Monday",
          start_time:"09:00:00",
          end_time:"10:00:00"
        }
      })
    }
  }, [initial])

  const addSession = () => {
    setForm(f => ({
      ...f,
      sessions: [...f.sessions, f.tmpSession],
      tmpSession: { day: "Monday", start_time:"09:00:00", end_time:"10:00:00" }
    }))
  }
  const removeSession = (i:number) => {
    setForm(f => ({
      ...f,
      sessions: f.sessions.filter((_,idx)=>idx!==i)
    }))
  }

  const handleSave = async () => {
    const { tmpSession, ...payload } = form
    console.log("▶️ payload a enviar:", JSON.stringify(payload, null, 2))
    const ok = await onSave(payload)
    if (ok) {
      setOpen(false)
      if (!initial) {
        setForm({
          name:"", instructor:"", capacity:0, location:"",
          description:"", status:true, sessions:[],
          tmpSession:{ day:"Monday", start_time:"09:00:00", end_time:"10:00:00" }
        })
      }
    }
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>{trigger}</DialogTrigger>
      <DialogContent className="p-6 sm:p-8 w-full max-w-xl">
        <DialogHeader>
          <DialogTitle>
            { initial ? t("classes.editClass") : t("classes.addClass") }
          </DialogTitle>
        </DialogHeader>

        {/* ==== FORMULARIO ==== */}
        <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-6">
          {/* Nombre */}
          <div className="flex flex-col">
            <Label htmlFor="name">{t("classes.form.name")}</Label>
            <Input
              id="name"
              className="mt-1"
              value={form.name}
              onChange={e=>setForm(f=>({...f,name:e.target.value}))}
            />
          </div>

          {/* Instructor */}
          <div className="flex flex-col">
            <Label htmlFor="instructor">{t("classes.form.instructor")}</Label>
            <Input
              id="instructor"
              className="mt-1"
              value={form.instructor}
              onChange={e=>setForm(f=>({...f,instructor:e.target.value}))}
            />
          </div>

          {/* Capacidad */}
          <div className="flex flex-col">
            <Label htmlFor="capacity">{t("classes.form.capacity")}</Label>
            <Input
              id="capacity"
              type="number"
              className="mt-1"
              value={form.capacity}
              onChange={e=>setForm(f=>({...f,capacity:+e.target.value}))}
            />
          </div>

          {/* Ubicación */}
          <div className="flex flex-col">
            <Label htmlFor="location">{t("classes.form.location")}</Label>
            <Input
              id="location"
              className="mt-1"
              value={form.location}
              onChange={e=>setForm(f=>({...f,location:e.target.value}))}
            />
          </div>

          {/* Descripción (ocupa dos columnas en sm) */}
          <div className="sm:col-span-2 flex flex-col">
            <Label htmlFor="description">{t("classes.form.description")}</Label>
            <Textarea
              id="description"
              className="mt-1"
              rows={4}
              value={form.description}
              onChange={e=>setForm(f=>({...f,description:e.target.value}))}
            />
          </div>

          {/* Estado */}
          <div className="flex flex-col">
            <Label htmlFor="status">{t("classes.form.status")}</Label>
            <Select
              id="status"
              className="mt-1"
              value={form.status ? "active" : "cancelled"}
              onValueChange={v=>setForm(f=>({...f,status:v==="active"}))}
            >
              <SelectTrigger><SelectValue/></SelectTrigger>
              <SelectContent>
                <SelectItem value="active">{t("classes.status.active")}</SelectItem>
                <SelectItem value="cancelled">{t("classes.status.cancelled")}</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Sesiones (dos columnas) */}
          <div className="sm:col-span-2">
            <h3 className="text-base font-medium mb-2">
              {t("classes.form.sessions")}
            </h3>

            <div className="flex flex-col sm:flex-row sm:items-end gap-2">
              {/* Día */}
              <div className="flex-1 flex flex-col">
                <Label>{t("classes.form.sessionDay")}</Label>
                <Select
                  className="mt-1"
                  value={form.tmpSession.day}
                  onValueChange={d=>
                    setForm(f=>({
                      ...f,
                      tmpSession:{...f.tmpSession,day:d as Session["day"]}
                    }))
                  }
                >
                  <SelectTrigger><SelectValue/></SelectTrigger>
                  <SelectContent>
                    {weekDays.map(d=>
                      <SelectItem key={d} value={d}>
                        {t(`days.${d.toLowerCase()}`)}
                      </SelectItem>
                    )}
                  </SelectContent>
                </Select>
              </div>

              {/* Hora inicio */}
              <div className="flex-1 flex flex-col">
                <Label>{t("classes.form.startTime")}</Label>
                <Input
                  type="time"
                  className="mt-1 w-full sm:w-24"
                  value={form.tmpSession.start_time.slice(0,5)}
                  onChange={e=>
                    setForm(f=>({
                      ...f,
                      tmpSession:{...f.tmpSession,start_time:e.target.value + ":00"}
                    }))
                  }
                />
              </div>

              {/* Hora fin */}
              <div className="flex-1 flex flex-col">
                <Label>{t("classes.form.endTime")}</Label>
                <Input
                  type="time"
                  className="mt-1 w-full sm:w-24"
                  value={form.tmpSession.end_time.slice(0,5)}
                  onChange={e=>
                    setForm(f=>({
                      ...f,
                      tmpSession:{...f.tmpSession,end_time:e.target.value + ":00"}
                    }))
                  }
                />
              </div>

              {/* Añadir sesión */}
              <div className="mt-4 sm:mt-6">
                <Button variant="outline" size="icon" onClick={addSession}>
                  <Plus className="h-4 w-4"/>
                </Button>
              </div>
            </div>

            <ul className="mt-3 space-y-1">
              {(form.sessions ?? []).map((s,i) => (
                <li
                  key={i}
                  className="flex justify-between items-center bg-gray-50 p-2 rounded"
                >
                  <span className="text-sm">
                    {t(`days.${s.day.toLowerCase()}`)} —{" "}
                    {s.start_time.slice(0,5)}–{s.end_time.slice(0,5)}
                  </span>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={()=>removeSession(i)}
                  >
                    <Trash2 className="h-4 w-4 text-red-600"/>
                  </Button>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <DialogFooter className="mt-6">
          <Button onClick={handleSave} className="w-full sm:w-auto">
            { initial ? t("classes.form.update") : t("classes.form.save") }
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
