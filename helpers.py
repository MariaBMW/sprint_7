import random
import string
import requests
import allure
from urls import DELETE_COURIER, LOGIN_COURIER, CANCEL_ORDER
from data import ORDER_TEMPLATE

@allure.step("Генерация случайной строки длиной {length}")
def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

@allure.step("Генерация логина для несуществующего пользователя")
def generate_nonexistent_login():
    return "nonexistent" + generate_random_string(10)

@allure.step("Генерация данных тест-курьера")
def generate_courier_data():
    return {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10)
    }

@allure.step("Генерация данных заказа")
def generate_order_data():
    """
    Возвращает уникальные данные заказа на базе шаблона ORDER_TEMPLATE,
    чтобы исключить пересечения данных между тестами.
    """
    with allure.step("Копирование шаблона заказа и добавление уникального комментария"):
        data = ORDER_TEMPLATE.copy()
        data["comment"] = generate_random_string(15)
    return data

@allure.step("Удаление курьера по id={courier_id}")
def delete_courier_by_id(courier_id):
    url = DELETE_COURIER.format(courier_id=courier_id)
    response = requests.delete(url)
    return response.status_code

@allure.step("Получение id курьера по логину: {login}")
def get_courier_id(login, password):
    resp = requests.post(LOGIN_COURIER, json={"login": login, "password": password})
    if resp.status_code == 200:
        return resp.json().get("id")
    return None

@allure.step("Отмена заказа по треку {track}")
def cancel_order(track):
    response = requests.put(CANCEL_ORDER, params={"track": track})
    allure.attach(str(response.text), "Ответ отмены", allure.attachment_type.TEXT)
    return response.status_code

