"""
Servicio para la gestión de productos en Firestore, utilizando el ProductRepository.
Incluye:
- Creación de productos (con compresión de imagen en WebP y conversión a Base64).
- Obtención de todos los productos o uno en particular por ID.
- Actualización parcial de campos.
- Eliminación de un producto.
"""
import logging
import base64
import io
from datetime import date
from typing import Optional
from fastapi import UploadFile, HTTPException
from PIL import Image

from app.models.product_model import ProductBase, ProductResponse
from app.repositories.product_repository import ProductRepository

logging.basicConfig(level=logging.INFO)

class ProductService:
    """
    Clase que encapsula la lógica de negocio para operar con productos,
    delegando la persistencia al ProductRepository.
    """

    @staticmethod
    async def create_product(product_data: ProductBase, product_image: Optional[UploadFile], user: dict):
        """
        Crea un nuevo producto en la colección 'products' de Firestore.

        1. Verifica que el usuario tenga rol 'gym_owner'.
        2. Comprime la imagen (si se proporciona) a WebP y la convierte a Base64.
        3. Calcula el profit_margin.
        4. Construye el diccionario para almacenar en Firestore y llama al repositorio.
        5. Retorna un ProductResponse.

        Raises:
            HTTPException(403): Si el usuario no tiene rol de 'gym_owner'.
            HTTPException(400): Si hay problemas con la imagen o la validación de datos.
        """
        # Validar rol
        if user.get("role") != "gym_owner":
            raise HTTPException(status_code=403, detail="No tienes permiso para crear productos.")

        # Procesar imagen
        image_base64 = None
        if product_image:
            try:
                content = await product_image.read()
                image = Image.open(io.BytesIO(content)).convert("RGB")
                image.thumbnail((800, 800))  # Redimensionar
                buffer = io.BytesIO()
                image.save(buffer, format="WEBP", quality=70)  # Comprimir a WebP
                compressed_content = buffer.getvalue()
                image_base64 = base64.b64encode(compressed_content).decode("utf-8")
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error al procesar la imagen: {str(e)}")

        # Calcular margen de ganancia
        profit_margin = float(
            (product_data.sale_price - product_data.purchase_price) / product_data.purchase_price * 100
        )

        # Preparar diccionario para Firestore
        from uuid import uuid4
        product_id = str(uuid4())
        now_str = str(date.today())

        product_dict = {
            "id": product_id,
            "name": product_data.name,
            "sku": product_data.sku,
            "category": product_data.category.value,
            "description": product_data.description,
            "purchase_price": float(product_data.purchase_price),
            "sale_price": float(product_data.sale_price),
            "current_stock": product_data.current_stock,
            "min_stock": product_data.min_stock,
            "expiration_date": str(product_data.expiration_date) if product_data.expiration_date else None,
            "supplier_id": product_data.supplier_id,
            "barcode": product_data.barcode,
            "status": product_data.status.value,
            "image_base64": image_base64,
            "created_at": now_str,
            "last_updated": now_str,
            "profit_margin": profit_margin
        }

        # Guardar en Firestore mediante el repositorio
        ProductRepository.create_product(product_dict)

        # Retornar un ProductResponse
        return ProductResponse(**product_dict)

    @staticmethod
    async def get_all_products():
        """
        Retorna la lista de todos los productos registrados en Firestore,
        delegando al ProductRepository.
        """
        products_data = ProductRepository.get_all_products()
        return [ProductResponse(**data) for data in products_data]

    @staticmethod
    async def get_product_by_id(product_id: str):
        """
        Obtiene un producto específico por su ID, usando el repositorio.
        """
        data = ProductRepository.get_product_by_id(product_id)
        if not data:
            return None
        return ProductResponse(**data)

    @staticmethod
    async def update_product(product_id: str, product_data: dict):
        """
        Actualiza uno o varios campos de un producto existente.

        product_data debe contener los campos: sale_price, current_stock, min_stock, status, description.
        """
        # Obtener datos antiguos
        old_data = ProductRepository.get_product_by_id(product_id)
        if not old_data:
            return None

        # Preparar campos a actualizar
        updated_fields = {}
        for key in ["sale_price", "current_stock", "min_stock", "status", "description"]:
            if key in product_data and product_data[key] is not None:
                updated_fields[key] = product_data[key]

        # Actualizar 'last_updated'
        updated_fields["last_updated"] = str(date.today())

        # Recalcular profit_margin si hay cambio en sale_price
        sale_price = float(updated_fields.get("sale_price", old_data["sale_price"]))
        purchase_price = float(old_data["purchase_price"])
        updated_fields["profit_margin"] = float((sale_price - purchase_price) / purchase_price * 100)

        # Llamar al repositorio para hacer el update
        new_data = ProductRepository.update_product(product_id, updated_fields)
        if not new_data:
            return None
        return ProductResponse(**new_data)

    @staticmethod
    async def delete_product(product_id: str):
        """
        Elimina un producto de Firestore. Retorna True/False.
        """
        success = ProductRepository.delete_product(product_id)
        return success
