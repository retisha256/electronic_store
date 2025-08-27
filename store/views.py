from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Category, Product, Order, OrderItem
from .forms import CheckoutForm

# Home: list categories with products
def index(request):
    categories = Category.objects.prefetch_related("products").all()
    return render(request, "index.html", {"categories": categories})

# Category page (optional anchor-free route)
def category_page(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return render(request, "category.html", {"category": category})

# Search (backend)
def search(request):
    q = request.GET.get("q", "")
    results = Product.objects.none()
    if q:
        results = Product.objects.filter(name__icontains=q) | Product.objects.filter(description__icontains=q)
    return render(request, "search.html", {"query": q, "results": results})

# ----- Cart helpers -----
def _get_cart(session):
    return session.setdefault("cart", {})

def _save_cart(request, cart):
    request.session["cart"] = cart
    request.session.modified = True

# Add to cart (POST only)
def add_to_cart(request, product_id):
    if request.method != "POST":
        return redirect("index") # Changed 'home' to 'index'
    product = get_object_or_404(Product, id=product_id)
    cart = _get_cart(request.session)
    key = str(product.id)
    if key in cart:
        cart[key]["qty"] += 1
    else:
        cart[key] = {"name": product.name, "price": float(product.price), "qty": 1}
    _save_cart(request, cart)
    return redirect(request.POST.get("next") or "index") # Changed 'home' to 'index'
# Remove item
def remove_from_cart(request, product_id):
    cart = _get_cart(request.session)
    key = str(product_id)
    if key in cart:
        del cart[key]
        _save_cart(request, cart)
    return redirect("cart")

# Update quantities (POST)
def update_cart(request):
    if request.method == "POST":
        cart = _get_cart(request.session)
        for key, item in list(cart.items()):
            qty_str = request.POST.get(f"qty_{key}")
            try:
                qty = int(qty_str)
            except (ValueError, TypeError):
                qty = item.get("qty", 1)
            if qty <= 0:
                del cart[key]
            else:
                item["qty"] = qty
        _save_cart(request, cart)
    return redirect("cart")

# View cart
def cart(request):
    cart = _get_cart(request.session)
    items = []
    total = Decimal("0.00")
    for key, item in cart.items():
        line_total = Decimal(str(item["price"])) * item["qty"]
        items.append({
            "id": key,
            "name": item["name"],
            "price": Decimal(str(item["price"])),
            "qty": item["qty"],
            "line_total": line_total,
        })
        total += line_total
    return render(request, "cart.html", {"items": items, "total": total})

# Checkout -> create Order & OrderItems
def checkout(request):
    cart = _get_cart(request.session)
    if not cart:
        return redirect("cart")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                customer_name=form.cleaned_data["customer_name"],
                address=form.cleaned_data["address"],
                email=form.cleaned_data["email"],
                phone=form.cleaned_data.get("phone", ""),
                total=Decimal("0.00"),
            )
            order_total = Decimal("0.00")
            for key, item in cart.items():
                price = Decimal(str(item["price"]))
                qty = item["qty"]
                OrderItem.objects.create(
                    order=order,
                    product_id=int(key),
                    quantity=qty,
                    price=price,
                )
                order_total += price * qty
            order.total = order_total
            order.save()
            # clear cart
            request.session["cart"] = {}
            request.session.modified = True
            return redirect("order_success", order_id=order.id)
    else:
        form = CheckoutForm()

    return render(request, "checkout.html", {"form": form})

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "order_success.html", {"order": order})
