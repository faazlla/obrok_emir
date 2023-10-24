from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('news/', views.news, name='news'),
    path('donation/', views.donation, name='donation'),
    path('get_restaurants/<int:city_id>/', views.get_restaurants, name='get_restaurants'),
    path('donation_user/', views.donation_user, name='donation_user'),
    path('collaboration/', views.collaboration, name='collaboration'),
    path('user_restaurants/', views.user_restaurants, name='user_restaurants'),
    path('edit_restaurant/<int:restaurant_id>/', views.edit_restaurant, name='edit_restaurant'),
    path('myprofile/', views.my_profile, name='my_profile'),
    path('search/', views.search_profile, name='search_profile'),
    path('<str:username>/', views.user_profile, name='user_profile'),
]