from django.urls import path
from . import views

app_name = 'homepage'

urlpatterns = [
    path('', views.home, name='homepage'),
    path('payment', views.payment, name='payment'),
    path('question', views.question, name='question'),
    path('faq', views.faq, name='faq'),
    # 가격정책,
    # 가입문의
    # faq
    # path('product/trp/', views.trp, name='trp'),
    # path('product/dispatch/', views.dispatch, name='dispatch'),
    # path('product/servicelink/', views.servicelink, name='servicelink'),
    # path('product/web/', views.web, name='web'),
    # path('product/customizing/', views.customizing, name='customizing'),
    # path('business/kingbus/', views.kingbus, name='kingbus'),
    # path('business/driver/', views.driver, name='driver'),
    # path('register/check/', views.check, name='check'),
    # path('register/consulting/', views.consulting, name='consulting'),
    
]

