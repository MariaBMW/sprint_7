# Шаблон заказа
ORDER_TEMPLATE = {
    "firstName": "Василиса",
    "lastName": "Прекрасная",
    "address": "Москва, Дворец Чудес, д.1",
    "metroStation": 1,
    "phone": "+79037778899",
    "rentTime": 4,
    "deliveryDate": "2025-10-26",
    "comment": "Не знакомлюсь",
    "color": []
}

# Перебор цветов для заказов
ORDER_COLORS = [
    ["BLACK"],
    ["GREY"],
    ["BLACK", "GREY"],
    []
]

# Тексты ошибок
ERROR_MESSAGES = {
    "courier_exists": "Этот логин уже используется. Попробуйте другой.",
    "no_data_create": "Недостаточно данных для создания учетной записи",
    "no_data_login":  "Недостаточно данных для входа",
    "not_found": "Учетная запись не найдена"
}