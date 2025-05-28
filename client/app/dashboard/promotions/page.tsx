"use client";

import React, { useState } from "react";
import { useLanguage } from "@/lib/hooks/use-language";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Search, Plus, MoreHorizontal, Edit, Trash2 } from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { usePromotions, Promotion, PromotionInput } from "@/hooks/usePromotions";
import { PromotionFormDialog } from "./PromotionFormDialog";

export default function PromotionsPage() {
  const { t } = useLanguage();
  const {
    promotions,
    loading,
    error,
    createPromotion,
    updatePromotion,
    deletePromotion,
  } = usePromotions();

  const [filter, setFilter] = useState<"all" | "active" | "inactive">("all");
  const [dialogOpen, setDialogOpen] = useState(false);
  const [selectedPromo, setSelectedPromo] = useState<Promotion | undefined>(undefined);

  const handleAdd = () => {
    setSelectedPromo(undefined);
    setDialogOpen(true);
  };

  const handleEdit = (p: Promotion) => {
    setSelectedPromo(p);
    setDialogOpen(true);
  };

  const onSave = async (data: PromotionInput) => {
    if (selectedPromo) {
      return await updatePromotion(selectedPromo.id, data);
    }
    return await createPromotion(data);
  };

  const filtered = promotions.filter((p) => {
    if (filter === "all") return true;
    return filter === "active" ? p.status === true : p.status === false;
  });

  return (
    <div className="flex-1 space-y-4 p-8 pt-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold">{t("promotions.title")}</h2>
        <div className="flex space-x-2">
          <Select value={filter} onValueChange={(v) => setFilter(v as any)}>
            <SelectTrigger className="w-32">
              <SelectValue placeholder={t("promotions.filter")} />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">{t("promotions.filterAll")}</SelectItem>
              <SelectItem value="active">{t("promotions.filterActive")}</SelectItem>
              <SelectItem value="inactive">{t("promotions.filterInactive")}</SelectItem>
            </SelectContent>
          </Select>
          <Button onClick={handleAdd}>
            <Plus className="mr-2 h-4 w-4" />
            {t("promotions.add")}
          </Button>
        </div>
      </div>

      <PromotionFormDialog
        open={dialogOpen}
        onOpenChange={setDialogOpen}
        initialData={selectedPromo}
        onSave={onSave}
        title={
          selectedPromo
            ? t("promotions.editPromotion")
            : t("promotions.addPromotion")
        }
        description={t(
          `promotions.${selectedPromo ? "editPromotionDescription" : "addPromotionDescription"}`
        )}
      />

      <Card>
        <CardHeader>
          <CardTitle>{t("promotions.title")}</CardTitle>
        </CardHeader>
        <CardContent>
          {loading ? (
            <p>{t("promotions.loading")}</p>
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
                  <TableHead>{t("promotions.table.applicableTo")}</TableHead>
                  <TableHead>{t("promotions.table.autoApply")}</TableHead>
                  <TableHead>{t("promotions.table.promoCode")}</TableHead>
                  <TableHead>{t("promotions.table.status")}</TableHead>
                  <TableHead>{t("promotions.table.actions")}</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filtered.map((p) => (
                  <TableRow key={p.id}>
                    <TableCell>{p.name}</TableCell>
                    <TableCell>{p.discount_type}</TableCell>
                    <TableCell>{p.discount_value}</TableCell>
                    <TableCell>{p.start_date}</TableCell>
                    <TableCell>{p.end_date}</TableCell>
                    <TableCell>{p.applicable_to}</TableCell>
                    <TableCell>
                      {p.auto_apply ? <Badge>Yes</Badge> : <Badge variant="outline">No</Badge>}
                    </TableCell>
                    <TableCell>{p.promo_code ?? "N/A"}</TableCell>
                    <TableCell>
                      {p.status ? (
                        <Badge>Active</Badge>
                      ) : (
                        <Badge variant="outline">Inactive</Badge>
                      )}
                    </TableCell>
                    <TableCell>
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant="ghost" className="h-8 w-8 p-0">
                            <span className="sr-only">
                              {t("promotions.actions.open")}
                            </span>
                            <MoreHorizontal className="h-4 w-4" />
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                          <DropdownMenuLabel>
                            {t("promotions.actions.title")}
                          </DropdownMenuLabel>
                          <DropdownMenuItem onClick={() => handleEdit(p)}>
                            <Edit className="mr-2 h-4 w-4" />
                            {t("promotions.actions.edit")}
                          </DropdownMenuItem>
                          <DropdownMenuItem onClick={() => deletePromotion(p.id)}>
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
