from django.conf.urls import url
import views 

urlpatterns = [
    url(r'^book_list/$', views.book_list),
    url(r'^cloud_tag/$', views.get_tags),
]
