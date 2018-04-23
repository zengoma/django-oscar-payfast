from django.conf.urls import url
from payfast import views

urlpatterns = [
    url(r'^redirect/', views.redirect_view, name='payfast-redirect'),
    url(r'^notify/', views.notify_view, name='payfast-notify'),
    url(r'^cancel/', views.cancel_view, name='payfast-cancel')
]
