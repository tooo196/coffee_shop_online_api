from django.contrib import admin
from .models import Category, Product, Order, OrderItem, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'created_at')
	search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'category', 'price', 'roast_level', 'is_available')
	list_filter = ('category', 'roast_level', 'is_available')
	search_fields = ('name', 'description', 'origin')

class OrderItemInline(admin.TabularInline):
	model = OrderItem
	extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'status', 'total_amount', 'created_at')
	list_filter = ('status', 'created_at')
	search_fields = ('user__username', 'shipping_address')
	inlines = [OrderItemInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
	list_display = ('product', 'user', 'rating', 'created_at')
	list_filter = ('rating', 'created_at')
	search_fields = ('product__name', 'user__username')