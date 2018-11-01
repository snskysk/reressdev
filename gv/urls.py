from django.urls import path
from . import views

urlpatterns = [
    path('hp/', views.hp, name = 'hp'),
    path('info/', views.info, name = 'info'),
    path('', views.index, name = 'index'),
    path('get/', views.get, name = 'get'),
    path('detail/', views.detail, name = 'detail'),
    path('mainhome/', views.mainhome, name = 'mainhome'),
    path('mainhome_after_login', views.mainhome_after_login, name = 'mainhome_after_login'),
    path('review/', views.review, name = 'review'),
    path('shop_search/', views.shop_search, name = 'shop_search'),
        #path('to_kkk/', views.to_kkk, name = 'to_kkk'),
    path('course', views.course, name = 'course'),
    path('teacher_search', views.teacher_search, name = 'teacher_search'),
    path('sirabasu', views.sirabasu, name = 'sirabasu'),
    path('course/<int:num>', views.course, name='course'),
    path('flush/', views.flush, name='flush'),
    path('inquiry', views.inquiry, name='inquiry'),

]
