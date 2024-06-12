from drf_yasg import openapi
from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING
from drf_yasg.utils import swagger_auto_schema
from django.utils.translation import gettext_lazy as _
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from server.models import Request
from server.paginators import RequestPagination
from server.serializers import RequestSerializer
from server.services import number_valid
from server.tasks import server_response


class QueryAPIView(APIView):
    """
    Класс представления для получения запроса.
    Необходимо передать в параметрах кадастровый номер (cadastral_number), широту (latitude) и долготу (longitude).
    Возвращает номер запроса, который нужно передать по адресу “/result" для получения результата
    """

    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    @swagger_auto_schema(request_body=Schema(type=TYPE_OBJECT,
                                             required=['cadastral_number', 'latitude', 'longitude'],
                                             properties={'cadastral_number': Schema(type=TYPE_STRING),
                                                         'latitude': Schema(type=TYPE_STRING),
                                                         'longitude': Schema(type=TYPE_STRING)
                                                         }))
    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            # Сохраняем объект запроса в базе данных
            serializer.save()

            # Получаем id объекта запроса
            id = serializer.instance.id

            server_response.delay(id)

            return Response({'message': _(f'Запрос зарегистрирован. Номер вашего обращения {id}')},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'message': _('Введены неверные данные')}, status=status.HTTP_400_BAD_REQUEST)


class ResultAPIView(APIView):
    """
    Класс представления для получения результата запроса.
    Необходимо передать в параметрах номер запроса id запроса (number_request).
    Возвращает результат запроса.
    """

    @swagger_auto_schema(request_body=Schema(type=TYPE_OBJECT,
                                             required=['number_request'],
                                             properties={'number_request': Schema(type=TYPE_STRING)
                                                         }))
    def post(self, request):
        #  Получение данных из запроса
        number_request = request.data.get('number_request')
        try:
            req_obj = Request.objects.filter(id=number_request).first()
        except ValueError:
            return Response({"message": _("Некорректно введен номер вашего обращения")},
                            status=status.HTTP_400_BAD_REQUEST)

        if req_obj:
            result = req_obj.server_response
            if result:
                return Response({"message": _("Статус запроса: Успешно")},
                                status=status.HTTP_200_OK)
            elif result is None:
                return Response({"message": _("Статус запроса: Запрос еще не обработан, ожидает ответа сервера")},
                                status=status.HTTP_200_OK)
            else:
                return Response({"message": _("Статус запроса: Неуспешно")},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': _(f"Запроса с номером {number_request} не существует")},
                            status=status.HTTP_400_BAD_REQUEST)


class PingAPIView(APIView):
    """
    Класс представления для получения информации о том, что сервер запущен.
    """

    @swagger_auto_schema(responses={
        200: openapi.Response(description="Сервер запущен")
    },
    )
    def get(self, request):
        return Response({'message': 'Сервер запущен'}, status=status.HTTP_200_OK)


class HistoryListNumberAPIView(APIView):
    """
    Класс представления для получения истории запросов, принадлежащих только одному кадастровому номеру.
    Необходимо передать в параметрах кадастровый номер (cadastral_number).
    Возвращает историю запросов.
    """

    @swagger_auto_schema(request_body=Schema(type=TYPE_OBJECT,
                                             required=['cadastral_number'],
                                             properties={'cadastral_number': Schema(type=TYPE_STRING)
                                                         }))
    def post(self, request):
        #  Получение данных из запроса
        cadastral_number = request.data.get('cadastral_number')

        if cadastral_number is not None:
            if number_valid(cadastral_number):
                #  Получаем историю запросов из базы данных по кадастровому номеру
                queryset = Request.objects.filter(cadastral_number=cadastral_number).all()
                if queryset:
                    serializer_for_queryset = RequestSerializer(
                        instance=queryset,  # Передаём набор записей
                        many=True  # Указываем, что на вход подаётся именно набор записей
                    )
                    return Response({'message': serializer_for_queryset.data},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({'message': _(f'По кадастровому номеру {cadastral_number} запросы не найдены')},
                                    status=status.HTTP_200_OK)
            else:
                return Response({'message': _(
                    'Кадастровый номер введен некорректно.'
                    'Правильный формат: АА:ВВ:CCCCСCC:КК'
                    'АА – код округа'
                    'ВВ - код района'
                    'CCCCCCС - код кадастрового квартала (состоит из 6 или 7 цифр)'
                    'КК – номер объекта'
                )},
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': _('Кадастровый номер не был передан в запросе')},
                            status=status.HTTP_400_BAD_REQUEST)


class HistoryListAPIView(generics.ListAPIView):
    """
    Класс представления для получения истории всех запросов
    """
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    pagination_class = RequestPagination
