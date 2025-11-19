from decimal import Decimal, ROUND_HALF_UP

def _scale(value: Decimal, grams: Decimal) -> Decimal:
    return (value * grams / Decimal(100)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def calc_item_by_product(product: dict, weight_g: float) -> dict:
    grams = Decimal(str(weight_g))
    kcal = _scale(Decimal(str(product['kcal_per_100'])), grams)
    protein = _scale(Decimal(str(product.get('protein_per_100', 0))), grams)
    fat = _scale(Decimal(str(product.get('fat_per_100', 0))), grams)
    carbs = _scale(Decimal(str(product.get('carbs_per_100', 0))), grams)
    return {'kcal': float(kcal), 'protein': float(protein), 'fat': float(fat), 'carbs': float(carbs)}

def sum_items(items: list) -> dict:
    total = {'kcal': 0.0, 'protein': 0.0, 'fat': 0.0, 'carbs': 0.0}
    for it in items:
        total['kcal'] += float(it.get('kcal', 0))
        total['protein'] += float(it.get('protein', 0))
        total['fat'] += float(it.get('fat', 0))
        total['carbs'] += float(it.get('carbs', 0))
    for k in total:
        total[k] = round(total[k], 2)
    return total
