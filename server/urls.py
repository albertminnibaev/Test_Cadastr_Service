from django.urls import path

from server.apps import ServerConfig
from server.views import QueryAPIView, PingAPIView, ResultAPIView, HistoryListAPIView, HistoryListNumberAPIView

app_name = ServerConfig.name

urlpatterns = [
    path('query', QueryAPIView.as_view(), name='query'),
    path('result', ResultAPIView.as_view(), name='result'),
    path('ping', PingAPIView.as_view(), name='ping'),
    path('history', HistoryListAPIView.as_view(), name='history'),
    path('history_number', HistoryListNumberAPIView.as_view(), name='history_number'),
]
