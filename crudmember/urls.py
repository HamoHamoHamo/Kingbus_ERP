from django.urls import path
from . import views

app_name = 'crudmember'
urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('signup_terms', views.signup_terms, name='signup_terms'),
    path('welcome', views.welcome, name='welcome'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('reset/password', views.reset_password, name='reset_password'),
    path('profile', views.profile, name='profile'),
    # path('find_password/<str:uid64>/<str:token>/', views.pwchangeauth, name='pwchangeauth'),
    path('id-check', views.id_overlap_check, name="id_check"),
]
