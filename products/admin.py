from django.contrib import admin
from products.models import Categories, Products

@admin.register(Categories)
class CategoryModel(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name','slug')
    list_display = ('name','slug')
    
@admin.register(Products)
class ProductModel(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('description','image','price','category')
    list_display = ('description','image','price','category')