from xml.etree.ElementInclude import include
from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.SignUpView, name='signup'),
    path('app', views.AppView.as_view(), name='app'),
    path('<str:username>', views.AppView.as_view(), name='chat'),
    path('error', views.Error, name='error'),
]