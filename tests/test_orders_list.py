import requests
import allure
from urls import ORDERS_LIST

@allure.epic("Заказы")
@allure.feature("Список заказов")
class TestOrdersList:

    @allure.title("В теле ответа возвращается список заказов")
    def test_get_orders_list(self):
        with allure.step("Отправляем запрос на получение списка заказов"):
            response = requests.get(ORDERS_LIST)
        with allure.step("Проверяем, что ответ содержит список orders"):
            assert response.status_code == 200
            data = response.json()
            assert "orders" in data
            assert isinstance(data["orders"], list)