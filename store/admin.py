from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "kind", "price", "stock", "featured")
    list_filter = ("category", "kind", "featured")
    search_fields = ("title", "author", "description")
    list_editable = ("price", "stock", "featured")
