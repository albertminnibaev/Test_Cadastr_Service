from datetime import datetime

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.utils.translation import gettext_lazy as _

from server.models import Request
from users.management.commands.ccsu import Command
from users.models import User
from server.tasks import server_response


class RequestTestCase(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(email='test@test.com', first_name='aaa', last_name='dadasd',
                                        password='test')
        self.client.force_authenticate(user=self.user)

        self.request = Request.objects.create(
            cadastral_number="11:11:111111:111",
            latitude=11,
            longitude=111
        )

    def test_create_1(self):
        """ Тестирование создания запроса при вводе верных данных """

        data = {
            'cadastral_number': self.request.cadastral_number,
            'latitude': self.request.latitude,
            'longitude': self.request.longitude
        }
        response = self.client.post(
            '/query',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {'message': _(f'Запрос зарегистрирован. Номер вашего обращения {self.request.id + 1}')}
        )

        self.assertTrue(
            Request.objects.all().exists()
        )

        self.assertEqual(
            self.request.__str__(),
            f'Запрос №{self.request.id} ({self.request.cadastral_number}, {self.request.latitude}, '
            f'{self.request.longitude})'
        )

    def test_create_2(self):
        """ Тестирование создания запроса при вводе неверных данных,
         не предан кадастровый номер"""

        data = {
            'latitude': "10",
            'longitude': "1"
        }

        response = self.client.post(
            '/query',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {'cadastral_number': ['This field is required.']}
        )

    def test_create_3(self):
        """ Тестирование создания запроса при вводе неверных данных,
         не верно введен кадастровый номер"""

        data = {
            'cadastral_number': "11:11:1111:11",
            'latitude': "111",
            'longitude': "111"
        }

        response = self.client.post(
            '/query',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Кадастровый номер введен некорректно.Правильный формат: '
                                  'АА:ВВ:CCCCСCC:ККАА – код округаВВ - код районаCCCCCCС - '
                                  'код кадастрового квартала (состоит из 6 или 7 цифр)КК – '
                                  'номер объекта',
                                  'Некорректный ввод широты (неверный формат)Введите '
                                  'широту в диапазоне от -90 до 90']}
        )

    def test_create_4(self):
        """ Тестирование создания запроса при вводе неверных данных,
         не верно введены данные широты"""

        data = {
            'cadastral_number': "11:11:111111:111",
            'latitude': "111",
            'longitude': "1"
        }

        response = self.client.post(
            '/query',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Некорректный ввод широты (неверный формат)'
                                  'Введите широту в диапазоне от -90 до 90']}
        )

    def test_create_5(self):
        """ Тестирование создания запроса при вводе неверных данных,
         не верно введены данные долготы"""

        data = {
            'cadastral_number': "11:11:111111:111",
            'latitude': "11",
            'longitude': "1111"
        }

        response = self.client.post(
            '/query',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Некорректный ввод долготы (неверный формат)'
                                  'Введите долготу в диапазоне от -180 до 180']}
        )

    def test_create_6(self):
        """ Тестирование создания запроса при вводе неверных данных,
         не передано значение широты"""

        data = {
            'cadastral_number': "11:11:111111:111",
            'longitude': "1"
        }

        response = self.client.post(
            '/query',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Значение широты не было передано в запросе']}
        )

    def test_create_7(self):
        """ Тестирование создания запроса при вводе неверных данных,
         не передано значение долготы"""

        data = {
            'cadastral_number': "11:11:111111:111",
            'latitude': "11"
        }

        response = self.client.post(
            '/query',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Значение долготы не было передано в запросе']}
        )

    def test_result_1(self):
        """ Тестирование получения результата запроса """

        data = {
            'number_request': self.request.id,
        }

        response = self.client.post(
            '/result',
            data=data
        )

        result = self.request.server_response

        if result:
            self.assertEqual(
                response.status_code,
                status.HTTP_200_OK
            )

            self.assertEqual(
                response.json(),
                {"message": _("Статус запроса: Успешно")}
            )

        elif result is None:
            self.assertEqual(
                response.status_code,
                status.HTTP_200_OK
            )

            self.assertEqual(
                response.json(),
                {"message": _("Статус запроса: Запрос еще не обработан, ожидает ответа сервера")}
            )

        else:
            self.assertEqual(
                response.status_code,
                status.HTTP_400_BAD_REQUEST
            )

            self.assertEqual(
                response.json(),
                {"message": _("Статус запроса: Неуспешно")}
            )

    def test_result_2(self):
        """ Тестирование получения результата запроса при некорретном вводе номера запроса """

        data = {
            'number_request': '5',
        }

        response = self.client.post(
            '/result',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {"message": _("Запроса с номером 5 не существует")}
        )

    def test_result_3(self):
        """ Тестирование получения результата запроса при некорректном вводе кадастрового номера """

        data = {
            'number_request': 'qqqqq',
        }

        response = self.client.post(
            '/result',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {"message": _("Некорректно введен номер вашего обращения")}
        )

    def test_ping(self):

        """ Тестирование получения информации о том, что сервер запущен """

        response = self.client.get(
            '/ping'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {"message": 'Сервер запущен'}
        )

    def test_history_number_1(self):

        """ Тестирование получения истории запросов по кадастровому номеру при вводе верных данных """

        data = {
            'cadastral_number': self.request.cadastral_number,
        }

        response = self.client.post(
            '/history_number',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {"message": [{'cadastral_number': '11:11:111111:111',
                          'created_at': datetime.strftime(self.request.created_at, '%Y-%m-%dT%H:%M:%S.%fZ'),
                          'id': self.request.id,
                          'latitude': str(format(self.request.latitude, ".7f")),
                          'longitude': str(format(self.request.longitude, ".7f")),
                          'server_response': self.request.server_response}]}
        )

    def test_history_number_2(self):

        """ Тестирование получения истории запросов по несуществующему кадастровому номеру"""

        data = {
            'cadastral_number': '11:11:111111:999',
        }

        response = self.client.post(
            '/history_number',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {"message": _('По кадастровому номеру 11:11:111111:999 запросы не найдены')}
        )

    def test_history_number_3(self):

        """ Тестирование получения истории запросов, когда кадастровый номер введен некорректно"""

        data = {
            'cadastral_number': '11:11:111:999',
        }

        response = self.client.post(
            '/history_number',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {"message": _('Кадастровый номер введен некорректно.Правильный формат: '
                          'АА:ВВ:CCCCСCC:ККАА – код округаВВ - код районаCCCCCCС - код '
                          'кадастрового квартала (состоит из 6 или 7 цифр)КК – номер объекта')}
                        )

    def test_history_number_4(self):

        """ Тестирование получения истории запросов, когда кадастровый номер введен некорректно"""

        data = {}

        response = self.client.post(
            '/history_number',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {"message": _('Кадастровый номер не был передан в запросе')}
        )

    def test_history_1(self):

        """ Тестирование получения истории всех запросов """

        response = self.client.get(
            '/history'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data['results']),
            1
        )

    def test_tasks(self):

        """ Тестирование задачи Celery """

        request_obj = Request.objects.create(
            cadastral_number="22:22:222222:222",
            latitude=1,
            longitude=1
        )

        result = server_response.delay(request_obj.id)

        self.assertEqual(
            result.state,
            'PENDING'
        )

    def test_ccsu(self):

        """ Тестирование создания суперпользователя """

        self.assertTrue(
            Command()
        )
