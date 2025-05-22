"use client"

import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis } from "recharts"

const data = [
  {
    name: "Lun",
    total: 145,
  },
  {
    name: "Mar",
    total: 168,
  },
  {
    name: "Mie",
    total: 182,
  },
  {
    name: "Jue",
    total: 156,
  },
  {
    name: "Vie",
    total: 192,
  },
  {
    name: "Sab",
    total: 134,
  },
  {
    name: "Dom",
    total: 89,
  },
]

export function Overview() {
  return (
    <ResponsiveContainer width="100%" height={350}>
      <BarChart data={data}>
        <XAxis dataKey="name" stroke="#888888" fontSize={12} tickLine={false} axisLine={false} />
        <YAxis stroke="#888888" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(value) => `${value}`} />
        <Bar dataKey="total" fill="#F97316" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  )
}

