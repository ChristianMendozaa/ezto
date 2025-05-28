"use client";

import React from "react";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";
import { Button } from "@/components/ui/button";
import { Edit, MoreHorizontal, Package, Trash2 } from "lucide-react";
import { useLanguage } from "@/lib/hooks/use-language";
import { Product } from "../hooks/useProducts";

interface ProductTableProps {
  products: Product[];
  onEdit: (product: Product) => void;
  onDelete: (productId: string) => void;
}

export const ProductTable: React.FC<ProductTableProps> = ({ products, onEdit, onDelete }) => {
  const { t } = useLanguage();

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>{t("store.catalog.table.name")}</TableHead>
          <TableHead>{t("store.catalog.table.category")}</TableHead>
          <TableHead>{t("store.catalog.table.price")}</TableHead>
          <TableHead>{t("store.catalog.table.stock")}</TableHead>
          <TableHead className="text-right">{t("store.catalog.table.actions")}</TableHead>
          <TableHead>{/* Imagen */}</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {products.map(product => (
          <TableRow key={product.id}>
            <TableCell className="font-medium">{product.name}</TableCell>
            <TableCell>{product.category}</TableCell>
            <TableCell>${Number(product.sale_price).toFixed(2)}</TableCell>
            <TableCell>{product.current_stock}</TableCell>
            <TableCell className="text-right">
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" className="h-8 w-8 p-0">
                    <span className="sr-only">{t("store.catalog.actions.open")}</span>
                    <MoreHorizontal className="h-4 w-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <DropdownMenuLabel>{t("store.catalog.actions.title")}</DropdownMenuLabel>
                  <DropdownMenuItem onClick={() => onEdit(product)}>
                    <Edit className="mr-2 h-4 w-4" />
                    {t("store.catalog.actions.edit")}
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => onDelete(product.id)}>
                    <Trash2 className="mr-2 h-4 w-4" />
                    {t("store.catalog.actions.delete")}
                  </DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem>
                    <Package className="mr-2 h-4 w-4" />
                    {t("store.catalog.actions.updateStock")}
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </TableCell>
            <TableCell>
              {product.image_base64 && (
                <img
                  src={`data:image/webp;base64,${product.image_base64}`}
                  alt={product.name}
                  className="h-10 w-10 object-cover"
                />
              )}
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};
