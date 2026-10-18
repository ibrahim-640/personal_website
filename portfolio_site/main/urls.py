from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('packages/', views.packages, name='packages'),
    path('process/', views.process, name='process'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
]