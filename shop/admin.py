from django.contrib import admin
from .models import Category, Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image',)  
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('category',)
    inlines = [ProductImageInline] 


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1
    fields = ('name', 'price') 
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    inlines = [ProductInline,]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
