from django.urls import path
from . import views

urlpatterns = [
    path('user-messages', views.store_message, name='user-message'),
]