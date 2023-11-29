from django.urls import path
from . import views as my_views
from django.contrib.auth import views as auth_views


urlpatterns = [

    #path('authentication/', auth_views.LoginView.as_view(template_name='auth/authentication.html'),
    # name='authentication-url'),
]