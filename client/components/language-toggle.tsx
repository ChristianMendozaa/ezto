"use client"

import { Button } from "@/components/ui/button"
import { useLanguage } from "@/lib/hooks/use-language"

export function LanguageToggle() {
  const { language, setLanguage } = useLanguage()

  const toggleLanguage = () => {
    setLanguage(language === "es" ? "en" : "es")
  }

  return (
    <Button variant="ghost" size="sm" onClick={toggleLanguage} className="w-16">
      {language.toUpperCase()}
    </Button>
  )
}

