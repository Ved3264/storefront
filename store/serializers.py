from rest_framework import serializers
from .models import Product,Collection,Review
from decimal import Decimal
from django.db.models import F


class CollectionSerializers(serializers.ModelSerializer):
    total_product = serializers.SerializerMethodField(method_name='product_count')

    class Meta:
        model = Collection
        fields = ['id', 'title', 'total_product']

    def product_count(self, obj):
        return Product.objects.filter(collection=obj).count()



class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','discription','slug','inventory','price','price_with_tax','collection']

    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    #collection = CollectionSerializers()


    def calculate_tax(self,product:Product):
        return product.price *Decimal(1.1)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields=['id','product','name','message']