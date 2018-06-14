from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^register/', views.register, name='register'),
    url(r'^api/(?P<pk>[0-9]+)/$', views.ListStatusView.as_view())
]
