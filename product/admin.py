from django.contrib import admin

from .models import ProductImage, Category, Product


class ImageInline(admin.TabularInline):
    model   = ProductImage
    extra   = 3
    fields  = ('image', )    #--> tuple that's why we put the comma


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline
    ]
    list_display        = ('uuid', 'title', 'price')
    list_display_links  = ('uuid', 'title')

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)

