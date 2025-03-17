from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSET, CollectinViewSET,ReviewViewSET
from rest_framework_nested.routers import NestedDefaultRouter


router = DefaultRouter()
router.register('products', ProductViewSET, basename='product')
router.register('collections', CollectinViewSET, basename='collection')

reviews_router = NestedDefaultRouter(router,'products', lookup='product')
reviews_router.register('reviews', ReviewViewSET, basename='product-reviews')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(reviews_router.urls)),
]