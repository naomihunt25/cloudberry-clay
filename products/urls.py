from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Display all products with optional sorting/filtering/search
    path('', views.all_products, name='products'),

    # Display a single product detail page
    path('<int:product_id>/', views.product_detail, name='product_detail'),

    # Admin-only: Add a new product
    path('add/', views.add_product, name='add_product'),

    # Admin-only: Edit an existing product
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),

    # Admin-only: Delete a product
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
]