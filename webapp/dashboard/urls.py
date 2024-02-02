from django.urls import path

from . import views

urlpatterns = [
    path('', views.home),
    path('test/', views.test),
    path('achecker_evaluation/', views.achecker_evaluation),
    path('get_districts/', views.get_districts),
    # path('axe/', views.axe),
    # path('url2report/', views.url2report),
]
