import pytest
import requests
import allure
from urls import CREATE_COURIER
from helpers import (
    generate_courier_data,
    delete_courier_by_id,
    get_courier_id,
    generate_order_data,
)

@pytest.fixture
def courier_data():
    with allure.step("Генерация данных для нового курьера"):
        return generate_courier_data()

@pytest.fixture
def courier(courier_data):
    with allure.step("Создание тестового курьера"):
        response = requests.post(CREATE_COURIER, json=courier_data)
        assert response.status_code == 201, f"Курьер не создан: {response.text}"
        courier_id = get_courier_id(courier_data["login"], courier_data["password"])
        assert courier_id is not None, "Не удалось получить id курьера"

    yield courier_data, courier_id, response

    with allure.step("Удаление тестового курьера после теста"):
        if courier_id:  # Проверяем, что курьер создан
            status_code = delete_courier_by_id(courier_id)
            assert status_code == 200, f"Курьер не удален, статус: {status_code}"

@pytest.fixture
def order_data():
    with allure.step("Генерирование изолированных тест-данных заказа"):
        # Используем хелпер для генерации свежих уникальных данных заказа
        return generate_order_data()
    