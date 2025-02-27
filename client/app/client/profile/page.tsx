"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { useLanguage } from "@/lib/hooks/use-language"

export default function ClientProfile() {
  const { t } = useLanguage()

  return (
    <div className="space-y-4">
      <h1 className="text-3xl font-bold">{t("client.profile.title")}</h1>
      <Card>
        <CardHeader>
          <CardTitle>{t("client.profile.personalInfo")}</CardTitle>
        </CardHeader>
        <CardContent>
          <form className="space-y-4">
            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="firstName">{t("client.profile.firstName")}</Label>
                <Input id="firstName" defaultValue="John" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="lastName">{t("client.profile.lastName")}</Label>
                <Input id="lastName" defaultValue="Doe" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="email">{t("client.profile.email")}</Label>
                <Input id="email" type="email" defaultValue="john.doe@example.com" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="phone">{t("client.profile.phone")}</Label>
                <Input id="phone" type="tel" defaultValue="+1234567890" />
              </div>
            </div>
            <Button type="submit">{t("common.save")}</Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}

