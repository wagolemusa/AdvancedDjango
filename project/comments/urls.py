from django.urls import path

from django.conf.urls import  url
from .views import (
	comment_thread,
	comment_delete,
	)

app_name = 'comments'
urlpatterns = [

  path('<int:id>/',comment_thread, name='thread'),
  	path('<int:id>/delete/', comment_delete, name='delete'),
]