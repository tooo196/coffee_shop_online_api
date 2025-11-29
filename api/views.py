from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Avg, Count
from .models import Category, Product, Order, Review
from .serializers import (
	CategorySerializer, ProductSerializer, OrderSerializer,
	ReviewSerializer, UserRegisterSerializer, UserSerializer
)
from .permissions import IsOwnerOrReadOnly

class CategoryViewSet(viewsets.ModelViewSet):
	"""
	ViewSet для категорий товаров.
	"""
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	permission_classes = [AllowAny]
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ['name']
	ordering_fields = ['name', 'created_at']

class ProductViewSet(viewsets.ModelViewSet):
	"""
	ViewSet для товаров.
	"""
	queryset = Product.objects.filter(is_available=True)
	serializer_class = ProductSerializer
	permission_classes = [AllowAny]
	filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
	filterset_fields = ['category', 'roast_level', 'is_available']
	search_fields = ['name', 'description', 'origin']
	ordering_fields = ['name', 'price', 'created_at']

	@action(detail=True, methods=['get'])
	def reviews(self, request, pk=None):
		"""Custom action: получить все отзывы для конкретного товара"""
		product = self.get_object()
		reviews = product.reviews.all()
		page = self.paginate_queryset(reviews)
		if page is not None:
			serializer = ReviewSerializer(page, many=True)
			return self.get_paginated_response(serializer.data)
		serializer = ReviewSerializer(reviews, many=True)
		return Response(serializer.data)

	@action(detail=False, methods=['get'])
	def featured(self, request):
		"""Custom action: получить рекомендованные товары (рейтинг >= 4)"""
		featured_products = self.get_queryset().annotate(
			avg_rating=Avg('reviews__rating'),
			review_count=Count('reviews')
		).filter(avg_rating__gte=4.0, review_count__gte=1).order_by('-avg_rating')[:8]

		serializer = self.get_serializer(featured_products, many=True)
		return Response(serializer.data)

class OrderViewSet(viewsets.ModelViewSet):
	"""
	ViewSet для заказов.
	Пользователи видят только свои заказы.
	"""
	serializer_class = OrderSerializer
	permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
	filter_backends = [DjangoFilterBackend, OrderingFilter]
	filterset_fields = ['status']
	ordering_fields = ['created_at', 'total_amount']

	# ЯВНО УКАЗЫВАЕМ queryset ДЛЯ АВТОМАТИЧЕСКОГО ОПРЕДЕЛЕНИЯ BASENAME
	queryset = Order.objects.all()

	def get_queryset(self):
		"""Возвращаем только заказы текущего пользователя"""
		return self.queryset.filter(user=self.request.user)

	def perform_create(self, serializer):
		"""Автоматически устанавливаем пользователя при создании заказа"""
		serializer.save(user=self.request.user)

class ReviewViewSet(viewsets.ModelViewSet):
	"""
	ViewSet для отзывов.
	Пользователи могут управлять только своими отзывами.
	"""
	serializer_class = ReviewSerializer
	permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
	filter_backends = [DjangoFilterBackend, OrderingFilter]
	filterset_fields = ['product', 'rating']
	ordering_fields = ['created_at', 'rating']

	# ЯВНО УКАЗЫВАЕМ queryset ДЛЯ АВТОМАТИЧЕСКОГО ОПРЕДЕЛЕНИЯ BASENAME
	queryset = Review.objects.all()

	def get_queryset(self):
		"""Возвращаем только отзывы текущего пользователя"""
		return self.queryset.filter(user=self.request.user)

	def perform_create(self, serializer):
		"""Автоматически устанавливаем пользователя при создании отзыва"""
		serializer.save(user=self.request.user)

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

class UserRegistrationView(APIView):
	"""
	API endpoint для регистрации новых пользователей.
	"""
	permission_classes = [AllowAny]

	def post(self, request):
		serializer = UserRegisterSerializer(data=request.data)
		if serializer.is_valid():
			user = serializer.save()
			return Response({
				"message": "User created successfully",
				"user": UserSerializer(user).data
			}, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
	"""
	API endpoint для просмотра и редактирования профиля пользователя.
	"""
	permission_classes = [IsAuthenticated]

	def get(self, request):
		"""Получить профиль текущего пользователя"""
		serializer = UserSerializer(request.user)
		return Response(serializer.data)

	def put(self, request):
		"""Обновить профиль текущего пользователя"""
		serializer = UserSerializer(request.user, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)