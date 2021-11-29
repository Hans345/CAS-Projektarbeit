from django.urls import path

from dataVisualisation import views

urlpatterns = [
    path('', views.test, name="test"),
]