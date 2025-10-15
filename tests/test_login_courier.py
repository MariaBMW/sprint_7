import pytest
import requests
import allure
from urls import LOGIN_COURIER, CREATE_COURIER
from utils import generate_random_string, delete_courier_by_id

@allure.epic("Курьеры")
@allure.feature("Логин курьера")
class TestLoginCourier:

    @allure.story("Курьер может авторизоваться")
    def test_login_courier_success(self, courier_data):
        """Успешная авторизация курьера"""
        with allure.step("Создаём курьера"):
            requests.post(CREATE_COURIER, data=courier_data)

        with allure.step("Пробуем авторизоваться"):
            response = requests.post(LOGIN_COURIER, data={
                "login": courier_data["login"],
                "password": courier_data["password"]
            })
            assert response.status_code == 200
            assert "id" in response.json()

        courier_id = response.json().get("id")
        with allure.step("Удаляем курьера (чистка)"):
            if courier_id:
                delete_courier_by_id(courier_id)

    @allure.story("Для авторизации нужны все поля")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_courier_empty_field(self, missing_field, courier_data):
        """Попытка авторизации с пустым обязательным полем"""
        with allure.step("Создаём курьера"):
            requests.post(CREATE_COURIER, data=courier_data)
        payload = {
            "login": courier_data["login"],
            "password": courier_data["password"]
        }
        payload[missing_field] = ""  
        with allure.step(f"Пробуем авторизоваться с пустым полем {missing_field}"):
            response = requests.post(LOGIN_COURIER, data=payload)
            assert response.status_code == 400
            assert "Недостаточно данных для входа" in response.text

        with allure.step("Удаляем курьера (чистка)"):
            courier_id = self._get_courier_id(courier_data)
            if courier_id:
                delete_courier_by_id(courier_id)

    @allure.story("Ошибка при неверном логине/пароле")
    def test_login_wrong_credentials(self, courier_data):
        """Неправильные логин/пароль -- 404"""
        with allure.step("Создаём курьера"):
            requests.post(CREATE_COURIER, data=courier_data)

        with allure.step("Пробуем неверный пароль"):
            response1 = requests.post(LOGIN_COURIER, data={
                "login": courier_data["login"], "password": "wrongpass"
            })
            assert response1.status_code == 404
            assert "Учетная запись не найдена" in response1.text

        with allure.step("Пробуем неверный логин"):
            response2 = requests.post(LOGIN_COURIER, data={
                "login": "nouser", "password": courier_data["password"]
            })
            assert response2.status_code == 404

        with allure.step("Удаляем курьера (чистка)"):
            courier_id = self._get_courier_id(courier_data)
            if courier_id:
                delete_courier_by_id(courier_id)

    @allure.story("Авторизация под несуществующим пользователем")
    def test_login_nonexistent_courier(self):
        """Неизвестный логин -- 404"""
        login = "nonexistent" + generate_random_string(10)
        with allure.step("Пробуем авторизоваться несуществующим курьером"):
            response = requests.post(LOGIN_COURIER, data={
                "login": login, "password": "nopass"
            })
            assert response.status_code == 404
            assert "Учетная запись не найдена" in response.text

    @allure.step("Получить ID курьера для удаления")
    def _get_courier_id(self, courier_data):
        login_resp = requests.post(LOGIN_COURIER, data={
            "login": courier_data["login"],
            "password": courier_data["password"]
        })
        return login_resp.json().get("id")
    