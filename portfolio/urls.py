from django.urls import path
from . import views


urlpatterns = [
    
    path('', views.base, name='base'),
    path('home/', views.home, name='home'),
    # path('about/', views.about, name='about'),
    # path('gallery/', views.gallery, name='gallery'),
    # path('contact/', views.contact, name='contact'),

]
