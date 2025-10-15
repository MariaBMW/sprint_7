import requests
import allure
from urls import ORDERS_LIST

@allure.epic("Заказы")
@allure.feature("Список заказов")
class TestOrdersList:

    @allure.story("Возвращается список заказов")
    def test_get_orders_list(self):
        """В ответе есть поле orders, и это список"""
        with allure.step("Отправляем запрос на получение списка заказов"):
            response = requests.get(ORDERS_LIST)
        with allure.step("Проверяем содержимое ответа"):
            assert response.status_code == 200
            body = response.json()
            assert "orders" in body
            assert isinstance(body["orders"], list)