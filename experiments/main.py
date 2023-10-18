import pytest
import requests
import pprint
import json

poshlye_tryapky = {
    "brand": "Polo",
    "id": 1,
    "name": "Blue Top",
    "price": "Rs. 500",
    "category": {
        "category": "Tops",
        "usertype": {
            "usertype": "Women"
        }
    }
}

def test_check_status_code_is_200():
    url = "https://automationexercise.com/api/productsList"  # Замените на URL вашего API и путь к ресурсу
    response = requests.get(url)
    json_data = response.json()
    pprint.pprint(json_data)

    assert response.status_code == 200, f"Ошибка: статус ответа {response.status_code}"
    assert json_data["products"][0]["brand"] == "Polo"


def test_check_first_product_body_1():
    url = "https://automationexercise.com/api/productsList"
    response = requests.get(url)
    json_data = response.json()

    assert response.status_code == 200, f"Ошибка: статус ответа {response.status_code}"
    assert json_data["products"][0]["brand"] == poshlye_tryapky["brand"]
    assert json_data["products"][0]["id"] == poshlye_tryapky["id"]
    assert json_data["products"][0]["name"] == poshlye_tryapky["name"]
    assert json_data["products"][0]["price"] == poshlye_tryapky["price"]
    assert json_data["products"][0]["category"]["category"] == poshlye_tryapky["category"]["category"]
    assert json_data["products"][0]["category"]["usertype"]["usertype"] == poshlye_tryapky["category"]["usertype"]["usertype"]

def test_check_products_count():
    url = "https://automationexercise.com/api/productsList"  # Замените на URL вашего API и путь к ресурсу
    response = requests.get(url)
    json_data = response.json()
    products_count = json_data.get('products', [])
    actual_products_count = len(products_count)
    expected_product_count = 34
    print(products_count)
    assert expected_product_count == actual_products_count


def test_check_prices_are_valid():
    url = "https://automationexercise.com/api/productsList"  # Замените на URL вашего API и путь к ресурсу
    response = requests.get(url)
    json_data = response.json()
    products_count = json_data.get('products', [])

    product_prices_set = set()
    for product in products_count:
        price_str = product.get('price', [])
        try:
            price = float(price_str.replace('Rs. ', ''))
            product_prices_set.add(price)
        except ValueError:
            pytest.fail(f"Sosesh")

    for price in product_prices_set:
        assert price < 0, f"Progrev ne nachat"
    print(product_prices_set)



