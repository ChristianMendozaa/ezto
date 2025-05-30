import { useEffect, useState } from "react"
import { onSnapshot, doc } from "firebase/firestore"
import { db } from "@/lib/firebaseConfig"

export interface AccessData {
  id: string
  name: string
  entrada: string
  email?: string
  plan?: string
  end_date?: string
  salida?: string
  tiempo_total?: string
}

export interface DashboardStats {
  activeMembers: number
  dailyActivity: number
  monthlyRevenue: number
}

export interface OverviewData {
  name: string
  total: number
}

export function useDashboardData() {
  const [accesses, setAccesses] = useState<AccessData[]>([])
  const [stats, setStats] = useState<DashboardStats>({ activeMembers: 0, dailyActivity: 0, monthlyRevenue: 0 })
  const [overview, setOverview] = useState<OverviewData[]>([])

  useEffect(() => {
    const unsubscribe = onSnapshot(doc(db, "dashboard", "registro_general"), (docSnap) => {
      const data = docSnap.data()
      const accesos = data?.accesos || {}
      const stats = data?.stats || {}
      const activityPerDay = data?.activity_per_day || {}
      const monthlyRevenueData = data?.monthly_revenue || {}

      // Obtener el mes actual (ej: "2025-05")
      const currentMonth = new Date().toISOString().slice(0, 7)
      const revenueThisMonth = monthlyRevenueData[currentMonth] || 0

      // Ordenar las fechas en el eje X por día cronológico (formato: YYYY-MM-DD)
      const overviewArray: OverviewData[] = Object.entries(activityPerDay)
        .map(([key, value]) => ({
          name: key, // formato ya es YYYY-MM-DD
          total: value as number
        }))
        .sort((a, b) => {
          const dateA = new Date(a.name).getTime()
          const dateB = new Date(b.name).getTime()
          return dateA - dateB
        })

      const accessList = Object.entries(accesos).map(([timestamp, value]: [string, any]) => ({
        id: timestamp,
        name: value?.name || "Desconocido",
        entrada: value?.entrada || "",
        email: value?.email,
        plan: value?.plan,
        end_date: value?.end_date,
        salida: value?.salida,
        tiempo_total: value?.tiempo_total
      }))

      accessList.sort((a, b) => {
        const timeA = new Date(a.entrada).getTime()
        const timeB = new Date(b.entrada).getTime()
        return timeB - timeA
      })

      setAccesses(accessList)
      setStats({
        activeMembers: stats.activeMembers || 0,
        dailyActivity: stats.dailyActivity || 0,
        monthlyRevenue: revenueThisMonth
      })
      setOverview(overviewArray)
    })

    return () => unsubscribe()
  }, [])

  return { accesses, stats, overview }
}
