from django.urls import path
from . import views

#USE ONLY ON DEVELOPMENT
from django.conf import settings
from django.conf.urls.static import static
#USE ONLY ON DEVELOPMENT


urlpatterns = [
    path('registration/', views.UserRegisterView.as_view(), name='user_registration'),
    #path('login/', views.UserLoginView.as_view(), name='login'),
]

#USE ONLY ON DEVELOPMENT
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#USE ONLY ON DEVELOPMENT
