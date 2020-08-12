from django.urls import path
from .views import *

urlpatterns = [
    path('', index_view)
]

app_name = 'search'
