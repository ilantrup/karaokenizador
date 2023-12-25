from django.urls import path

from . import views



urlpatterns = [
    path("", views.index.as_view(), name="index"),
    path('get-video/', views.get_video, name='get_video'),

]
