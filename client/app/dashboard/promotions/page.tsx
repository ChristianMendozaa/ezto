"use client";

import { useState } from "react";
import { useLanguage } from "@/lib/hooks/use-language";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Search, Plus, MoreHorizontal, Edit, Trash2, Calendar } from "lucide-react";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { usePromotions } from "@/hooks/usePromotions";

export default function PromotionsPage() {
  const { t } = useLanguage();
  const [filter, setFilter] = useState("all");
  const [isAddPromotionOpen, setIsAddPromotionOpen] = useState(false);
  const { promotions, loading, error, createPromotion, deletePromotion } = usePromotions();

  const filteredPromotions = promotions.filter((promotion) => {
    if (filter === "all") return true;
    return promotion.status === filter;
  });

  return (
    <div className="flex-1 space-y-4 p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">{t("promotions.title")}</h2>
        <Button onClick={() => setIsAddPromotionOpen(true)}>
          <Plus className="mr-2 h-4 w-4" />
          {t("promotions.add")}
        </Button>
      </div>

      <Dialog open={isAddPromotionOpen} onOpenChange={setIsAddPromotionOpen}>
        <DialogContent className="sm:max-w-[30vw] max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>{t("promotions.addPromotion")}</DialogTitle>
            <DialogDescription>{t("promotions.addPromotionDescription")}</DialogDescription>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <Label>{t("promotions.form.name")}</Label>
            <Input id="name" />

            <Label>{t("promotions.form.description")}</Label>
            <Textarea id="description" />

            <Label>{t("promotions.form.startDate")}</Label>
            <Input id="startDate" type="date" />

            <Label>{t("promotions.form.endDate")}</Label>
            <Input id="endDate" type="date" />

            <Label>{t("promotions.form.discountType")}</Label>
            <Select>
              <SelectTrigger>
                <SelectValue placeholder={t("promotions.form.select")} />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="percentage">{t("promotions.discountType.percentage")}</SelectItem>
                <SelectItem value="fixed">{t("promotions.discountType.fixed")}</SelectItem>
                <SelectItem value="free_month">{t("promotions.discountType.freeMonth")}</SelectItem>
              </SelectContent>
            </Select>

            <Label>{t("promotions.form.discountValue")}</Label>
            <Input id="discountValue" type="number" />

            <Label>{t("promotions.form.promoCode")}</Label>
            <Input id="promoCode" />

            <Label>{t("promotions.form.autoApply")}</Label>
            <Select>
              <SelectTrigger>
                <SelectValue placeholder={t("promotions.form.select")} />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="true">{t("promotions.autoApply.yes")}</SelectItem>
                <SelectItem value="false">{t("promotions.autoApply.no")}</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <DialogFooter>
            <Button type="submit" onClick={() => setIsAddPromotionOpen(false)}>
              {t("promotions.form.save")}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <Card>
        <CardHeader>
          <CardTitle>{t("promotions.title")}</CardTitle>
        </CardHeader>
        <CardContent>
          {loading ? (
            <p>Cargando promociones...</p>
          ) : error ? (
            <p className="text-red-500">{error}</p>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>{t("promotions.table.name")}</TableHead>
                  <TableHead>{t("promotions.table.discountType")}</TableHead>
                  <TableHead>{t("promotions.table.discountValue")}</TableHead>
                  <TableHead>{t("promotions.table.startDate")}</TableHead>
                  <TableHead>{t("promotions.table.endDate")}</TableHead>
                  <TableHead>{t("promotions.table.autoApply")}</TableHead>
                  <TableHead>{t("promotions.table.promoCode")}</TableHead>
                  <TableHead>{t("promotions.table.actions")}</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredPromotions.map((promotion) => (
                  <TableRow key={promotion.id}>
                    <TableCell>{promotion.name}</TableCell>
                    <TableCell>{promotion.discount_type}</TableCell>
                    <TableCell>{promotion.discount_value}</TableCell>
                    <TableCell>{promotion.start_date}</TableCell>
                    <TableCell>{promotion.end_date}</TableCell>
                    <TableCell>{promotion.auto_apply ? "Yes" : "No"}</TableCell>
                    <TableCell>{promotion.promo_code || "N/A"}</TableCell>
                    <TableCell>
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant="ghost" className="h-8 w-8 p-0">
                            <span className="sr-only">{t("promotions.actions.open")}</span>
                            <MoreHorizontal className="h-4 w-4" />
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                          <DropdownMenuLabel>{t("promotions.actions.title")}</DropdownMenuLabel>
                          <DropdownMenuItem>
                            <Edit className="mr-2 h-4 w-4" />
                            {t("promotions.actions.edit")}
                          </DropdownMenuItem>
                          <DropdownMenuItem onClick={() => deletePromotion(promotion.id)}>
                            <Trash2 className="mr-2 h-4 w-4 text-red-500" />
                            {t("promotions.actions.delete")}
                          </DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
