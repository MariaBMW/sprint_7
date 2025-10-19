import pytest
import requests
import allure
from urls import CREATE_ORDER
from data import ORDER_COLORS
from helpers import generate_order_data, cancel_order

@allure.epic("Заказы")
@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Заказ можно создать с разными вариантами цвета: {colors}")
    @pytest.mark.parametrize("colors", ORDER_COLORS)
    def test_create_order_colors(self, colors):
        with allure.step(f"Готовим валидные данные заказа с цветом(ами): {colors}"):
            data = generate_order_data()
            data['color'] = colors
        with allure.step("Отправляем запрос на создание заказа"):
            response = requests.post(CREATE_ORDER, json=data)
        with allure.step("Проверяем успешность создания заказа и наличие трека"):
            assert response.status_code == 201, f"status_code: {response.status_code}, тело: {response.text}"
            track = response.json().get("track")
            assert track is not None, "Нет track в ответе"
        with allure.step("Отменяем созданный заказ"):
            cancel_order(track)