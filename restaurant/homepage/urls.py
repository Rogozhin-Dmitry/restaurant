from django.urls import path

from homepage.views import Home

urlpatterns = [
    path("", Home.as_view(), name='home'),
]
