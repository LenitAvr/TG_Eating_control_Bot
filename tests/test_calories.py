import pytest
from services.calories import calc_item_by_product, sum_items

def test_calc_item_by_product():
    product = {'kcal_per_100':200,'protein_per_100':10,'fat_per_100':5,'carbs_per_100':30}
    res = calc_item_by_product(product, 150)
    assert round(res['kcal'],2) == round(200*1.5,2)
    assert round(res['protein'],2) == round(10*1.5,2)

def test_sum_items():
    items = [{'kcal':100,'protein':10,'fat':5,'carbs':20},{'kcal':200,'protein':5,'fat':2,'carbs':30}]
    s = sum_items(items)
    assert s['kcal'] == 300
