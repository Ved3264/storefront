from django.contrib import admin
from django.db.models.aggregates import Count
from . import models
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [ 
            ('<10','Low'),
            ('>10','Ok')
        ]
    
    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        elif self.value() == '>10':
            return queryset.filter(inventory__gt=10)
    
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields=['collection']
    prepopulated_fields={
        'slug':['title']
    }
    actions=['inventory_clear']
    list_display=['title','price','InventoryStatus','collection_title']
    list_editable=['price']
    list_per_page=10
    list_select_related=['collection']
    list_filter=['collection',InventoryFilter]
    search_fields=['title']


    @admin.display(ordering='inventory')
    def InventoryStatus(self,product):
        if product.inventory<=10:
            return 'low'
        return 'ok'
    
    @admin.action(description='Clear inventory')
    def inventory_clear(self,request,queryset):
        update_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{update_count} inventory count update successfully!'
            
        )
    
    def collection_title(self,product):
        return product.collection.title


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','membership']
    list_editable=['membership']
    ordering=['first_name','last_name']
    list_per_page=10
    search_fields=['first_name__istartswith','last_name__istartswith']


class OrderItemInline(admin.TabularInline):
    autocomplete_fields=['product']
    model = models.OrderItem
    extra=0
    min_num=1
    max_num=10

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines=[OrderItemInline]
    list_display=['id','placed_at','customer','payment_status']
    autocomplete_fields=['customer']
    


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_count']
    search_fields=['title']

    @admin.display(ordering='product_count')
    def product_count(self, collection):
        url = reverse('admin:store_product_changelist') + '?' + urlencode({'collection_id': str(collection.id)})
        return format_html('<a href="{}">{}</a>', url, collection.product_count)


    def get_queryset(self, request):
        return super().get_queryset(request).annotate(product_count=Count('product'))

