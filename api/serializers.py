from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Category, Product, Order, OrderItem, Review

class UserSerializer(serializers.ModelSerializer):
	"""Сериализатор для модели User - только для чтения"""
	class Meta:
		model = User
		fields = ('id', 'username', 'email', 'first_name', 'last_name')
		read_only_fields = fields  # Все поля только для чтения

class UserRegisterSerializer(serializers.ModelSerializer):
	"""Сериализатор для регистрации пользователя"""
	password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
	password2 = serializers.CharField(write_only=True, required=True)

	class Meta:
		model = User
		fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

	def validate(self, attrs):
		"""Проверка совпадения паролей"""
		if attrs['password'] != attrs['password2']:
			raise serializers.ValidationError({"password": "Password fields didn't match."})
		return attrs

	def create(self, validated_data):
		"""Создание пользователя с хешированием пароля"""
		validated_data.pop('password2')  # Удаляем подтверждение пароля
		user = User.objects.create_user(**validated_data)  # create_user хеширует пароль
		return user

class CategorySerializer(serializers.ModelSerializer):
	"""Сериализатор для категорий"""
	class Meta:
		model = Category
		fields = '__all__'  # Все поля модели

class ProductSerializer(serializers.ModelSerializer):
	"""Сериализатор для товаров с дополнительным полем названия категории"""
	category_name = serializers.CharField(source='category.name', read_only=True)

	class Meta:
		model = Product
		fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
	"""Сериализатор для элементов заказа с дополнительной информацией о товаре"""
	product_name = serializers.CharField(source='product.name', read_only=True)
	product_price = serializers.DecimalField(source='product.price', read_only=True, max_digits=10, decimal_places=2)

	class Meta:
		model = OrderItem
		fields = '__all__'
		read_only_fields = ('price',)  # Цена устанавливается автоматически

class OrderSerializer(serializers.ModelSerializer):
	"""Сериализатор для заказов с вложенными элементами заказа"""
	items = OrderItemSerializer(many=True, read_only=True)  # Вложенные элементы заказа
	user_email = serializers.EmailField(source='user.email', read_only=True)
	user_name = serializers.CharField(source='user.get_full_name', read_only=True)

	class Meta:
		model = Order
		fields = '__all__'
		read_only_fields = ('user', 'total_amount')  # Эти поля устанавливаются автоматически

class ReviewSerializer(serializers.ModelSerializer):
	"""Сериализатор для отзывов с именем пользователя"""
	user_name = serializers.CharField(source='user.username', read_only=True)

	class Meta:
		model = Review
		fields = '__all__'
		read_only_fields = ('user',)  # Пользователь устанавливается автоматически