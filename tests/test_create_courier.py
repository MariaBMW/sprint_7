import pytest
import requests
import allure
from urls import CREATE_COURIER
from data import ERROR_MESSAGES
from helpers import generate_courier_data

@allure.epic("Курьеры")
@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.title("Курьера можно создать")
    def test_create_courier_success(self, courier):
        courier_data = generate_courier_data()
        with allure.step("Создаём курьера через функцию-фикстуру"):
            for courier_data, courier_id, response in courier(courier_data):
                with allure.step("Проверяем статус-код ответа"):
                    assert response.status_code == 201, "Неверный статус-код при создании курьера"
                with allure.step("Проверяем флаг ok в ответе"):
                    assert response.json().get("ok") is True, "Флаг ok отсутствует или не равен True"

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_two_same_couriers(self, courier):
        courier_data = generate_courier_data()
        with allure.step("Создаём первого курьера через функцию-фикстуру"):
            for courier_data, courier_id, response in courier(courier_data):
                with allure.step("Проверяем успешное создание первого курьера"):
                    assert response.status_code == 201
                with allure.step("Пробуем создать второго курьера с теми же данными"):
                    response2 = requests.post(CREATE_COURIER, json=courier_data)
                with allure.step("Проверяем, что возвращается ошибка о существовании курьера"):
                    assert response2.status_code == 409
                    assert ERROR_MESSAGES["courier_exists"] in response2.text

    @allure.title("Не удаётся создать курьера без обязательных полей")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_field(self, missing_field):
        """Создание курьера без обязательного поля должно вернуть ошибку"""
        data = generate_courier_data()
        data.pop(missing_field)
        with allure.step(f"Пробуем создать курьера без поля {missing_field}"):
            response = requests.post(CREATE_COURIER, json=data)
            assert response.status_code == 400
            assert ERROR_MESSAGES["no_data_create"] in response.text

    @allure.title("Создать курьера с существующим логином нельзя")
    def test_create_courier_with_existing_login(self, courier):
        courier_data = generate_courier_data()
        with allure.step("Создаём первого курьера через функцию-фикстуру"):
            for courier_data, courier_id, response in courier(courier_data):
                with allure.step("Проверяем успешное создание первого курьера"):
                    assert response.status_code == 201
                with allure.step("Генерируем новые данные, но используем тот же login"):
                    new_data = generate_courier_data()
                    new_data["login"] = courier_data["login"]
                with allure.step("Пробуем создать второго курьера с этим логином"):
                    response2 = requests.post(CREATE_COURIER, json=new_data)
                with allure.step("Проверяем, что возвращается ошибка о существовании курьера"):
                    assert response2.status_code == 409
                    assert ERROR_MESSAGES["courier_exists"] in response2.text
