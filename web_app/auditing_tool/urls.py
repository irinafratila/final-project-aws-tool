from django.urls import path
from . import views

# urls that go to different views

urlpatterns = [
    path("index/", views.index, name='index'),
    path("list_page/", views.list_page, name='list_page'),
    path("v1/", views.v1, name='v1'),
    path("", views.home, name='home')
]