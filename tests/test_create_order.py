import pytest
import requests
import allure
from urls import CREATE_ORDER, CANCEL_ORDER

def cancel_order(track):
    """Отмена заказа по треку через query params, как требует API"""
    with allure.step(f"Отмена заказа track={track}"):
        response = requests.put(CANCEL_ORDER, params={"track": track})
        allure.attach(str(response.text), "Ответ отмены", allure.attachment_type.TEXT)
        assert response.status_code == 200, f"Ошибка отмены: {response.status_code}, {response.text}"

@allure.epic("Заказы")
@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.story("Параметризация по цветам заказа")
    @pytest.mark.parametrize("colors", [
        (["BLACK"]),
        (["GREY"]),
        (["BLACK", "GREY"]),
        ([])
    ])
    def test_create_order_colors(self, order_data, colors):
        """Создание заказа с разными вариантами цвета"""
        order_data_mod = order_data.copy()
        order_data_mod['color'] = colors

        track = None
        try:
            with allure.step(f"Пробуем создать заказ с цветами {colors}"):
                response = requests.post(CREATE_ORDER, json=order_data_mod)
                with allure.step("Проверяем успешность создания заказа"):
                    assert response.status_code == 201, f"status_code: {response.status_code}, тело: {response.text}"
                    track = response.json().get("track")
                    assert track is not None, f"Нет трека заказа в ответе: {response.text}"
        finally:
            if track:
                cancel_order(track)