from django.conf.urls import url
import views 

urlpatterns = [
    url(r'^book_list/$', views.book_list),
    url(r'^cloud_tag/$', views.get_tags),
    url(r'simple_cloud_tag/$', views.get_simple_tags),
]
