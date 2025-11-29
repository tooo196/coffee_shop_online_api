from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Настройка Swagger документации
schema_view = get_schema_view(
	openapi.Info(
		title="Coffee Shop API",
		default_version='v1',
		description="API for Coffee Shop E-commerce",
		terms_of_service="https://www.google.com/policies/terms/",
		contact=openapi.Contact(email="contact@coffeeshop.local"),
		license=openapi.License(name="BSD License"),
	),
	public=True,
	permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
	# Админ-панель Django
	path('admin/', admin.site.urls),

	# Основные API endpoints
	path('api/', include('api.urls')),

	# Swagger документация
	path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
	path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Serving media files in development
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)