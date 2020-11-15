from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    path("",views.home,name="home"),
    path("prefecture/",views.prefecture,name="prefecture"),
    path("prefecture/<str:pref>/",views.prefectures,name="prefectures")
]
