from django.urls import path
from . import views

#USE ONLY ON DEVELOPMENT
from django.conf import settings
from django.conf.urls.static import static
#USE ONLY ON DEVELOPMENT


urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('publish_thesis/', views.ThesisPublishView.as_view(), name='thesis_publish'),
    path('thesis_list/', views.ThesisListView.as_view(), name='thesis_list'),
    path('thesis/<int:pk>', views.ThesisDetailView.as_view(), name='thesis_detail'),
    path('thesis/update/<int:pk>', views.ThesisUpdateView, name='thesis_update'),
    #path('thesis/update/<int:pk>', views.ThesisUpdateView.as_view(), name='thesis_update'),
    path('thesis/<int:pk>/delete', views.ThesisDeleteView.as_view(), name='thesis_delete'),
]

#USE ONLY ON DEVELOPMENT
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#USE ONLY ON DEVELOPMENT
