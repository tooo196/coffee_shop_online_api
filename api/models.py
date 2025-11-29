from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
	"""
	Модель категорий товаров (например: Зерновой, Молотый, Капсулы)
	Связана с Product через ForeignKey
	"""
	name = models.CharField(max_length=100, unique=True)
	description = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = "Categories"  # Правильное отображение в админке
		ordering = ['name']  # Сортировка по умолчанию

	def __str__(self):
		return self.name

class Product(models.Model):
	"""
	Основная модель товара - кофе
	Связана с Category, OrderItem и Review
	"""
	# Варианты степени обжарки
	ROAST_LEVEL_CHOICES = [
		('light', 'Light Roast'),
		('medium', 'Medium Roast'),
		('dark', 'Dark Roast'),
	]

	name = models.CharField(max_length=200)
	description = models.TextField()
	price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
	category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
	roast_level = models.CharField(max_length=10, choices=ROAST_LEVEL_CHOICES, default='medium')
	origin = models.CharField(max_length=100)  # Страна происхождения
	weight_grams = models.PositiveIntegerField(default=250)  # Вес упаковки
	is_available = models.BooleanField(default=True)  # Доступен для заказа
	image = models.ImageField(upload_to='products/', null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']  # Новые товары первыми

	def __str__(self):
		return self.name

class Order(models.Model):
	"""
	Модель заказа. Связывает пользователя с товарами через OrderItem
	"""
	STATUS_CHOICES = [
		('pending', 'Pending'),
		('processing', 'Processing'),
		('shipped', 'Shipped'),
		('delivered', 'Delivered'),
		('cancelled', 'Cancelled'),
	]

	user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
	total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	shipping_address = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']  # Новые заказы первыми

	def __str__(self):
		return f"Order #{self.id} - {self.user.username}"

class OrderItem(models.Model):
	"""
	Промежуточная модель для связи заказа и товаров
	Хранит количество и цену на момент заказа
	"""
	order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
	price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена на момент заказа

	class Meta:
		unique_together = ['order', 'product']  # Уникальная пара заказ-товар

	def __str__(self):
		return f"{self.quantity} x {self.product.name}"

class Review(models.Model):
	"""
	Модель отзывов на товары
	Пользователь может оставить только один отзыв на товар
	"""
	product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])  # 1-5 звезд
	comment = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ['product', 'user']  # Один отзыв на товар от пользователя
		ordering = ['-created_at']  # Новые отзывы первыми

	def __str__(self):
		return f"Review for {self.product.name} by {self.user.username}"