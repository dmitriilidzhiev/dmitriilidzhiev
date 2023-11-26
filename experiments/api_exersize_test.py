import pytest
import requests
import pprint
import jsonschema
from faker import Faker

fake = Faker()



server_url = 'https://automationexercise.com/api'

first_product = {
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


brands_scheme = {
    "type": "object",
    "required": ["responseCode", "brands"],
    "properties": {
        "responseCode": {
            "type": "integer",
            "enum": [200]
        },
        "brands": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "brand"],
                "properties": {
                    "id": {
                        "type": "integer"
                    },
                    "brand": {
                        "type": "string"
                    }
                },
                "additionalProperties": False
            }
        }
    },
    "additionalProperties": False
}


search_category_scheme = {
    "type": "object",
    "required": ["responseCode"],
    "properties": {
        "responseCode": {
            "type": "integer",
            "enum": [200]
        },
        "products": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "brand"],
                "properties": {
                    "brand": {
                        "type": "string"
                    },
                    "category": {
                        "type": "object",
                        "items": {

                            "properties": {
                                "category": {
                                    "type": "string"
                                },
                                "usertype": {
                                    "type": "string"
                                }
                            }
                        }
                    },
                    "id": {
                        "type": "integer"
                    },
                    "name": {
                        "type": "string"
                    },
                    "price": {
                        "type": "string"
                    },
                },
                "additionalProperties": False
            }
        }
    },
    "additionalProperties": False
}


#API1 - exersize

def test_check_first_endpoint_success_200():

    response = requests.get(f"{server_url}/productsList")
    json_data = response.json()
    pprint.pprint(json_data)

    assert response.status_code == 200, f"Ошибка: статус ответа {response.status_code}"
    assert json_data["products"][0]["brand"] == "Polo"

def test_check_first_endpoint_product_body_check():
    response = requests.get(f"{server_url}/productsList")
    json_data = response.json()
    pprint.pprint(json_data)

    assert response.status_code == 200, f"Ошибка: статус ответа {response.status_code}"
    assert json_data["products"][0]["brand"] == first_product["brand"]
    assert json_data["products"][0]["id"] == first_product["id"]
    assert json_data["products"][0]["name"] == first_product["name"]
    assert json_data["products"][0]["price"] == first_product["price"]
    assert json_data["products"][0]["category"]["category"] == first_product["category"]["category"]
    assert json_data["products"][0]["category"]["usertype"]["usertype"] == first_product["category"]["usertype"]["usertype"]

def test_check_first_endpoint_products_count():
    response = requests.get(f"{server_url}/productsList")
    json_data = response.json()
    products_count = json_data.get('products', [])
    actual_products_count = len(products_count)
    print(products_count)

    assert 0 < actual_products_count


def test_check_first_endpoint_all_product_prices_are_notnull_or_negative():
    response = requests.get(f"{server_url}/productsList")
    json_data = response.json()
    products_count = json_data.get('products', [])
    product_prices_set = set()

    for product in products_count:
        price_str = product.get('price', [])
        try:
            price = float(price_str.replace('Rs. ', ''))
            product_prices_set.add(price)
        except ValueError:
            pytest.fail(f"there is products with negative price")
    for price in product_prices_set:
        assert price > 0.1, f"Product prices are ok"
    print(product_prices_set)


#API2 - exersize

def test_check_first_endpoint_invalid_method():

    response = requests.post(f"{server_url}/productsList")
    json_data = response.json()
    assert json_data["responseCode"] == 405, f"Ошибка: статус ответа {response.status_code}"


##API3 - exersize

def test_check_second_endpoint_success():
    response = requests.get(f"{server_url}/brandsList")
    json_data = response.json()
    pprint.pprint(json_data)
    pprint.pprint(response.status_code)
    jsonschema.validate(json_data, brands_scheme)
    assert response.status_code == 200, f"samara"



def test_check_second_endpoint_wrong_status_code():
    response = requests.post(f"{server_url}/brandsList")
    json_data = response.json()
    pprint.pprint(json_data)
    pprint.pprint(response.status_code)
    assert response.status_code == 200, f"samara"
    assert json_data["responseCode"]  == 405

def test_check_second_endpoint_at_least_one_brand_present():
    response = requests.get(f"{server_url}/brandsList")
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
    response = requests.get(f"{server_url}/brandsList")
    json_data = response.json()
    assert json_data["brands"][0]["brand"] == 'Polo'
    assert response.status_code == 200, f"samara"

##API4 -exersize

def test_check_second_endpoint_wrong_status_code():
    response = requests.put(f"{server_url}/brandsList")
    json_data = response.json()
    pprint.pprint(json_data)
    pprint.pprint(response.status_code)
    assert response.status_code == 200, f"samara"
    assert json_data["responseCode"]  == 405

##API5 - exersize


def test_check_third_endpoint_schema_validation():
    target_product = "jean"
    search_parameter = {
        "search_product": target_product
    }
    response = requests.post(f"{server_url}/searchProduct", data = search_parameter)
    json_data = response.json()
    pprint.pprint(json_data)
    assert response.status_code == 200, f"samara"
    jsonschema.validate(json_data, search_category_scheme)


def test_check_third_endpoint_empty_result():
    target_product = "tshirtf"
    search_parameter = {
        "search_product": target_product
    }
    response = requests.post(f"{server_url}/searchProduct", data = search_parameter)
    json_data = response.json()
    pprint.pprint(json_data)
    assert response.status_code == 200, f"samara"
    assert len(json_data["products"]) == 0, f"samara"

def test_check_third_endpoint_request_all():
    target_product = ""
    search_parameter = {
        "search_product": target_product
    }
    response = requests.post(f"{server_url}/searchProduct", data=search_parameter)
    json_data = response.json()
    pprint.pprint(json_data)
    assert response.status_code == 200, f"samara"
    assert len(json_data["products"]) == 0, f"samara"

def test_check_third_endpoint_search_parameter_invalid_value_type():
    target_product = {
        "samara": 33,
        "ssss": "33"
    }
    search_parameter = {
        "search_product": target_product
    }
    response = requests.post(f"{server_url}/searchProduct", data=search_parameter)
    json_data = response.json()
    pprint.pprint(json_data)
    assert response.status_code == 200, f"samara"
    assert len(json_data["products"]) == 0, f"samara"

##API6- exersize

def test_check_third_endpoint_search_product_is_not_provided():
    response = requests.post(f"{server_url}/searchProduct")
    json_data = response.json()
    pprint.pprint(json_data)
    assert json_data["responseCode"] == 400, f"samara"
    assert json_data["message"] == "Bad request, search_product parameter is missing in POST request.", f"samara"

##API7- exersize

def test_check_fourth_endpoint_request_all():

    user_credentials = {
        "email": "dmitrii.lidzhiev@gmail.com",
        "password": "123123123"
    }
    response = requests.post(f"{server_url}/verifyLogin", data=user_credentials)
    json_data = response.json()
    pprint.pprint(json_data)
    assert response.status_code == 200, f"samara"
    assert json_data["message"] == "User exists!", f"samara"

def test_check_fourth_endpoint_wrong_value_type():
    user_credentials = {
        "email": 3333,
        "password": 33333
    }
    response = requests.post(f"{server_url}/verifyLogin", data=user_credentials)
    json_data = response.json()
    pprint.pprint(json_data)
    assert response.status_code == 200, f"samara"
    assert json_data["message"] == "User not found!", f"samara"

def test_check_fourth_endpoint_invalid_parameter_name():
    user_credentials = {
        "hemail": 3333,
        "shpassword": 33333
    }
    response = requests.post(f"{server_url}/verifyLogin", data=user_credentials)
    json_data = response.json()
    pprint.pprint(json_data)
    assert response.status_code == 200, f"samara"
    assert json_data["responseCode"] == 400
    assert json_data["message"] == "Bad request, email or password parameter is missing in POST request.", f"samara"



##API9 -exersize

def test_check_third_wrong_method_use():
    user_credentials = {
        "email": "dmitrii.lidzhiev@gmail.com",
        "password": "123123123"
    }
    response = requests.delete(f"{server_url}/verifyLogin", data=user_credentials)
    json_data = response.json()
    pprint.pprint(json_data)
    assert response.status_code == 200, f"samara"
    assert json_data["responseCode"] == 405, f"Ошибка: статус ответа {response.status_code}"
    assert json_data["message"] == "This request method is not supported."

##API10 -exersize

def test_check_fourth_endpoint_user_does_not_exists():
    user_credentials = {
        "email": "ssssss.sssss@ss.com",
        "password": "sssssssssss"
    }
    response = requests.post(f"{server_url}/verifyLogin", data=user_credentials)
    json_data = response.json()
    pprint.pprint(json_data)
    assert response.status_code == 200, f"samara"
    assert json_data["message"] == "User not found!", f"samara"


##API11 -exersize

def test_check_fourth_endpoint_success_user_creating():
    random_email = fake.email()
    new_user_credentials = {
        "name": "ABOBUS",
        "email": random_email,
        "password": "ABOBUSAVTOBUS",
        "title": "Mr",
        "birth_date": "10",
        "birth_month": "10",
        "birth_year": "2000",
        "firstname": "ABOBUS-first-name",
        "lastname": "ABOBUS-last-name",
        "company": "ABOBUS-company",
        "address1": "ABOBUS-address-1",
        "address2": "ABOBUS-address-2",
        "country": "ABOBUS-country",
        "zipcode": "1234432",
        "state": "ABOBO-state",
        "city": "Donda",
        "mobile_number": "+79657643276",
    }
    response = requests.post(f"{server_url}/createAccount", data=new_user_credentials)
    json_data = response.json()
    pprint.pprint(json_data)
    assert response.status_code == 200, f"samara"
    assert json_data["message"] == "User created!", f"samara"

def test_check_fourth_endpoint_body_is_missing():

    response = requests.post(f"{server_url}/createAccount", )
    json_data = response.json()
    pprint.pprint(json_data)
    assert response.status_code == 200, f"samara"
    assert json_data["responseCode"] == 400
    assert json_data["message"] == "Bad request, name parameter is missing in POST request."

def test_check_fourth_endpoint_body_is_missing():

    response = requests.post(f"{server_url}/createAccount", )
    json_data = response.json()
    pprint.pprint(json_data)
    assert response.status_code == 200, f"samara"
    assert json_data["responseCode"] == 400
    assert json_data["message"] == "Bad request, name parameter is missing in POST request."


def test_check_fourth_endpoint_only_mandatory_fields():
    random_email = fake.email()
    new_user_credentials = {
        "name": "ABOBUS",
        "email": random_email,
        "password": "ABOBUSAVTOBUS",
        "firstname": "ABOBUS-first-name",
        "lastname": "ABOBUS-last-name",
        "company": "ABOBUS-company",
        "address1": "ABOBUS-address-1",
        "country": "ABOBUS-country",
        "zipcode": "1234432",
        "state": "ABOBO-state",
        "city": "Donda",
        "mobile_number": "+79657643276",
    }
    response = requests.post(f"{server_url}/createAccount", data=new_user_credentials)
    json_data = response.json()
    pprint.pprint(json_data)
    assert response.status_code == 200, f"samara"
    assert json_data["message"] == "User created!", f"samara"

def test_check_fourth_endpoint_without_mandatory_field():
    random_email = fake.email()
    new_user_credentials = {
        "email": random_email,
        "password": "ABOBUSAVTOBUS",
        "firstname": "ABOBUS-first-name",
        "lastname": "ABOBUS-last-name",
        "company": "ABOBUS-company",
        "address1": "ABOBUS-address-1",
        "country": "ABOBUS-country",
        "zipcode": "1234432",
        "state": "ABOBO-state",
        "city": "Donda",
        "mobile_number": "+79657643276",
    }
    response = requests.post(f"{server_url}/createAccount", data=new_user_credentials)
    json_data = response.json()
    pprint.pprint(json_data)
    assert response.status_code == 200, f"samara"
    assert json_data["message"] == "Bad request, name parameter is missing in POST request."
    assert json_data["responseCode"] == 400



def test_check_fourth_endpoint_mandatory_field_is_empty():

    new_user_credentials = {
        "name": "ABOBUS",
        "email": "sasasa@sss.com",
        "password": "ABOBUSAVTOBUSABBOBUSAVTOBUS",
        "firstname": "ABOBUS-first-name",
        "lastname": "ABOBUS-last-name",
        "company": "ABOBUS-company",
        "address1": "ABOBUS-address-1",
        "country": "ABOBUS-country",
        "zipcode": "1234432",
        "state": "ABOBO-state",
        "city": "Donda",
        "mobile_number": "+79657643276",
    }
    response = requests.post(f"{server_url}/createAccount", data=new_user_credentials)
    json_data = response.json()
    pprint.pprint(json_data)
    assert response.status_code == 200, f"samara"
    ##Should be error to validate email
    assert json_data["message"] == "Email already exists!"
    assert json_data["responseCode"] == 400


##API12 -exersize

def test_check_fifth_endpoint_user_deletion():
    new_user_credentials = {
        "name": "ABOBUS",
        "email": "sasasa@sss.com",
        "password": "ABOBUSAVTOBUSABBOBUSAVTOBUS",
        "firstname": "ABOBUS-first-name",
        "lastname": "ABOBUS-last-name",
        "company": "ABOBUS-company",
        "address1": "ABOBUS-address-1",
        "country": "ABOBUS-country",
        "zipcode": "1234432",
        "state": "ABOBO-state",
        "city": "Donda",
        "mobile_number": "+79657643276",
    }
    response = requests.post(f"{server_url}/createAccount", data=new_user_credentials)
    delete_user_credentials = {
        "email": "sasasa@sss.com",
        "password": "ABOBUSAVTOBUSABBOBUSAVTOBUS",
    }
    response = requests.delete(f"{server_url}/deleteAccount", data=delete_user_credentials)
    json_data = response.json()
    pprint.pprint(json_data)
    assert response.status_code == 200, f"samara"
    assert json_data["message"] == "Account deleted!"
    assert json_data["responseCode"] == 200


def test_check_fifth_endpoint_not_existing_user():
    delete_user_credentials = {
        "email": "sasasa@sss.com",
        "password": "ABOBUSAVTOBUSABBOBUSAVTOBUS",
    }
    response = requests.delete(f"{server_url}/deleteAccount", data=delete_user_credentials)
    json_data = response.json()
    pprint.pprint(json_data)
    assert response.status_code == 200, f"samara"
    assert json_data["message"] == "Account not found!"
    assert json_data["responseCode"] == 404

def test_check_fifth_endpoint_invalid_parameters():
    delete_user_credentials = {
        "emdddail": "sasasa@sss.com",
        "passwdddord": "ABOBUSAVTOBUSABBOBUSAVTOBUS",
    }
    response = requests.delete(f"{server_url}/deleteAccount", data=delete_user_credentials)
    json_data = response.json()
    pprint.pprint(json_data)
    assert response.status_code == 200, f"samara"
    assert json_data["message"] == "Bad request, email parameter is missing in DELETE request."
    assert json_data["responseCode"] == 400

def test_check_fifth_endpoint_parameters_is_missing():
    delete_user_credentials = {
    }
    response = requests.delete(f"{server_url}/deleteAccount", data=delete_user_credentials)
    json_data = response.json()
    pprint.pprint(json_data)
    assert response.status_code == 200, f"samara"
    assert json_data["message"] == "Bad request, email parameter is missing in DELETE request."
    assert json_data["responseCode"] == 400

def test_check_fifth_endpoint_parameters_are_empty():
    delete_user_credentials = {
        "email": "",
        "password": "",
    }
    response = requests.delete(f"{server_url}/deleteAccount", data=delete_user_credentials)
    json_data = response.json()
    pprint.pprint(json_data)
    assert response.status_code == 200, f"samara"
    assert json_data["message"] == "Account not found!"
    assert json_data["responseCode"] == 404


##API13 -exersize

def test_test_check_sixth_endpoint_success_user_creating():
    update_body_user_credentials = {
        "name": "ABOBUS",
        "email": "sddasasa@sss.com",
        "password": "ABOBUSAVTOBUdSABBOBUSAVTOBUS",
        "title": "Mr",
        "birth_date": "10",
        "birth_month": "10",
        "birth_year": "2000",
        "firstname": "ABOBUS-first-name",
        "lastname": "ABOBUS-last-name",
        "company": "ABOBUS-company",
        "address1": "ABOBUS-address-1",
        "address2": "ABOBUS-address-2",
        "country": "ABOBUS-country",
        "zipcode": "1234432",
        "state": "ABOBO-state",
        "city": "Donda",
        "mobile_number": "+79657643276",
    }
    response = requests.put(f"{server_url}/updateAccount", data = update_body_user_credentials)
    json_data = response.json()
    pprint.pprint(json_data)
    assert response.status_code == 200, f"samara"
    assert json_data["message"] == "User updated!", f"samara"




def test_test_check_sixth_endpoint_wrong_password():
    update_body_user_credentials = {
        "name": "ABOBUS",
        "email": "sddasasa@sss.com",
        "password": "AdS",
        "title": "Mr",
        "birth_date": "10",
        "birth_month": "10",
        "birth_year": "2000",
        "firstname": "ABOBUS-first-name",
        "lastname": "ABOBUS-last-name",
        "company": "ABOBUS-company",
        "address1": "ABOBUS-address-1",
        "address2": "ABOBUS-address-2",
        "country": "ABOBUS-country",
        "zipcode": "1234432",
        "state": "ABOBO-state",
        "city": "Donda",
        "mobile_number": "+79657643276",
    }
    response = requests.put(f"{server_url}/updateAccount", data= update_body_user_credentials)
    json_data = response.json()
    pprint.pprint(json_data)
    assert response.status_code == 200, f"samara"
    assert json_data["message"] == "Account not found!"


def test_test_check_sixth_endpoint_wrong_email():
    update_body_user_credentials = {
        "name": "ABOBUS",
        "email": "avokado@akado.com",
        "password": "ABOBUSAVTOBUdSABBOBUSAVTOBUS",
        "title": "Mr",
        "birth_date": "10",
        "birth_month": "10",
        "birth_year": "2000",
        "firstname": "ABOBUS-first-name",
        "lastname": "ABOBUS-last-name",
        "company": "ABOBUS-company",
        "address1": "ABOBUS-address-1",
        "address2": "ABOBUS-address-2",
        "country": "ABOBUS-country",
        "zipcode": "1234432",
        "state": "ABOBO-state",
        "city": "Donda",
        "mobile_number": "+79657643276",
    }
    response = requests.put(f"{server_url}/updateAccount", data=update_body_user_credentials)
    json_data = response.json()
    pprint.pprint(json_data)
    assert response.status_code == 200, f"samara"
    assert json_data["message"] == "Account not found!"



def test_test_check_sixth_endpoint_updating_fields_to_empty():

    update_body_user_credentials = {
        "name": "ABOBUS",
        "email": "sddasasa@sss.com",
        "password": "ABOBUSAVTOBUdSABBOBUSAVTOBUS",
        "title": "",
        "birth_date": "",
        "birth_month": "",
        "birth_year": "",
        "firstname": "",
        "lastname": "",
        "company": " ",
        "address1": "",
        "address2": "",
        "country": "",
        "zipcode": "",
        "state": "",
        "city": "",
        "mobile_number": "",
    }
    response = requests.put(f"{server_url}/updateAccount", data=update_body_user_credentials)
    json_data = response.json()
    pprint.pprint(json_data)
    assert response.status_code == 200, f"samara"
    assert json_data["message"] == "User updated!", f"samara"



def test_test_check_sixth_endpoint_without_body():

    response = requests.put(f"{server_url}/updateAccount", )
    json_data = response.json()
    pprint.pprint(json_data)
    assert response.status_code == 200, f"samara"
    assert json_data["message"] == "Bad request, email parameter is missing in PUT request."
    assert json_data["responseCode"] == 400

def test_test_check_sixth_endpoint_no_fields_are_updated():
    update_body_user_credentials = {
        "email": "sddasasa@sss.com",
        "password": "ABOBUSAVTOBUdSABBOBUSAVTOBUS",
    }

    response = requests.put(f"{server_url}/updateAccount", data= update_body_user_credentials )
    json_data = response.json()
    pprint.pprint(json_data)
    assert response.status_code == 200, f"samara"
    assert json_data["message"] == "User updated!"
    assert json_data["responseCode"] == 200

def test_test_check_sixth_wrong_parameter_name():
    update_body_user_credentials = {
        "email": "sddasasa@sss.com",
        "password": "ABOBUSAVTOBUdSABBOBUSAVTOBUS",
        "pity": "peegeetee",
    }

    response = requests.put(f"{server_url}/updateAccount", data= update_body_user_credentials )
    json_data = response.json()
    pprint.pprint(json_data)
    assert response.status_code == 200, f"samara"
    ##It's actually an error
    assert json_data["message"] == "User updated!"
    assert json_data["responseCode"] == 200

def test_test_check_sixth_wrong_method():
    update_body_user_credentials = {
        "email": "sddasasa@sss.com",
        "password": "ABOBUSAVTOBUdSABBOBUSAVTOBUS",
        "pity": "peegeetee",
    }

    response = requests.get(f"{server_url}/updateAccount", data= update_body_user_credentials )
    json_data = response.json()
    pprint.pprint(json_data)
    assert response.status_code == 200, f"samara"
    assert json_data["detail"] == "Method \"GET\" not allowed."
    assert json_data["responseCode"] == 405

##API14 -exersize

def test_test_check_seventh_wrong_parameter_name():
    email = "&email=sddasasa@sss.com"
    response = requests.get(f"{server_url}/getUserDetailByEmail", params= email )
    json_data = response.json()
    pprint.pprint(json_data)
    assert response.status_code == 200, f"samara"


def test_test_check_wrong_method():
    email = "&email=sddasasa@sss.com"
    response = requests.delete(f"{server_url}/getUserDetailByEmail", params= email )
    json_data = response.json()
    pprint.pprint(json_data)
    assert response.status_code == 200, f"samara"