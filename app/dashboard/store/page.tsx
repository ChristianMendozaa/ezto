"use client"

import { useState } from "react"
import { useLanguage } from "@/lib/hooks/use-language"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { MainNav } from "@/components/main-nav"
import { UserNav } from "@/components/user-nav"
import { Search, Plus, MoreHorizontal, Edit, Trash2, ShoppingCart, Package, History } from "lucide-react"
import { ThemeToggle } from "@/components/theme-toggle"
import { LanguageToggle } from "@/components/language-toggle"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Textarea } from "@/components/ui/textarea"

// Mock data for products
const products = [
  { id: 1, name: "Whey Protein", category: "Supplements", price: 29.99, stock: 50 },
  { id: 2, name: "Resistance Band Set", category: "Accessories", price: 15.99, stock: 30 },
  { id: 3, name: "Pre-Workout Powder", category: "Supplements", price: 34.99, stock: 40 },
  { id: 4, name: "Gym Gloves", category: "Accessories", price: 12.99, stock: 25 },
  { id: 5, name: "BCAA Capsules", category: "Supplements", price: 19.99, stock: 60 },
]

// Mock data for purchase history
const purchaseHistory = [
  { id: 1, customer: "John Doe", product: "Whey Protein", quantity: 2, total: 59.98, date: "2023-07-15" },
  { id: 2, customer: "Jane Smith", product: "Resistance Band Set", quantity: 1, total: 15.99, date: "2023-07-14" },
  { id: 3, customer: "Mike Johnson", product: "Pre-Workout Powder", quantity: 1, total: 34.99, date: "2023-07-13" },
  { id: 4, customer: "Emily Brown", product: "Gym Gloves", quantity: 1, total: 12.99, date: "2023-07-12" },
  { id: 5, customer: "Chris Wilson", product: "BCAA Capsules", quantity: 2, total: 39.98, date: "2023-07-11" },
]

export default function StorePage() {
  const { t } = useLanguage()
  const [activeTab, setActiveTab] = useState("catalog")
  const [isAddProductOpen, setIsAddProductOpen] = useState(false)

  return (
    <div className="hidden flex-col md:flex">
      <div className="border-b">
        <div className="flex h-16 items-center px-4">
          <MainNav className="mx-6" />
          <div className="ml-auto flex items-center space-x-4">
            <LanguageToggle />
            <ThemeToggle />
            <UserNav />
          </div>
        </div>
      </div>
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
                        <DialogDescription>{t("store.catalog.addProductDescription")}</DialogDescription>
                      </DialogHeader>
                      <div className="grid gap-4 py-4">
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="name" className="text-right">
                            {t("store.catalog.form.name")}
                          </Label>
                          <Input id="name" className="col-span-3" />
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
                              <SelectItem value="supplements">{t("store.catalog.categories.supplements")}</SelectItem>
                              <SelectItem value="accessories">{t("store.catalog.categories.accessories")}</SelectItem>
                            </SelectContent>
                          </Select>
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="price" className="text-right">
                            {t("store.catalog.form.price")}
                          </Label>
                          <Input id="price" type="number" className="col-span-3" />
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="stock" className="text-right">
                            {t("store.catalog.form.stock")}
                          </Label>
                          <Input id="stock" type="number" className="col-span-3" />
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="description" className="text-right">
                            {t("store.catalog.form.description")}
                          </Label>
                          <Textarea id="description" className="col-span-3" />
                        </div>
                      </div>
                      <DialogFooter>
                        <Button type="submit" onClick={() => setIsAddProductOpen(false)}>
                          {t("store.catalog.form.save")}
                        </Button>
                      </DialogFooter>
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
                        <TableCell>${product.price.toFixed(2)}</TableCell>
                        <TableCell>{product.stock}</TableCell>
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
                <div className="flex justify-between mb-4">
                  <div className="flex w-full max-w-sm items-center space-x-2">
                    <Input placeholder={t("store.search")} className="w-[300px]" />
                    <Button type="submit" size="icon">
                      <Search className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
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
                    {purchaseHistory.map((purchase) => (
                      <TableRow key={purchase.id}>
                        <TableCell className="font-medium">{purchase.customer}</TableCell>
                        <TableCell>{purchase.product}</TableCell>
                        <TableCell>{purchase.quantity}</TableCell>
                        <TableCell>${purchase.total.toFixed(2)}</TableCell>
                        <TableCell>{purchase.date}</TableCell>
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
                <div className="flex justify-between mb-4">
                  <div className="flex w-full max-w-sm items-center space-x-2">
                    <Input placeholder={t("store.search")} className="w-[300px]" />
                    <Button type="submit" size="icon">
                      <Search className="h-4 w-4" />
                    </Button>
                  </div>
                  <Button>
                    <Package className="mr-2 h-4 w-4" />
                    {t("store.inventory.updateStock")}
                  </Button>
                </div>
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
                        <TableCell>{product.stock}</TableCell>
                        <TableCell>
                          {product.stock < 20 ? (
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
    </div>
  )
}

