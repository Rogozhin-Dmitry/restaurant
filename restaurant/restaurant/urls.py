from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path("cooker/", include("cooker.urls")),
    path("waiter/", include("waiter.urls")),
    path("", include("homepage.urls")),

]
