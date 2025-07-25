from django.contrib import admin
from django.urls import path,include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("v1/api/user/",include("accounts.urls")),
    path("v1/api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("v1/api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
