import logging
from datetime import date
from httpx import AsyncClient
import os
from app.utils.promotion_math import apply_promotion_to_price

logger = logging.getLogger(__name__)

PROMOTION_SERVICE_URL = os.getenv("PROMOTIONS_SERVICE_HOST", "http://promotions-service:8000") + "/promotions"

class PromotionValidatorService:

    @staticmethod
    async def validate_and_apply_promotion(promotion_id: str, user_type: str, plan_price: float, today: date = date.today()) -> dict:
        """
        Llama al microservicio de promociones para obtener y validar una promoción.

        :param promotion_id: ID de la promoción
        :param user_type: 'new_users', 'loyal_users', etc.
        :param plan_price: Precio original del plan
        :param today: Fecha actual (por defecto hoy)
        :return: Diccionario con {valid, final_price, promotion_data, message}
        """
        try:
            async with AsyncClient() as client:
                url = f"{PROMOTION_SERVICE_URL}/{promotion_id}"
                response = await client.get(url)
                if response.status_code != 200:
                    return {
                        "valid": False,
                        "message": "Promoción no encontrada o inaccesible"
                    }

                promo = response.json().get("data") or response.json()
                
                # 🔍 Validar fechas
                start_date = date.fromisoformat(promo["start_date"])
                end_date = date.fromisoformat(promo["end_date"])
                if not (start_date <= today <= end_date):
                    return {
                        "valid": False,
                        "message": "La promoción no está activa en esta fecha"
                    }

                # 🔍 Validar tipo de usuario
                if promo["applicable_to"] != "all_users" and promo["applicable_to"] != user_type:
                    return {
                        "valid": False,
                        "message": f"La promoción no aplica a usuarios de tipo '{user_type}'"
                    }

                # ✅ Calcular precio final
                final_price = apply_promotion_to_price(
                    price=plan_price,
                    discount_type=promo["discount_type"],
                    discount_value=promo["discount_value"]
                )

                return {
                    "valid": True,
                    "final_price": final_price,
                    "promotion_data": promo,
                    "message": "Promoción válida"
                }

        except Exception as e:
            logger.error(f"❌ Error al validar promoción desde promotions-service: {e}")
            return {
                "valid": False,
                "message": "Error interno al validar la promoción"
            }
