from django.urls import path
from . import views
from .views import force_fix_images


urlpatterns =[
    path('',views.home,name='home'),
    path('projects/<slug:slug>/',views.project_detail,name='project_detail'),
    path('services/',views.services,name='services'),
    path('skills/',views.skills,name='skills'),
    path('projects/',views.projects,name='projects'),
    path('contact/',views.contact,name='contact'),
    path('force-fix-images/', force_fix_images, name='force_fix_images'),
]