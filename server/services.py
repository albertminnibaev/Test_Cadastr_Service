import random
import re

list_random = [True, False]


def server_random_response():
    """
    Функция для получения случайного ответа сервера
    """
    return random.choice(list_random)


def number_valid(value):
    number_valid_value = r'^\d{2}:\d{2}:\d{6,7}:\d+$'
    return re.match(number_valid_value, value)
