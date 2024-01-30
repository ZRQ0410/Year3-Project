from django.urls import path

from . import views

urlpatterns = [
    path('', views.home),
    path('other/', views.other),
    path('achecker_evaluation/', views.achecker_evaluation),
    # path('axe/', views.axe),
    path('url2report/', views.url2report),
]
