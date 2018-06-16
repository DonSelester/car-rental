from django.contrib import admin
from django.urls import path, re_path
from auto import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    # /car/id/
    re_path(r'^car/(?P<c_id>[0-9]+)/$', views.about_car, name='about_car'),
    # /bronirovanie/
    path('bronirovanie', views.rent_car, name='bronirovanie'),
    # /bronirovanie/id
    re_path(r'^bronirovanie/(?P<c_id>[0-9]+)/$', views.rent_car_def, name='bronirovanie_id'),
    # /add_car/
    path('add_car/', views.add_car, name='add_car'),
    # /login/
    path('login/', views.user_login, name='login'),
    # /logout/
    path('logout/', views.user_logout, name='logout'),
    # /stats/id
    re_path(r'^stats/(?P<c_id>[0-9]+)/$', views.stats_id, name='stats_id'),
    # /stats/
    path('stats/', views.stats, name='stats'),
    # /contr_infos/
    path('contr_infos/', views.contr_infos, name='contr_infos'),
]
