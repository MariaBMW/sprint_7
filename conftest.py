import pytest
import allure
from helpers import delete_courier_by_id, create_courier

@pytest.fixture
def courier():
    """
    Фикстура для создания и удаления курьера.
    Каждый тест сам генерирует courier_data и передает в фикстуру courier(data).
    """
    def _create_and_cleanup(courier_data):
        with allure.step("Создание тестового курьера через helpers.py"):
            courier_id, response = create_courier(courier_data)
        yield courier_data, courier_id, response
        with allure.step("Удаление курьера после завершения теста"):
            if courier_id:
                delete_courier_by_id(courier_id)
    return _create_and_cleanup


    