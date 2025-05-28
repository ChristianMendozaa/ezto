// components/PurchaseTable.tsx
"use client";

import React from "react";
import {
  Table,
  TableHeader,
  TableHead,
  TableRow,
  TableBody,
  TableCell,
} from "@/components/ui/table";
import { useLanguage } from "@/lib/hooks/use-language";
import { Purchase } from "../hooks/usePurchases";

interface PurchaseTableProps {
  purchases: Purchase[];
}

export const PurchaseTable: React.FC<PurchaseTableProps> = ({ purchases }) => {
  const { t } = useLanguage();

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>{t('store.purchases.table.invoice')}</TableHead>
          <TableHead>{t('store.purchases.table.clientId')}</TableHead>
          <TableHead>{t('store.purchases.table.date')}</TableHead>
          <TableHead>{t('store.purchases.table.total')}</TableHead>
          <TableHead>{t('store.purchases.table.status')}</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {purchases.map(p => (
          <TableRow key={p.sale_id}>
            <TableCell>{p.invoice_number}</TableCell>
            <TableCell>{p.client_id}</TableCell>
            <TableCell>{new Date(p.sale_date).toLocaleString()}</TableCell>
            <TableCell>${p.total_amount.toFixed(2)}</TableCell>
            <TableCell>{p.status}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};
