from django.urls import path, include

from product import views

urlpatterns = [
    path('products/', views.ProductsList.as_view()),
    path('products/search/', views.search),
    path('products/by-vendor/', views.get_products_by_vendorid),
    path('products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view()),
    path('products/<slug:category_slug>/', views.CategoryDetail.as_view()),
]