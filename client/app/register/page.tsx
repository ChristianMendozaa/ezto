"use client"

import type React from "react"

import { useState } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { useLanguage } from "@/lib/hooks/use-language"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Checkbox } from "@/components/ui/checkbox"
import { Textarea } from "@/components/ui/textarea"
import { Calendar } from "@/components/ui/calendar"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { CalendarIcon, Dumbbell } from "lucide-react"
import { format } from "date-fns"
import { cn } from "@/lib/utils"
import { ThemeToggle } from "@/components/theme-toggle"
import { LanguageToggle } from "@/components/language-toggle"

export default function RegisterPage() {
  const { t } = useLanguage()
  const router = useRouter()
  const [userType, setUserType] = useState<"gym_owner" | "gym_member" | null>(null)
  const [date, setDate] = useState<Date>()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    const formData = new FormData()

    // Recoger los valores de los campos por ID (campos generales)
    formData.append("full_name", (document.getElementById("fullName") as HTMLInputElement)?.value || "")
    formData.append("email", (document.getElementById("email") as HTMLInputElement)?.value || "")
    formData.append("password", (document.getElementById("password") as HTMLInputElement)?.value || "")
    formData.append("confirm_password", (document.getElementById("confirmPassword") as HTMLInputElement)?.value || "")
    formData.append("phone", (document.getElementById("phone") as HTMLInputElement)?.value || "")

    // Usar el estado local `userType` para obtener el valor del tipo de usuario
    if (userType) {
      formData.append("user_type", userType)
    } else {
      console.error("Tipo de usuario no seleccionado")
      alert("Por favor selecciona el tipo de usuario (Dueño de gimnasio o Miembro de gimnasio)")
      return
    }

    // Capturar los campos de Member Info solo si el tipo de usuario es "gym_member"
    if (userType === "gym_member") {
      formData.append("gym_id", (document.getElementById("selectGym") as HTMLInputElement)?.value || "")
      formData.append("membership_number", (document.getElementById("membershipNumber") as HTMLInputElement)?.value || "")
      formData.append("gender", (document.getElementById("gender") as HTMLInputElement)?.value || "")

      // Capturar y formatear la fecha de nacimiento (birth_date)
      if (date) {
        const formattedDate = date.toISOString().split("T")[0] // Formato YYYY-MM-DD
        formData.append("birth_date", formattedDate)
      } else {
        console.warn("Fecha de nacimiento no proporcionada")
        formData.append("birth_date", "")
      }

      // Capturar los objetivos de entrenamiento y preferencias de actividades (checkboxes)
      const trainingGoals = Array.from(document.querySelectorAll('input[name="training_goals"]:checked')).map((el) => (el as HTMLInputElement).value)
      formData.append("training_goals", trainingGoals.join(",") || "")

      const activityPreferences = Array.from(document.querySelectorAll('input[name="activity_preferences"]:checked')).map((el) => (el as HTMLInputElement).value)
      formData.append("activity_preferences", activityPreferences.join(",") || "")
    }

    // Imprimir FormData para depuración
    for (const [key, value] of formData.entries()) {
      console.log(`${key}: ${value}`);
    }

    try {
      const response = await fetch("http://localhost:8000/auth/register", {
        method: "POST",
        body: formData,
        headers: {
          "Accept": "application/json",
        },
      })

      if (!response.ok) {
        const errorData = await response.json()
        console.error("Datos de error recibidos:", errorData)
        if (Array.isArray(errorData.detail)) {
          const formattedErrors = errorData.detail
            .map((err: any) => `${err.loc.join(".")}: ${err.msg}`)
            .join("\n")
          throw new Error(formattedErrors)
        }
        throw new Error(errorData.detail || "Error en el registro")
      }

      const data = await response.json()
      console.log("Usuario registrado:", data)
      router.push("/login")
    } catch (error: any) {
      console.error("Error al registrar usuario:", error.message)
      alert(error.message)
    }
  }

  return (
    <div className="min-h-screen flex flex-col bg-gray-100 dark:bg-gray-900">
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-2">
            <Dumbbell className="h-6 w-6 text-orange-500" />
            <span className="text-xl font-bold">EzTo</span>
          </div>
          <nav className="hidden md:flex gap-6">
            <Link href="/#features" className="text-sm font-medium hover:text-orange-500">
              {t("nav.features")}
            </Link>
            <Link href="/#pricing" className="text-sm font-medium hover:text-orange-500">
              {t("nav.pricing")}
            </Link>
            <Link href="/#testimonials" className="text-sm font-medium hover:text-orange-500">
              {t("nav.testimonials")}
            </Link>
            <Link href="/#blog" className="text-sm font-medium hover:text-orange-500">
              {t("nav.blog")}
            </Link>
          </nav>
          <div className="flex items-center gap-2">
            <LanguageToggle />
            <ThemeToggle />
            <Link href="/login">
              <Button variant="ghost">{t("common.signIn")}</Button>
            </Link>
          </div>
        </div>
      </header>
      <main className="flex-grow flex items-center justify-center p-4">
        <Card className="w-full max-w-4xl">
          <CardHeader>
            <CardTitle className="text-2xl font-bold">{t("auth.register.title")}</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-8">
              <div className="space-y-4">
                <h2 className="text-xl font-semibold">{t("auth.register.generalInfo")}</h2>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="fullName">{t("auth.register.fullName")}</Label>
                    <Input id="fullName" required />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="email">{t("auth.register.email")}</Label>
                    <Input id="email" type="email" required />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="password">{t("auth.register.password")}</Label>
                    <Input id="password" type="password" required />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="confirmPassword">{t("auth.register.confirmPassword")}</Label>
                    <Input id="confirmPassword" type="password" required />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="phone">{t("auth.register.phone")}</Label>
                    <Input id="phone" type="tel" required />
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                <h2 className="text-xl font-semibold">{t("auth.register.userType")}</h2>
                <RadioGroup onValueChange={(value) => setUserType(value as "gym_owner" | "gym_member")}>
                  <div className="flex items-center space-x-2">
                    <RadioGroupItem value="gym_owner" id="gym_owner" />
                    <Label htmlFor="gym_owner">{t("auth.register.gymOwner")}</Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <RadioGroupItem value="gym_member" id="gym_member" />
                    <Label htmlFor="gym_member">{t("auth.register.gymMember")}</Label>
                  </div>
                </RadioGroup>
              </div>

              {userType === "gym_owner" && (
                <div className="space-y-4">
                  <h2 className="text-xl font-semibold">{t("auth.register.gymInfo")}</h2>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="gymName">{t("auth.register.gymName")}</Label>
                      <Input id="gymName" required />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="gymAddress">{t("auth.register.gymAddress")}</Label>
                      <Input id="gymAddress" required />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="gymPhone">{t("auth.register.gymPhone")}</Label>
                      <Input id="gymPhone" type="tel" required />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="gymHours">{t("auth.register.gymHours")}</Label>
                      <Input id="gymHours" required />
                    </div>
                    <div className="space-y-2 col-span-2">
                      <Label>{t("auth.register.gymServices")}</Label>
                      <div className="grid grid-cols-2 gap-2">
                        {["weights", "cardio", "groupClasses", "personalTraining"].map((service) => (
                          <div key={service} className="flex items-center space-x-2">
                            <Checkbox id={service} />
                            <Label htmlFor={service}>{t(`auth.register.services.${service}`)}</Label>
                          </div>
                        ))}
                      </div>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="gymCapacity">{t("auth.register.gymCapacity")}</Label>
                      <Input id="gymCapacity" type="number" required />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="gymLogo">{t("auth.register.gymLogo")}</Label>
                      <Input id="gymLogo" type="file" accept="image/*" />
                    </div>
                    <div className="space-y-2 col-span-2">
                      <Label htmlFor="gymSocial">{t("auth.register.gymSocial")}</Label>
                      <Textarea id="gymSocial" placeholder={t("auth.register.gymSocialPlaceholder")} />
                    </div>
                  </div>
                </div>
              )}

              {userType === "gym_member" && (
                <div className="space-y-4">
                  <h2 className="text-xl font-semibold">{t("auth.register.memberInfo")}</h2>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="selectGym">{t("auth.register.selectGym")}</Label>
                      <Select>
                        <SelectTrigger id="selectGym">
                          <SelectValue placeholder={t("auth.register.selectGymPlaceholder")} />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="gym1">Gym 1</SelectItem>
                          <SelectItem value="gym2">Gym 2</SelectItem>
                          <SelectItem value="gym3">Gym 3</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="membershipNumber">{t("auth.register.membershipNumber")}</Label>
                      <Input id="membershipNumber" />
                    </div>
                    <div className="space-y-2">
                      <Label>{t("auth.register.dateOfBirth")}</Label>
                      <Popover>
                        <PopoverTrigger asChild>
                          <Button
                            variant={"outline"}
                            className={cn(
                              "w-full justify-start text-left font-normal",
                              !date && "text-muted-foreground",
                            )}
                          >
                            <CalendarIcon className="mr-2 h-4 w-4" />
                            {date ? format(date, "PPP") : <span>{t("auth.register.pickADate")}</span>}
                          </Button>
                        </PopoverTrigger>
                        <PopoverContent className="w-auto p-0">
                          <Calendar mode="single" selected={date} onSelect={setDate} initialFocus />
                        </PopoverContent>
                      </Popover>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="gender">{t("auth.register.gender")}</Label>
                      <Select>
                        <SelectTrigger id="gender">
                          <SelectValue placeholder={t("auth.register.selectGender")} />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="male">{t("auth.register.genderMale")}</SelectItem>
                          <SelectItem value="female">{t("auth.register.genderFemale")}</SelectItem>
                          <SelectItem value="other">{t("auth.register.genderOther")}</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    <div className="space-y-2 col-span-2">
                      <Label>{t("auth.register.trainingGoals")}</Label>
                      <div className="grid grid-cols-2 gap-2">
                        {["loseWeight", "gainMuscle", "improveHealth"].map((goal) => (
                          <div key={goal} className="flex items-center space-x-2">
                            <Checkbox id={goal} />
                            <Label htmlFor={goal}>{t(`auth.register.goals.${goal}`)}</Label>
                          </div>
                        ))}
                      </div>
                    </div>
                    <div className="space-y-2 col-span-2">
                      <Label>{t("auth.register.activityPreferences")}</Label>
                      <div className="grid grid-cols-2 gap-2">
                        {["groupClasses", "weights", "cardio", "yoga"].map((activity) => (
                          <div key={activity} className="flex items-center space-x-2">
                            <Checkbox id={activity} />
                            <Label htmlFor={activity}>{t(`auth.register.activities.${activity}`)}</Label>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              )}

              <Button type="submit" className="w-full">
                {t("auth.register.registerButton")}
              </Button>
            </form>
          </CardContent>
          <CardFooter className="flex justify-center">
            <p className="text-sm text-muted-foreground">
              {t("auth.register.haveAccount")}{" "}
              <Link href="/login" className="text-primary hover:underline">
                {t("auth.register.login")}
              </Link>
            </p>
          </CardFooter>
        </Card>
      </main>
    </div>
  )
}

