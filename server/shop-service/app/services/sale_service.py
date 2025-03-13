"""
Servicio para la gestión de ventas, utilizando SaleRepository.
"""
import uuid
from fastapi import HTTPException
from datetime import datetime
from app.repositories.sale_repository import SaleRepository
from app.models.purchase_model import SaleCreate, SaleResponse, SaleStatus

class SaleService:
    """
    Encapsula la lógica de negocio de ventas (sales),
    delegando la persistencia a SaleRepository.
    """

    @staticmethod
    async def create_sale(sale_data: SaleCreate, user: dict):
        """
        Crea una nueva venta:
        - Valida que el rol sea 'gym_owner' o 'gym_employee'.
        - Calcula subtotal, impuestos, total.
        - Genera un ID único y guarda en Firestore.
        """
        role = user.get("role")
        if role not in ["gym_owner", "gym_employee"]:
            raise HTTPException(status_code=403, detail="No tienes permiso para registrar ventas.")

        sale_id = str(uuid.uuid4())
        sale_date = datetime.utcnow().isoformat()

        # Calcular subtotal
        subtotal = 0.0
        for item in sale_data.items:
            unit_price = float(item.unit_price)
            discount = float(item.discount or 0)
            subtotal += (unit_price - discount) * item.quantity

        tax_rate = 0.15  # 15% de impuestos, por ejemplo
        tax_amount = round(subtotal * tax_rate, 2)
        total_amount = round(subtotal + tax_amount, 2)

        sale_dict = {
            "sale_id": sale_id,
            "client_id": sale_data.client_id,
            "items": [i.dict() for i in sale_data.items],
            "payment_method": sale_data.payment_method.value,
            "notes": sale_data.notes,
            "total_amount": total_amount,
            "tax_amount": tax_amount,
            "sale_date": sale_date,
            "seller_id": user.get("user_id"),
            "invoice_number": None,
            "status": SaleStatus.COMPLETADA.value
        }

        # Guardar en Firestore
        SaleRepository.create_sale(sale_dict)

        return SaleResponse(**sale_dict)

    @staticmethod
    async def get_all_sales():
        """
        Retorna la lista de todas las ventas.
        """
        sales_data = SaleRepository.get_all_sales()
        return [SaleResponse(**data) for data in sales_data]

    @staticmethod
    async def get_sale_by_id(sale_id: str):
        """
        Obtiene la información de una venta por su ID.
        """
        data = SaleRepository.get_sale_by_id(sale_id)
        if not data:
            return None
        return SaleResponse(**data)

    @staticmethod
    async def delete_sale(sale_id: str):
        """
        Elimina una venta de Firestore.
        """
        return SaleRepository.delete_sale(sale_id)
