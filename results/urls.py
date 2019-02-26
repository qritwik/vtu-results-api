from django.conf.urls import url
from results import views

urlpatterns = [
    url(r'^vtu/$', views.get_result_post),
    url(r'^(?P<usn>[\w\-]+)/(?P<sem>[\w\-]+)/$', views.get_result_get),
]
