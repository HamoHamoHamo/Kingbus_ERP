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
    path('change/id', views.change_id, name="change_id"),
    path('change/password', views.change_password, name="change_password"),
    path('setting', views.CategoryList.as_view(), name="setting"),
    path('setting/create', views.setting_create, name="setting_create"),
    path('setting/delete', views.setting_delete, name="setting_delete"),
    path('setting/client', views.ClientList.as_view(), name="setting_client"),
    path('setting/client/create', views.setting_client_create, name="setting_client_create"),
    path('setting/salary/meal', views.salary_meal, name="salary_meal"),
    path('setting/salary/date', views.salary_date, name="salary_date"),
]
