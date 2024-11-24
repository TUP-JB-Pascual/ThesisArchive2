from django.urls import path, include, re_path
from . import views
from django.views.static import serve

#USE ONLY ON DEVELOPMENT
from django.conf import settings
from django.conf.urls.static import static
#USE ONLY ON DEVELOPMENT


urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('publish_thesis/', views.ThesisPublishView.as_view(), name='thesis_publish'),
    path('thesis_list/', views.ThesisListView.as_view(), name='thesis_list'),
    path('thesis/<int:pk>', views.ThesisDetailView, name='thesis_detail'),
    path('thesis/update/<int:pk>', views.ThesisUpdateView, name='thesis_update'),
    path('thesis/<int:pk>/delete', views.ThesisDeleteView.as_view(), name='thesis_delete'),
    path('generate-pdf-url/<int:pk>', views.generate_temp_url, name='generate_temp_url'),
    path('temp/pdf/<str:url_key>', views.temp_url_redirect, name='temporary_url_redirect'),
    path('thesis/<int:pk>/request', views.ThesisRequestView, name='thesis_request'),
    path('thesis/request_list', views.ThesisRequestListView.as_view(), name='request_list'),
    path('thesis/request_list/<int:pk>', views.RequestDetailView, name='request_view'),
    path('thesis/request_list/<int:pk>/reject', views.RequestReject, name='request_reject'),
    path('thesis/<int:pk>/download', views.ThesisDownload, name='thesis_download'),
    path('download-pdf/<str:pdf>', views.ThesisDownload, name='download'),
    path('window-blur/<str:temp_url>', views.window_blur_method, name='window_blur_method'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]



#USE ONLY ON DEVELOPMENT
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#USE ONLY ON DEVELOPMENT
