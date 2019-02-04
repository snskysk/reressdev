from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name = 'base'),
    path('hp/', views.hp, name = 'hp'),
    path('detail/', views.detail, name = 'detail'),
    path('mainhome/', views.mainhome, name = 'mainhome'),
    path('mainhome_after_login', views.mainhome_after_login, name = 'mainhome_after_login'),
    path('course', views.course, name = 'course'),
    path('teacher_search', views.teacher_search, name = 'teacher_search'),
    path('sirabasu', views.sirabasu, name = 'sirabasu'),
    path('course/<int:num>', views.course, name='course'),
    path('flush/', views.flush, name='flush'),
    path('inquiry', views.inquiry, name='inquiry'),
    path('more/', views.more, name='more'),
    path('pastdata/', views.pastdata, name='pastdata'),
    path('counter/', views.counter, name='counter'),
    path('sub_search/', views.sub_search, name='sub_search'),
    path('substitution/', views.substitution, name='substitution'),
    path('course_more/', views.course_more, name='course_more'),

]
