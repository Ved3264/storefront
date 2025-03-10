from django.contrib import admin
from django.db.models.aggregates import Count
from . import models
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['title','price','InventoryStatus','collection_title']
    list_editable=['price']
    list_per_page=10
    list_select_related=['collection']

    @admin.display(ordering='inventory')
    def InventoryStatus(self,product):
        if product.inventory<=10:
            return 'low'
        return 'ok'
    
    def collection_title(self,product):
        return product.collection.title


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','membership']
    list_editable=['membership']
    ordering=['first_name','last_name']
    list_per_page=10
    search_fields=['first_name__istartswith','last_name__istartswith']


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['id','placed_at','customer']



@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_count']

    @admin.display(ordering='product_count')
    def product_count(self, collection):
        url = reverse('admin:store_product_changelist') + '?' + urlencode({'collection_id': str(collection.id)})
        return format_html('<a href="{}">{}</a>', url, collection.product_count)


    def get_queryset(self, request):
        return super().get_queryset(request).annotate(product_count=Count('product'))

