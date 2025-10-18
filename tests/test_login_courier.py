import pytest
import requests
import allure
from urls import LOGIN_COURIER
from helpers import generate_nonexistent_login, generate_courier_data
from data import ERROR_MESSAGES

@allure.epic("Курьеры")
@allure.feature("Логин курьера")
class TestLoginCourier:

    @allure.title("Курьер может авторизоваться по логину и паролю")
    def test_login_courier_success(self, courier):
        courier_data = generate_courier_data()
        for courier_data, _, _ in courier(courier_data):
            with allure.step("Пытаемся залогиниться этим курьером"):
                response = requests.post(LOGIN_COURIER, json={
                    "login": courier_data["login"],
                    "password": courier_data["password"]
                })
            with allure.step("Проверяем ответ сервера — статус 200 и есть id"):
                assert response.status_code == 200
                assert "id" in response.json()

    @allure.title("Для авторизации нужны все обязательные поля")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_courier_empty_field(self, missing_field, courier):
        courier_data = generate_courier_data()
        for courier_data, _, _ in courier(courier_data):
            with allure.step(f"Готовим данные с пустым обязательным полем {missing_field}"):
                payload = {
                    "login": courier_data["login"],
                    "password": courier_data["password"]
                }
                payload[missing_field] = ""
            with allure.step(f"Пробуем авторизоваться с пустым {missing_field}"):
                response = requests.post(LOGIN_COURIER, json=payload)
            with allure.step("Проверяем, что появилась ошибка и нужный текст"):
                assert response.status_code == 400
                assert ERROR_MESSAGES["no_data_login"] in response.text

    @allure.title("Ошибка, если неверный логин/пароль")
    def test_login_wrong_credentials(self, courier):
        courier_data = generate_courier_data()
        for courier_data, _, _ in courier(courier_data):
            with allure.step("Пробуем залогиниться с верным логином и неверным паролем"):
                response1 = requests.post(LOGIN_COURIER, json={
                    "login": courier_data["login"],
                    "password": "wrongpass"
                })
            with allure.step("Проверяем статус 404 и текст ошибки"):
                assert response1.status_code == 404
                assert ERROR_MESSAGES["not_found"] in response1.text
            with allure.step("Пробуем залогиниться с неверным логином и верным паролем"):
                response2 = requests.post(LOGIN_COURIER, json={
                    "login": "nouser",
                    "password": courier_data["password"]
                })
            with allure.step("Проверяем статус 404 и текст ошибки"):
                assert response2.status_code == 404
                assert ERROR_MESSAGES["not_found"] in response2.text

    @allure.title("Авторизация несуществующим пользователем - ошибка")
    def test_login_nonexistent_courier(self):
        with allure.step("Генерируем данные для несуществующего пользователя"):
            login = generate_nonexistent_login()
        with allure.step("Пытаемся залогиниться несуществующим пользователем"):
            response = requests.post(LOGIN_COURIER, json={
                "login": login,
                "password": "nopass"
            })
        with allure.step("Проверяем статус 404 и текст ошибки"):
            assert response.status_code == 404
            assert ERROR_MESSAGES["not_found"] in response.text