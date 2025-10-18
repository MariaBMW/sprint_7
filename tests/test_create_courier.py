import pytest
import requests
import allure
from urls import CREATE_COURIER
from data import ERROR_MESSAGES


@allure.epic("Курьеры")
@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.title("Курьера можно создать")
    def test_create_courier_success(self, courier):
        courier_data, courier_id, response = courier
        with allure.step("Проверяем статус-код и флаг ok"):
            assert response.status_code == 201, "Неверный статус-код при создании курьера"
        
            with allure.step("Проверяем наличие флага ok"):
                response_json = response.json()
                assert "ok" in response_json, "Флаг ok отсутствует в ответе"
                assert response_json["ok"] is True, "Флаг ok не равен True"

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_two_same_couriers(self, courier):
        courier_data, _, _ = courier
        with allure.step("Пытаемся создать второго курьера с теми же данными"):
            response = requests.post(CREATE_COURIER, json=courier_data)
        with allure.step("Проверяем ошибку и текст ошибки"):
            assert response.status_code == 409
            assert ERROR_MESSAGES["courier_exists"] in response.text

    @allure.title("Не удаётся создать курьера без обязательных полей")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_field(self, missing_field, courier_data):
        """Создание курьера без обязательного поля должно вернуть ошибку"""
        data = courier_data.copy()
        data.pop(missing_field)
        with allure.step(f"Пробуем создать курьера без поля {missing_field}"):
            response = requests.post(CREATE_COURIER, json=data)
            assert response.status_code == 400
            assert ERROR_MESSAGES["no_data_create"] in response.text

    @allure.title("Создать курьера с существующим логином нельзя")
    def test_create_courier_with_existing_login(self, courier):
        courier_data, _, _ = courier
        with allure.step("Готовим другие данные, но тот же логин"):
            new_data = courier_data.copy()
            new_data['password'] = 'diffpass'
            new_data['firstName'] = 'diffname'
        with allure.step("Пытаемся создать такого курьера ещё раз"):
            response = requests.post(CREATE_COURIER, json=new_data)
        with allure.step("Проверяем ошибку и текст ошибки"):
            assert response.status_code == 409
            assert ERROR_MESSAGES["courier_exists"] in response.text