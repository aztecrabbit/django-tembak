from django.urls import path
from django.views.generic import RedirectView

from . import views


app_name = 'tembak'

urlpatterns = [
    path('', RedirectView.as_view(url='xl/', permanent=True)),
    path('xl/', views.xl_index, name='xl-index'),
    path('xl/request-otp', views.xl_request_otp, name='xl-request-otp'),
    path('xl/signin', views.xl_signin, name='xl-signin'),
    path('xl/signout', views.xl_signout, name='xl-signout'),
]
