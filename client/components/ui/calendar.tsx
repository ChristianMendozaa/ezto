"use client"

import React from "react"
import DatePicker, { registerLocale } from "react-datepicker"
import { es } from "date-fns/locale"
import { CalendarIcon } from "lucide-react"
import "react-datepicker/dist/react-datepicker.css"
registerLocale("es", es)

interface Props {
  selected: Date | null
  onChange: (date: Date | null) => void
  placeholder?: string
}

export const DatePickerInput = ({ selected, onChange, placeholder }: Props) => {
  return (
    <div className="relative w-full">
      <DatePicker
        selected={selected}
        onChange={onChange}
        locale="es"
        dateFormat="dd/MM/yyyy"
        showMonthDropdown
        showYearDropdown
        dropdownMode="select"
        placeholderText={placeholder || "Selecciona una fecha"}
        className="w-full border rounded-md px-3 py-2 text-sm focus:outline-none dark:bg-background dark:text-white"
      />
      <CalendarIcon className="absolute right-3 top-2.5 h-4 w-4 text-gray-500 pointer-events-none" />
    </div>
  )
}
