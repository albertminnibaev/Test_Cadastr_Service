import random
import time

from celery import shared_task

from server.models import Request
from server.services import server_random_response


@shared_task
def server_response(id):
    """
    Асинхронная функция, получает на вход id запроса, получает объект запроса из базы данных и
    записывает в поле объекта 'server_response' ответ сервера (True/False),
    имитирует работу сервера создавая рандоиную задержку по времени до 60 секунд
    :param id: id запроса
    :return: None
    """

    time.sleep(random.randint(1, 60))

    req_obj = Request.objects.get(id=id)
    req_obj.server_response = server_random_response()
    req_obj.save()
