import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coffee_shop_online.settings')
django.setup()

from django.contrib.auth.models import User
from api.models import Category, Product, Order, OrderItem, Review

def create_initial_data():
	# Создаем категории
	categories_data = [
		{"name": "Coffee Beans", "description": "Fresh roasted coffee beans from around the world"},
		{"name": "Ground Coffee", "description": "Pre-ground coffee for various brewing methods"},
		{"name": "Coffee Capsules", "description": "Compatible capsules for Nespresso and other machines"},
		{"name": "Coffee Equipment", "description": "Brewing equipment and accessories"},
		{"name": "Tea & Accessories", "description": "Premium teas and tea brewing accessories"},
	]

	categories = {}
	for cat_data in categories_data:
		category, created = Category.objects.get_or_create(
			name=cat_data["name"],
			defaults={"description": cat_data["description"]}
		)
		categories[cat_data["name"]] = category
		print(f"Category: {category.name}")

	# Создаем товары
	products_data = [
		{"name": "Ethiopia Yirgacheffe", "category": "Coffee Beans", "price": 25.99, "roast_level": "light", "origin": "Ethiopia", "weight_grams": 250, "description": "Floral and tea-like with citrus notes"},
		{"name": "Colombia Supremo", "category": "Coffee Beans", "price": 22.50, "roast_level": "medium", "origin": "Colombia", "weight_grams": 250, "description": "Balanced with caramel and nutty flavors"},
		{"name": "Italian Espresso", "category": "Coffee Beans", "price": 27.99, "roast_level": "dark", "origin": "Brazil", "weight_grams": 250, "description": "Rich and bold with chocolate notes"},
		{"name": "French Press Blend", "category": "Ground Coffee", "price": 18.99, "roast_level": "medium", "origin": "Blend", "weight_grams": 500, "description": "Coarse grind perfect for French press"},
		{"name": "Morning Blend Capsules", "category": "Coffee Capsules", "price": 12.99, "roast_level": "medium", "origin": "Blend", "weight_grams": 200, "description": "Smooth and balanced everyday coffee"},
		{"name": "French Press", "category": "Coffee Equipment", "price": 49.99, "roast_level": "medium", "origin": "China", "weight_grams": 800, "description": "Classic glass French press"},
		{"name": "Earl Grey Premium", "category": "Tea & Accessories", "price": 15.99, "roast_level": "medium", "origin": "Sri Lanka", "weight_grams": 100, "description": "Bergamot flavored black tea"},
	]

	products = {}
	for prod_data in products_data:
		product, created = Product.objects.get_or_create(
			name=prod_data["name"],
			defaults={
				"category": categories[prod_data["category"]],
				"price": prod_data["price"],
				"roast_level": prod_data["roast_level"],
				"origin": prod_data["origin"],
				"weight_grams": prod_data["weight_grams"],
				"description": prod_data["description"]
			}
		)
		products[prod_data["name"]] = product
		print(f"Product: {product.name}")

	print("Initial data created successfully!")

if __name__ == "__main__":
	create_initial_data()