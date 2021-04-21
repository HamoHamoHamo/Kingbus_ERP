from django.urls import path
from . import views

app_name = 'crudmember'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signup_terms/', views.signup_terms, name='signup_terms'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout')
]