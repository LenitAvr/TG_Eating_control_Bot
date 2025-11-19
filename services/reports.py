import csv, io
def build_csv_meals(meals: list) -> bytes:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['timestamp','meal_name','item_name','weight_g','kcal','protein','fat','carbs'])
    for m in meals:
        for it in m.get('items', []):
            writer.writerow([m.get('timestamp'), m.get('name') or '', it.get('custom_name') or '', it.get('weight_g'),
                             it.get('kcal'), it.get('protein'), it.get('fat'), it.get('carbs')])
    return output.getvalue().encode('utf-8')

def ascii_summary(totals: dict) -> str:
    return f"""Calories: {totals.get('kcal')} kcal
Protein: {totals.get('protein')} g
Fat: {totals.get('fat')} g
Carbs: {totals.get('carbs')} g"""
