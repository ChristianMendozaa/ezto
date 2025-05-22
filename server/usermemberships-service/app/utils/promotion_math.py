def apply_promotion_to_price(price: float, discount_type: str, discount_value: float) -> float:
    if discount_type == "percentage":
        discount = price * (discount_value / 100)
    elif discount_type == "fixed":
        discount = discount_value
    else:
        raise ValueError("Tipo de descuento inválido")

    final_price = max(price - discount, 0.0)
    return round(final_price, 2)
