// StaffFormDialog.tsx
import React, { useState, useEffect } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { PersonalInput } from "@/hooks/usePersonal";

interface StaffFormDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  initialData?: PersonalInput;
  onSave: (data: PersonalInput) => Promise<boolean>;
  title: string;
  description?: string;
}

export function StaffFormDialog({ open, onOpenChange, initialData, onSave, title, description }: StaffFormDialogProps) {
  const [formData, setFormData] = useState<PersonalInput>({ name: "", role: "trainer", schedule: "", access_level: "standard" });

  useEffect(() => {
    if (initialData) {
      setFormData(initialData);
    } else {
      setFormData({ name: "", role: "trainer", schedule: "", access_level: "standard" });
    }
  }, [initialData]);

  const handleChange = (field: keyof PersonalInput, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSave = async () => {
    const ok = await onSave(formData);
    if (ok) onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
          {description && <DialogDescription>{description}</DialogDescription>}
        </DialogHeader>
        <div className="grid gap-4 py-4">
          {/* Name */}
          <div className="grid grid-cols-3 gap-4 items-center">
            <Label htmlFor="name" className="text-right">Nombre</Label>
            <Input id="name" value={formData.name} onChange={e => handleChange("name", e.target.value)} className="col-span-2" />
          </div>
          {/* Role */}
          <div className="grid grid-cols-3 gap-4 items-center">
            <Label htmlFor="role" className="text-right">Rol</Label>
            <select id="role" value={formData.role} onChange={e => handleChange("role", e.target.value)} className="col-span-2 border rounded p-2">
              <option value="trainer">Trainer</option>
              <option value="receptionist">Receptionist</option>
              <option value="manager">Manager</option>
              <option value="maintenance">Maintenance</option>
            </select>
          </div>
          {/* Schedule */}
          <div className="grid grid-cols-3 gap-4 items-center">
            <Label htmlFor="schedule" className="text-right">Horario</Label>
            <Input id="schedule" value={formData.schedule} onChange={e => handleChange("schedule", e.target.value)} className="col-span-2" />
          </div>
          {/* Access Level */}
          <div className="grid grid-cols-3 gap-4 items-center">
            <Label htmlFor="access_level" className="text-right">Nivel de acceso</Label>
            <select id="access_level" value={formData.access_level} onChange={e => handleChange("access_level", e.target.value)} className="col-span-2 border rounded p-2">
              <option value="full">Full</option>
              <option value="standard">Standard</option>
              <option value="limited">Limited</option>
            </select>
          </div>
        </div>
        <DialogFooter>
          <Button onClick={handleSave}>{initialData ? "Actualizar" : "Crear"}</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}