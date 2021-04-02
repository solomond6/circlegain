from django.conf.urls import url
from . import views
# from django.urls import path
# from .views import users_list, users_detail

app_name = 'exchange'

urlpatterns = [
	url(r'^$', views.ping, name='index'),
	url(r'^spendings/$',  views.ExchangeRate.as_view(), name='spendings')   
]