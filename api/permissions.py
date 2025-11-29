from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
	"""
	Custom permission: разрешает редактирование только владельцу объекта.
	Для безопасных методов (GET, HEAD, OPTIONS) доступ разрешен всем.
	"""
	def has_object_permission(self, request, view, obj):
		# Разрешаем чтение для всех запросов
		if request.method in permissions.SAFE_METHODS:
			return True

		# Разрешаем запись только владельцу объекта
		# Предполагаем, что у модели есть поле 'user'
		return obj.user == request.user