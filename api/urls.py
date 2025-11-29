from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
	CategoryViewSet, ProductViewSet, OrderViewSet,
	ReviewViewSet, UserRegistrationView, UserProfileView
)

# Автоматическая генерация URL для ViewSets
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
	# Автоматически сгенерированные URLs для ViewSets
	path('', include(router.urls)),

	# Authentication endpoints
	path('auth/register/', UserRegistrationView.as_view(), name='register'),
	path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),      # Получение JWT
	path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),     # Обновление JWT
	path('auth/profile/', UserProfileView.as_view(), name='user_profile'),             # Профиль пользователя
]