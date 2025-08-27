from django.urls import path
from . import views

urlpatterns = [
   path("", views.index, name="home"),
    path("search/", views.search, name="search"),
    path("cart/", views.cart, name="cart"),
    path("add_to_cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("checkout/", views.checkout, name="checkout"),
   # path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
]