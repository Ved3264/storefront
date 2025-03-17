from rest_framework.response import Response
from rest_framework.decorators import api_view,action
from django.shortcuts import render,redirect
from rest_framework import status,viewsets
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from .serializers import ProductSerializers,CollectionSerializers,ReviewSerializer
from .models import Product,Collection,OrderItem,Review



class ProductViewSET(viewsets.ModelViewSet):
    product = Product.objects.select_related('collection').all()
    serialize = ProductSerializers(product, many=True)

    def destroy(self, request, *args, **kwargs):
        product_pk = kwargs['pk']
        if OrderItem.objects.filter(product__id=product_pk).exists():
            return Response({"error": "Product cannot be deleted because it is associated with an order item."},
                             status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)
    



class CollectinViewSET(viewsets.ModelViewSet):
    collection = Collection.objects.all()
    serialize = CollectionSerializers(collection,many=True)


class ReviewViewSET(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def retrieve(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_pk')
        review_id = self.kwargs.get('pk')
        print(product_id)
        print(review_id)
        review = Review.objects.filter(id=review_id,product=product_id).first() 
        
        if not review:
            return Response({"error": "Review not found for this product"}, status=404)

        serializer = self.get_serializer(review)
        return Response(serializer.data)
