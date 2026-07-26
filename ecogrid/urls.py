"""
Root URL config.

Everything lives under /api/ so it lines up with the frontend's
VITE_API_BASE_URL=/api setting (see src/lib/api/client.ts).
"""

# from django.contrib import admin
# from django.urls import include, path

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("users.urls")),
    path("api/", include("buildings.urls")),
    path("api/", include("analytics.urls")),
    path("api/", include("ai.urls")),
    path("api/", include("iot.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)