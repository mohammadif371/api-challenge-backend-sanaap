from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Document Management System API",
        default_version='v1',
        description="""
        Document Management System (DMS) API
        
        ## Authentication
        Use JWT token in header: `Authorization: Bearer <token>`
        
        ## Roles
        - **admin**: Full access
        - **editor**: Upload and update documents
        - **viewer**: Read only
        """,
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API
    path('api/', include('users.urls')),
    path('api/', include('documents.urls')),
    path('api/', include('audit.urls')),

    # Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
]
