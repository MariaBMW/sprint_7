import pytest
import requests
from utils import generate_random_string, delete_courier_by_id
from urls import CREATE_COURIER, LOGIN_COURIER
from data import ORDER_TEMPLATE

@pytest.fixture
def courier_data():
    # Генерирует уникальные данные нового курьера для теста
    return {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10)
    }

@pytest.fixture
def courier(courier_data):
    # Создаёт курьера, после теста удаляет его из системы
    response = requests.post(CREATE_COURIER, data=courier_data)
    assert response.status_code == 201
    login_resp = requests.post(LOGIN_COURIER, data={
        "login": courier_data['login'],
        "password": courier_data['password']
    })
    courier_id = login_resp.json().get("id")
    yield courier_data, courier_id
    if courier_id:
        delete_courier_by_id(courier_id)

@pytest.fixture
def order_data():
    # Копирует шаблон заказа, чтобы данные гарантированно не пересекались между тестами
    data = ORDER_TEMPLATE.copy()
    data["comment"] = generate_random_string(15)
    return data