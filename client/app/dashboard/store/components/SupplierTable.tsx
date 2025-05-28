// components/SupplierTable.tsx
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
import { Supplier } from "../hooks/useSuppliers";

interface SupplierTableProps {
  suppliers: Supplier[];
}

export const SupplierTable: React.FC<SupplierTableProps> = ({ suppliers }) => {
  const { t } = useLanguage();

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>{t('store.suppliers.table.name')}</TableHead>
          <TableHead>{t('store.suppliers.table.email')}</TableHead>
          <TableHead>{t('store.suppliers.table.phone')}</TableHead>
          <TableHead>{t('store.suppliers.table.address')}</TableHead>
          <TableHead>{t('store.suppliers.table.status')}</TableHead>
          <TableHead>{t('store.suppliers.table.productsOffered')}</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {suppliers.map(s => (
          <TableRow key={s.id}>
            <TableCell>{s.name}</TableCell>
            <TableCell>{s.contact_email}</TableCell>
            <TableCell>{s.phone}</TableCell>
            <TableCell>{s.address}</TableCell>
            <TableCell>{s.status}</TableCell>
            <TableCell>{s.products_offered}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};
