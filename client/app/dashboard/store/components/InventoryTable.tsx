"use client";

import React from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { useLanguage } from "@/lib/hooks/use-language";
import { InventoryMovement } from "../hooks/useInventory";

interface InventoryTableProps {
  movements: InventoryMovement[];
}

export const InventoryTable: React.FC<InventoryTableProps> = ({ movements }) => {
  const { t } = useLanguage();

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>#{t('store.inventory.table.productId')}</TableHead>
          <TableHead>{t('store.inventory.table.type')}</TableHead>
          <TableHead>{t('store.inventory.table.qty')}</TableHead>
          <TableHead>{t('store.inventory.table.reason')}</TableHead>
          <TableHead>{t('store.inventory.table.reference')}</TableHead>
          <TableHead>{t('store.inventory.table.date')}</TableHead>
          <TableHead>{t('store.inventory.table.responsible')}</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {movements.map(mv => (
          <TableRow key={mv.id}>
            <TableCell>{mv.product_id}</TableCell>
            <TableCell>{t(`store.inventory.movement.${mv.movement_type}`)}</TableCell>
            <TableCell>{mv.quantity}</TableCell>
            <TableCell>{mv.reason}</TableCell>
            <TableCell>{mv.reference_id}</TableCell>
            <TableCell>{new Date(mv.movement_date).toLocaleString()}</TableCell>
            <TableCell>{mv.responsible_id}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};
