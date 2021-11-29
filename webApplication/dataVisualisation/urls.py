from django.urls import path

from dataVisualisation import views

urlpatterns = [
    path('', views.update_database, name="test"),
]