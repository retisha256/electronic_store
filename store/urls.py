

from django.urls import path
from . import views

urlpatterns = [
     path("", views.index, name="home"), # Changed 'index' to 'home',
    path("search/", views.search, name="search"),
    path("cart/", views.cart, name="cart"),
    path("add_to_cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("update_cart/", views.update_cart, name="update_cart"), # Add this line
    path("checkout/", views.checkout, name="checkout"),
    path("remove_from_cart/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
    # path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
]