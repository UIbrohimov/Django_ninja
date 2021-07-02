from django.contrib import admin
from django.urls import include, path

from blogs.api import api as blogs_api

from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("newspaper/", api.urls),
    path("blog/", blogs_api.urls),
    path("drf/", include("drf.urls")),
    path("", include("apinja.urls")),
]
