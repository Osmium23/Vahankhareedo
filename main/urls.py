from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('search_vehicle/', views.search_vehicle, name='search_vehicle'),
    # path('bike/', views.bike, name='bike'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    path('favourites/', views.favourites, name='favourites'),
    path('vehicle/', views.vehicle, name='vehicle'),
    path('add_fav/', views.add_fav, name='add_fav'),
    path('remove_fav/', views.remove_fav, name='remove_fav'),
    path('add_review/', views.add_review, name='add_review'),
    path('about', views.about, name='about')
]
