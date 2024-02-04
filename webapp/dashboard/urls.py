from django.urls import path

from . import views

urlpatterns = [
    path('', views.home),
    path('districts/', views.districts),
    path('achecker_evaluation/', views.achecker_evaluation),
    # path('axe/', views.axe),
    # path('url2report/', views.url2report),
    # path('get_districts/', views.get_districts),
]
