from .models import Category
from decimal import Decimal

def nav_and_cart(request):
    categories = Category.objects.all()
    cart = request.session.get("cart", {})
    count = sum(item.get("qty", 0) for item in cart.values())
    total = sum(Decimal(str(item.get("price", 0))) * item.get("qty", 0) for item in cart.values())
    return {
        "nav_categories": categories,
        "cart_count": count,
        "cart_total": total,
    }
