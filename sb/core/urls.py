
from django.urls import path
from . import views

urlpatterns = [
    # home page route
    path('',views.home, name='home'),
]
