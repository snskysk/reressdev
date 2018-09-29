from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('get/', views.get, name = 'get'),
    path('deteil/', views.deteil, name = 'deteil'),
    path('detail/', views.detail, name = 'detail')
]
