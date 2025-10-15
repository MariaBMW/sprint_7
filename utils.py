import random
import string
import requests
from urls import DELETE_COURIER

def generate_random_string(length=10):
    # Получаем строку заданной длины
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def delete_courier_by_id(courier_id):
    # Удаляем курьера по id через DELETE-запрос
    url = DELETE_COURIER.format(courier_id=courier_id)
    response = requests.delete(url)
    return response.status_code