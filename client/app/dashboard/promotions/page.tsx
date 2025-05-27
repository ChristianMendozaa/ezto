"use client";

import { useState } from "react";
import { useLanguage } from "@/lib/hooks/use-language";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
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
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { usePromotions, PromotionInput, Promotion } from "@/hooks/usePromotions";

export default function PromotionsPage() {
  const { t } = useLanguage();
  const {
    promotions,
    loading,
    error,
    createPromotion,
    deletePromotion,
  } = usePromotions();

  // filtro: all | active | inactive
  const [filter, setFilter] = useState<"all" | "active" | "inactive">("all");
  const [isDialogOpen, setIsDialogOpen] = useState(false);

  // estados del formulario
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [discountType, setDiscountType] = useState<"percentage" | "fixed" | "free_month">("percentage");
  const [discountValue, setDiscountValue] = useState<number>(0);
  const [promoCode, setPromoCode] = useState("");
  const [autoApply, setAutoApply] = useState(false);
  const [applicableTo, setApplicableTo] = useState<"all_users"|"new_users"|"loyal_users"|"specific_plan">("all_users");
  const [status, setStatus] = useState<boolean>(true);

  const filtered = promotions.filter((p: Promotion) => {
    if (filter === "all") return true;
    return filter === "active" ? p.status === true : p.status === false;
  });

  const resetForm = () => {
    setName("");
    setDescription("");
    setStartDate("");
    setEndDate("");
    setDiscountType("percentage");
    setDiscountValue(0);
    setPromoCode("");
    setAutoApply(false);
    setApplicableTo("all_users");
    setStatus(true);
  };

  const handleCreatePromotion = async () => {
    const data: PromotionInput = {
      name,
      description,
      start_date: startDate,
      end_date: endDate,
      discount_type: discountType,
      discount_value: discountValue,
      promo_code: promoCode || undefined,
      auto_apply: autoApply,
      applicable_to: applicableTo,
      status,
    };

    const ok = await createPromotion(data);
    if (ok) {
      setIsDialogOpen(false);
      resetForm();
    }
  };

  return (
    <div className="flex-1 space-y-4 p-8 pt-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold">{t("promotions.title")}</h2>
        <div className="flex space-x-2">
          <Select
            value={filter}
            onValueChange={(v) => setFilter(v as any)}
          >
            <SelectTrigger className="w-32">
              <SelectValue placeholder={t("promotions.filter")} />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">{t("promotions.filterAll")}</SelectItem>
              <SelectItem value="active">{t("promotions.filterActive")}</SelectItem>
              <SelectItem value="inactive">{t("promotions.filterInactive")}</SelectItem>
            </SelectContent>
          </Select>
          <Button onClick={() => setIsDialogOpen(true)}>
            <Plus className="mr-2 h-4 w-4" />
            {t("promotions.add")}
          </Button>
        </div>
      </div>

      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="sm:max-w-[30vw] max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>{t("promotions.addPromotion")}</DialogTitle>
            <DialogDescription>{t("promotions.addPromotionDescription")}</DialogDescription>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <Label>{t("promotions.form.name")}</Label>
            <Input value={name} onChange={(e) => setName(e.target.value)} />

            <Label>{t("promotions.form.description")}</Label>
            <Textarea value={description} onChange={(e) => setDescription(e.target.value)} />

            <Label>{t("promotions.form.startDate")}</Label>
            <Input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />

            <Label>{t("promotions.form.endDate")}</Label>
            <Input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} />

            <Label>{t("promotions.form.discountType")}</Label>
            <Select value={discountType} onValueChange={(v) => setDiscountType(v as any)}>
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
            <Input
              type="number"
              value={discountValue}
              onChange={(e) => setDiscountValue(Number(e.target.value))}
            />

            <Label>{t("promotions.form.promoCode")}</Label>
            <Input value={promoCode} onChange={(e) => setPromoCode(e.target.value)} />

            <Label>{t("promotions.form.autoApply")}</Label>
            <Select
              value={autoApply.toString()}
              onValueChange={(v) => setAutoApply(v === "true")}
            >
              <SelectTrigger>
                <SelectValue placeholder={t("promotions.form.select")} />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="true">{t("promotions.autoApply.yes")}</SelectItem>
                <SelectItem value="false">{t("promotions.autoApply.no")}</SelectItem>
              </SelectContent>
            </Select>

            <Label>{t("promotions.form.applicableTo")}</Label>
            <Select value={applicableTo} onValueChange={(v) => setApplicableTo(v as any)}>
              <SelectTrigger>
                <SelectValue placeholder={t("promotions.form.select")} />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all_users">{t("promotions.applicableTo.allUsers")}</SelectItem>
                <SelectItem value="new_users">{t("promotions.applicableTo.newUsers")}</SelectItem>
                <SelectItem value="loyal_users">{t("promotions.applicableTo.loyalUsers")}</SelectItem>
                <SelectItem value="specific_plan">{t("promotions.applicableTo.specificPlan")}</SelectItem>
              </SelectContent>
            </Select>

            <Label>{t("promotions.form.status")}</Label>
            <Select
              value={status ? "true" : "false"}
              onValueChange={(v) => setStatus(v === "true")}
            >
              <SelectTrigger>
                <SelectValue placeholder={t("promotions.form.select")} />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="true">{t("promotions.status.active")}</SelectItem>
                <SelectItem value="false">{t("promotions.status.inactive")}</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <DialogFooter>
            <Button onClick={handleCreatePromotion}>
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
                      {p.auto_apply ? (
                        <Badge>Yes</Badge>
                      ) : (
                        <Badge variant="outline">No</Badge>
                      )}
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
                          <DropdownMenuItem>
                            <Edit className="mr-2 h-4 w-4" />
                            {t("promotions.actions.edit")}
                          </DropdownMenuItem>
                          <DropdownMenuItem
                            onClick={() => deletePromotion(p.id)}
                          >
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
