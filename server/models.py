from django.db import models

NULLABLE = {"blank": True, "null": True}


class Request(models.Model):
    cadastral_number = models.CharField(max_length=50, verbose_name='кадастровый номер')
    latitude = models.DecimalField(max_digits=11, decimal_places=7, **NULLABLE, verbose_name='широта')
    longitude = models.DecimalField(max_digits=11, decimal_places=7, **NULLABLE, verbose_name='долгота')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания запроса')
    server_response = models.BooleanField(verbose_name='ответ сервера', **NULLABLE)

    def __str__(self):
        return f'Запрос №{self.id} ({self.cadastral_number}, {self.latitude}, {self.longitude})'

    class Meta:
        verbose_name = 'запрос'
        verbose_name_plural = 'запрос'
