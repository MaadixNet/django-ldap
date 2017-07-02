from django.conf.urls import url 

from . import views

urlpatterns = [ 
    url(r'^notifications/', views.sender_email, name='sender_email_action'),
]

