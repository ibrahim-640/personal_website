from django.urls import path
from . import views
from .views import force_fix_images


urlpatterns =[
    path('',views.home,name='home'),
    path('packages/',views.packages,name='packages'),
    path('about/',views.about,name='about'),
    path('process/',views.process,name='process'),
    path('contact/',views.contact,name='contact'),
    path('force-fix-images/', force_fix_images, name='force_fix_images'),
]