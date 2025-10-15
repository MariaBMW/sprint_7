import pytest
import requests
import allure
from urls import CREATE_COURIER, LOGIN_COURIER
from utils import delete_courier_by_id

@allure.epic("Курьеры")
@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.story("Курьера можно создать")
    def test_create_courier_success(self, courier_data):
        """Проверяем успешное создание курьера"""
        with allure.step("Создаём курьера"):
            response = requests.post(CREATE_COURIER, data=courier_data)
            assert response.status_code == 201
            assert response.json().get("ok") is True

        with allure.step("Удаляем созданного курьера (чистка)"):
            courier_id = self._get_courier_id(courier_data)
            if courier_id:
                delete_courier_by_id(courier_id)

    @allure.story("Нельзя создать двух одинаковых курьеров")
    def test_create_two_same_couriers(self, courier_data):
        """Два одинаковых курьера создать нельзя"""
        with allure.step("Создаём первого курьера"):
            res1 = requests.post(CREATE_COURIER, data=courier_data)
            assert res1.status_code == 201

        with allure.step("Пробуем создать второго с теми же данными"):
            res2 = requests.post(CREATE_COURIER, data=courier_data)
            assert res2.status_code == 409
            assert "Этот логин уже используется" in res2.text

        with allure.step("Удаляем курьера (чистка)"):
            courier_id = self._get_courier_id(courier_data)
            if courier_id:
                delete_courier_by_id(courier_id)

    @allure.story("Обязательные поля при создании курьера")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_field(self, missing_field, courier_data):
        """Создание курьера без обязательного поля должно вернуть ошибку"""
        data = courier_data.copy()
        data.pop(missing_field)
        with allure.step(f"Пробуем создать курьера без поля {missing_field}"):
            response = requests.post(CREATE_COURIER, data=data)
            assert response.status_code == 400
            assert "Недостаточно данных для создания учетной записи" in response.text

    @allure.story("Создание с существующим логином -- ошибка")
    def test_create_courier_with_existing_login(self, courier_data):
        """Создание с занятым логином не допускается"""
        with allure.step("Создаём первого курьера"):
            resp1 = requests.post(CREATE_COURIER, data=courier_data)
            assert resp1.status_code == 201

        with allure.step("Пробуем создать второго с тем же логином, но разными другими полями"):
            new_data = courier_data.copy()
            new_data['password'] = 'diffpass'
            new_data['firstName'] = 'diffname'
            resp2 = requests.post(CREATE_COURIER, data=new_data)
            assert resp2.status_code == 409

        with allure.step("Удаляем курьера (чистка)"):
            courier_id = self._get_courier_id(courier_data)
            if courier_id:
                delete_courier_by_id(courier_id)

    @allure.step("Получить ID курьера по данным для логина")
    def _get_courier_id(self, courier_data):
        login_resp = requests.post(LOGIN_COURIER, data={
            "login": courier_data["login"],
            "password": courier_data["password"]
        })
        return login_resp.json().get("id")