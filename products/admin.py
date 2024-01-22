from django.contrib import admin
from products.models import Categories, Products

@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name','slug')
    list_display = ('name','slug')
    
@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name','quantity','description','image','price','category')
    list_display = ('name','quantity','description','image','price','category')
    list_editable = ['price']
    search_fields = ['name','description']
    fields = [
        "name",
        "category",
        "slug",
        "description",
        "image",
        ("price","discount"),
        "quantity"
    ]