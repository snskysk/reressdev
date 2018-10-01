from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('get/', views.get, name = 'get'),
    path('deteil/', views.deteil, name = 'deteil'),
    path('detail/', views.detail, name = 'detail'),
    path('mainhome/', views.mainhome, name = 'mainhome'),
    path('mainhome_after_login', views.mainhome_after_login, name = 'mainhome_after_login'),
    path('hp/', views.hp, name = 'hp')
]
