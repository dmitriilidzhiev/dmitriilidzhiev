import pytest
import requests
import pprint
import json
import options



#First api

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

#allowed_cloth_bands = {
#    "H&M", "Madame", "Mast & Harbour", "Polo", "Babyhug", "Allen Solly Junior", ""
#}

def test_check_status_code_is_200():
    response = requests.get(options.first_url)
    json_data = response.json()
    # pprint.pprint(json_data)

    assert response.status_code == 200, f"Ошибка: статус ответа {response.status_code}"
    assert json_data["products"][0]["brand"] == "Polo"

#First exersize

def test_check_first_product_body_1():
    response = requests.get(options.first_url)
    json_data = response.json()

    assert response.status_code == 200, f"Ошибка: статус ответа {response.status_code}"
    assert json_data["products"][0]["brand"] == poshlye_tryapky["brand"]
    assert json_data["products"][0]["id"] == poshlye_tryapky["id"]
    assert json_data["products"][0]["name"] == poshlye_tryapky["name"]
    assert json_data["products"][0]["price"] == poshlye_tryapky["price"]
    assert json_data["products"][0]["category"]["category"] == poshlye_tryapky["category"]["category"]
    assert json_data["products"][0]["category"]["usertype"]["usertype"] == poshlye_tryapky["category"]["usertype"]["usertype"]

def test_check_products_count():
    response = requests.get(options.first_url)
    json_data = response.json()
    products_count = json_data.get('products', [])
    actual_products_count = len(products_count)
    expected_product_count = 34
    print(products_count)
    assert expected_product_count == actual_products_count


def test_check_prices_are_valid():
    response = requests.get(options.first_url)
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
        assert price > 0, f"Progrev ne nachat"
    print(product_prices_set)


#Second exersize api wrong method test
def test_check_second_api_wrong_status_code():
    response = requests.post(options.first_url)
    json_data = response.json()
    pprint.pprint(json_data)
    pprint.pprint(response.status_code)
    assert response.status_code == 200, f"samara"
    assert json_data["responseCode"]  == 405


#Third exersize Brands test api
def test_check_status_code():
    response = requests.get(options.second_url)
    json_data = response.json()
    pprint.pprint(json_data)
    pprint.pprint(response.status_code)
    brand_count = json_data.get('brands', [])
    actual_brand_count = len(brand_count)
    expected_brand_count = 34
    print(actual_brand_count)
    assert expected_brand_count == actual_brand_count
    assert response.status_code == 200, f"samara"

def test_check_third_check_first_brand_id():
    response = requests.get(options.second_url)
    json_data = response.json()
    assert json_data["brands"][0]["id"] == 1
    assert response.status_code == 200, f"samara"

