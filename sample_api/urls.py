from django.urls import path
from .views import get_advertising_data, import_db

urlpatterns = [
    path('api/sample/', get_advertising_data),
    path('import_db/', import_db),
]
