"use client";

import React, { useEffect, useState, ChangeEvent, FormEvent } from "react";
import { useLanguage } from "@/lib/hooks/use-language";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
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
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
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
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Textarea } from "@/components/ui/textarea";
import {
  Search,
  Plus,
  MoreHorizontal,
  Edit,
  Trash2,
  Package,
  History,
  ShoppingCart,
} from "lucide-react";

// URL base de tu API
const API_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

// Tipos de datos de producto (puedes ajustarlos según tu modelo backend)
type Product = {
  id: string;
  name: string;
  sku: string;
  category: string;
  description?: string;
  purchase_price: number;
  sale_price: number;
  current_stock: number;
  min_stock: number;
  expiration_date?: string;
  supplier_id: string;
  barcode?: string;
  status: string;
  image_base64?: string;
  created_at: string;
  last_updated: string;
  profit_margin: number;
};

// Tipos de datos para compras y movimientos (similarmente se pueden definir)
type Purchase = {
  sale_id: string;
  client_id: string;
  total_amount: number;
  sale_date: string;
  // Otros campos que devuelva tu endpoint
};

type InventoryMovement = {
  movement_id: string;
  product_id: string;
  movement_type: string;
  quantity: number;
  reason: string;
  reference_id: string;
  movement_date: string;
  responsible_id: string;
};

export default function StorePage() {
  const { t } = useLanguage();
  const [activeTab, setActiveTab] = useState("catalog");
  const [isAddProductOpen, setIsAddProductOpen] = useState(false);
  const [products, setProducts] = useState<Product[]>([]);
  const [purchases, setPurchases] = useState<Purchase[]>([]);
  const [inventory, setInventory] = useState<InventoryMovement[]>([]);
  const [loading, setLoading] = useState(false);

  // Campos para crear un nuevo producto
  const [newProduct, setNewProduct] = useState({
    name: "",
    sku: "",
    category: "",
    purchase_price: "",
    sale_price: "",
    current_stock: "",
    min_stock: "",
    supplier_id: "",
    description: "",
    expiration_date: "",
    barcode: "",
    status: "activo",
  });
  const [productImage, setProductImage] = useState<File | null>(null);

  // Token obtenido del login, debe estar almacenado (por ejemplo, en localStorage o en cookies)
  const token = typeof window !== "undefined" ? localStorage.getItem("authToken") : null;

  // Función para obtener productos desde el backend
  const fetchProducts = async () => {
    try {
      const res = await fetch(`${API_URL}/products`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        credentials: "include",
      });
      if (res.ok) {
        const data = await res.json();
        setProducts(data);
      }
    } catch (error) {
      console.error("Error fetching products", error);
    }
  };

  // Funciones similares para purchases e inventory si tienes endpoints
  const fetchPurchases = async () => {
    try {
      const res = await fetch(`${API_URL}/purchases`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        credentials: "include",
      });
      if (res.ok) {
        const data = await res.json();
        setPurchases(data);
      }
    } catch (error) {
      console.error("Error fetching purchases", error);
    }
  };

  const fetchInventory = async () => {
    try {
      const res = await fetch(`${API_URL}/inventory`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        credentials: "include",
      });
      if (res.ok) {
        const data = await res.json();
        setInventory(data);
      }
    } catch (error) {
      console.error("Error fetching inventory", error);
    }
  };

  useEffect(() => {
    if (token) {
      fetchProducts();
      fetchPurchases();
      fetchInventory();
    }
  }, [token]);

  // Manejo de cambios en campos de producto
  const handleInputChange = (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { id, value } = e.target;
    setNewProduct((prev) => ({ ...prev, [id]: value }));
  };

  const handleImageChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setProductImage(e.target.files[0]);
    }
  };

  // Función para agregar un nuevo producto
  const handleAddProduct = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      // Usamos FormData para enviar datos y el archivo (imagen)
      const formData = new FormData();
      Object.entries(newProduct).forEach(([key, value]) => {
        formData.append(key, value);
      });
      if (productImage) {
        formData.append("product_image", productImage);
      }

      const res = await fetch(`${API_URL}/products`, {
        method: "POST",
        headers: {
          // Nota: No incluir "Content-Type" para FormData
          Authorization: `Bearer ${token}`,
        },
        credentials: "include",
        body: formData,
      });

      if (res.ok) {
        await fetchProducts();
        setIsAddProductOpen(false);
        setNewProduct({
          name: "",
          sku: "",
          category: "",
          purchase_price: "",
          sale_price: "",
          current_stock: "",
          min_stock: "",
          supplier_id: "",
          description: "",
          expiration_date: "",
          barcode: "",
          status: "activo",
        });
        setProductImage(null);
      } else {
        console.error("Error al agregar producto", await res.text());
      }
    } catch (error) {
      console.error("Error al agregar producto", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-1 space-y-4 p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">{t("store.title")}</h2>
      </div>
      <Tabs defaultValue="catalog" className="space-y-4">
        <TabsList>
          <TabsTrigger value="catalog" onClick={() => setActiveTab("catalog")}>
            {t("store.tabs.catalog")}
          </TabsTrigger>
          <TabsTrigger value="purchases" onClick={() => setActiveTab("purchases")}>
            {t("store.tabs.purchases")}
          </TabsTrigger>
          <TabsTrigger value="inventory" onClick={() => setActiveTab("inventory")}>
            {t("store.tabs.inventory")}
          </TabsTrigger>
        </TabsList>
        {/* Catalogo de productos */}
        <TabsContent value="catalog" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>{t("store.catalog.title")}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex justify-between mb-4">
                <div className="flex w-full max-w-sm items-center space-x-2">
                  <Input placeholder={t("store.search")} className="w-[300px]" />
                  <Button type="submit" size="icon">
                    <Search className="h-4 w-4" />
                  </Button>
                </div>
                <Dialog open={isAddProductOpen} onOpenChange={setIsAddProductOpen}>
                  <DialogTrigger asChild>
                    <Button>
                      <Plus className="mr-2 h-4 w-4" />
                      {t("store.catalog.addProduct")}
                    </Button>
                  </DialogTrigger>
                  <DialogContent className="sm:max-w-[425px]">
                    <DialogHeader>
                      <DialogTitle>{t("store.catalog.addProductTitle")}</DialogTitle>
                      <DialogDescription>
                        {t("store.catalog.addProductDescription")}
                      </DialogDescription>
                    </DialogHeader>
                    <form onSubmit={handleAddProduct}>
                      <div className="grid gap-4 py-4">
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="name" className="text-right">
                            {t("store.catalog.form.name")}
                          </Label>
                          <Input id="name" value={newProduct.name} onChange={handleInputChange} className="col-span-3" required />
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="sku" className="text-right">
                            SKU
                          </Label>
                          <Input id="sku" value={newProduct.sku} onChange={handleInputChange} className="col-span-3" required />
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="category" className="text-right">
                            {t("store.catalog.form.category")}
                          </Label>
                          <Select>
                            <SelectTrigger id="category" className="col-span-3">
                              <SelectValue placeholder={t("store.catalog.form.selectCategory")} />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="supplements">
                                {t("store.catalog.categories.supplements")}
                              </SelectItem>
                              <SelectItem value="accessories">
                                {t("store.catalog.categories.accessories")}
                              </SelectItem>
                            </SelectContent>
                          </Select>
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="purchase_price" className="text-right">
                            Precio Compra
                          </Label>
                          <Input id="purchase_price" type="number" value={newProduct.purchase_price} onChange={handleInputChange} className="col-span-3" required />
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="sale_price" className="text-right">
                            {t("store.catalog.form.price")}
                          </Label>
                          <Input id="sale_price" type="number" value={newProduct.sale_price} onChange={handleInputChange} className="col-span-3" required />
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="current_stock" className="text-right">
                            {t("store.catalog.form.stock")}
                          </Label>
                          <Input id="current_stock" type="number" value={newProduct.current_stock} onChange={handleInputChange} className="col-span-3" required />
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="min_stock" className="text-right">
                            Stock Mínimo
                          </Label>
                          <Input id="min_stock" type="number" value={newProduct.min_stock} onChange={handleInputChange} className="col-span-3" required />
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="description" className="text-right">
                            {t("store.catalog.form.description")}
                          </Label>
                          <Textarea id="description" value={newProduct.description} onChange={(e) => setNewProduct(prev => ({ ...prev, description: e.target.value }))} className="col-span-3" />
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="product_image" className="text-right">
                            Imagen del Producto
                          </Label>
                          <Input id="product_image" type="file" onChange={handleImageChange} className="col-span-3" accept="image/*" />
                        </div>
                      </div>
                      <DialogFooter>
                        <Button type="submit" disabled={loading}>
                          {t("store.catalog.form.save")}
                        </Button>
                      </DialogFooter>
                    </form>
                  </DialogContent>
                </Dialog>
              </div>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>{t("store.catalog.table.name")}</TableHead>
                    <TableHead>{t("store.catalog.table.category")}</TableHead>
                    <TableHead>{t("store.catalog.table.price")}</TableHead>
                    <TableHead>{t("store.catalog.table.stock")}</TableHead>
                    <TableHead className="text-right">{t("store.catalog.table.actions")}</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {products.map((product) => (
                    <TableRow key={product.id}>
                      <TableCell className="font-medium">{product.name}</TableCell>
                      <TableCell>{product.category}</TableCell>
                      <TableCell>${product.sale_price.toFixed(2)}</TableCell>
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
                            <DropdownMenuItem>
                              <Edit className="mr-2 h-4 w-4" />
                              {t("store.catalog.actions.edit")}
                            </DropdownMenuItem>
                            <DropdownMenuItem>
                              <Package className="mr-2 h-4 w-4" />
                              {t("store.catalog.actions.updateStock")}
                            </DropdownMenuItem>
                            <DropdownMenuSeparator />
                            <DropdownMenuItem>
                              <Trash2 className="mr-2 h-4 w-4" />
                              {t("store.catalog.actions.delete")}
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
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="purchases" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>{t("store.purchases.title")}</CardTitle>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>{t("store.purchases.table.customer")}</TableHead>
                    <TableHead>{t("store.purchases.table.product")}</TableHead>
                    <TableHead>{t("store.purchases.table.quantity")}</TableHead>
                    <TableHead>{t("store.purchases.table.total")}</TableHead>
                    <TableHead>{t("store.purchases.table.date")}</TableHead>
                    <TableHead className="text-right">{t("store.purchases.table.actions")}</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {purchases.map((purchase) => (
                    <TableRow key={purchase.sale_id}>
                      <TableCell className="font-medium">{purchase.client_id}</TableCell>
                      <TableCell>{/* Puedes mostrar el producto relacionado si tienes ese dato */}</TableCell>
                      <TableCell>{/* Cantidad */}</TableCell>
                      <TableCell>${purchase.total_amount.toFixed(2)}</TableCell>
                      <TableCell>{purchase.sale_date}</TableCell>
                      <TableCell className="text-right">
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" className="h-8 w-8 p-0">
                              <span className="sr-only">{t("store.purchases.actions.open")}</span>
                              <MoreHorizontal className="h-4 w-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuLabel>{t("store.purchases.actions.title")}</DropdownMenuLabel>
                            <DropdownMenuItem>
                              <ShoppingCart className="mr-2 h-4 w-4" />
                              {t("store.purchases.actions.viewDetails")}
                            </DropdownMenuItem>
                            <DropdownMenuItem>
                              <History className="mr-2 h-4 w-4" />
                              {t("store.purchases.actions.customerHistory")}
                            </DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="inventory" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>{t("store.inventory.title")}</CardTitle>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>{t("store.inventory.table.product")}</TableHead>
                    <TableHead>{t("store.inventory.table.category")}</TableHead>
                    <TableHead>{t("store.inventory.table.inStock")}</TableHead>
                    <TableHead>{t("store.inventory.table.reorderLevel")}</TableHead>
                    <TableHead className="text-right">{t("store.inventory.table.actions")}</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {products.map((product) => (
                    <TableRow key={product.id}>
                      <TableCell className="font-medium">{product.name}</TableCell>
                      <TableCell>{product.category}</TableCell>
                      <TableCell>{product.current_stock}</TableCell>
                      <TableCell>
                        {product.current_stock < 20 ? (
                          <Badge variant="destructive">{t("store.inventory.lowStock")}</Badge>
                        ) : (
                          <Badge variant="secondary">{t("store.inventory.adequate")}</Badge>
                        )}
                      </TableCell>
                      <TableCell className="text-right">
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" className="h-8 w-8 p-0">
                              <span className="sr-only">{t("store.inventory.actions.open")}</span>
                              <MoreHorizontal className="h-4 w-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuLabel>{t("store.inventory.actions.title")}</DropdownMenuLabel>
                            <DropdownMenuItem>
                              <Package className="mr-2 h-4 w-4" />
                              {t("store.inventory.actions.updateStock")}
                            </DropdownMenuItem>
                            <DropdownMenuItem>
                              <Edit className="mr-2 h-4 w-4" />
                              {t("store.inventory.actions.editProduct")}
                            </DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
