from django.urls import path
from . import views

#USE ONLY ON DEVELOPMENT
from django.conf import settings
from django.conf.urls.static import static
#USE ONLY ON DEVELOPMENT


urlpatterns = [
    path('registration/', views.UserRegisterView, name='user_registration'),
    path('verify-email/<str:uidb64>/<str:token>/', views.VerifyEmail, name='verify_email'),
    #path('login/', views.UserLoginView.as_view(), name='login'),
]
