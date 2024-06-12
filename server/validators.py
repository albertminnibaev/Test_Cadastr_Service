from rest_framework.serializers import ValidationError
import re
from django.utils.translation import gettext_lazy as _


class CadastralNumberValidator:
    """
    Проверка корректности ввода кадастрового номера.
    """

    def __init__(self, field):
        self.field = field
        self.number_valid = r'^\d{2}:\d{2}:\d{6,7}:\d+$'

    def __call__(self, value):
        tmp_value = dict(value).get(self.field)

        if not re.match(self.number_valid, tmp_value):
            raise ValidationError(_(
                'Кадастровый номер введен некорректно.'
                'Правильный формат: АА:ВВ:CCCCСCC:КК'
                'АА – код округа'
                'ВВ - код района'
                'CCCCCCС - код кадастрового квартала (состоит из 6 или 7 цифр)'
                'КК – номер объекта'
            ))


class LongitudeValidator:
    """
    Проверка корректности ввода долготы.
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_value = dict(value).get(self.field)

        if tmp_value is None:
            raise ValidationError(_(
                'Значение долготы не было передано в запросе'
            ))

        if not -180 <= tmp_value <= 180:
            raise ValidationError(_(
                'Некорректный ввод долготы (неверный формат)'
                'Введите долготу в диапазоне от -180 до 180'
            ))


class LatitudeValidator:
    """
    Проверка корректности ввода широты.
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_value = dict(value).get(self.field)

        if tmp_value is None:
            raise ValidationError(_(
                'Значение широты не было передано в запросе'
            ))

        if not -90 <= tmp_value <= 90:
            raise ValidationError(_(
                'Некорректный ввод широты (неверный формат)'
                'Введите широту в диапазоне от -90 до 90'
            ))
