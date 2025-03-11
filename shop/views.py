import json
import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from shop.form import CustomUserForm
from .models import *

# ✅ Home Page
def home(request):
    products = Product.objects.filter(trending=1)
    return render(request, "shop/index.html", {"products": products})

# ✅ Favourite Page
def favviewpage(request):
    if request.user.is_authenticated:
        fav = Favourite.objects.filter(user=request.user)
        return render(request, "shop/fav.html", {"fav": fav})
    else:
        messages.error(request, "You must be logged in to view your favourites.")
        return redirect("/login")

# ✅ Remove Favourite
def remove_fav(request, fid):
    if request.user.is_authenticated:
        Favourite.objects.filter(id=fid, user=request.user).delete()
    return redirect("/favviewpage")

# ✅ Cart Page (with total amount)
def cart_page(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        total_amount = sum(item.total_cost for item in cart)
        return render(request, "shop/cart.html", {"cart": cart, "total_amount": total_amount})
    else:
        messages.error(request, "You must be logged in to view your cart.")
        return redirect("/login")

# ✅ Remove from Cart
def remove_cart(request, cid):
    if request.user.is_authenticated:
        Cart.objects.filter(id=cid, user=request.user).delete()
    return redirect("/cart")

# ✅ Add to Favourite
@csrf_exempt
def fav_page(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            product_id = data.get('pid')

            if Product.objects.filter(id=product_id).exists():
                fav, created = Favourite.objects.get_or_create(user=request.user, product_id=product_id)
                if not created:
                    return JsonResponse({'status': 'Product Already in Favourite'}, status=200)
                return JsonResponse({'status': 'Product Added to Favourite'}, status=200)

            return JsonResponse({'status': 'Product Not Found'}, status=404)
        else:
            return JsonResponse({'status': 'Login to Add to Favourite'}, status=403)
    return JsonResponse({'status': 'Invalid Access'}, status=400)

# ✅ Add to Cart
@csrf_exempt
def add_to_cart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.load(request)
            product_qty = data['product_qty']
            product_id = data['pid']

            try:
                product_status = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return JsonResponse({'status': 'Product Not Found'}, status=404)

            if Cart.objects.filter(user=request.user, product_id=product_id).exists():
                return JsonResponse({'status': 'Product Already in Cart'}, status=200)
            else:
                if product_status.quantity >= product_qty:
                    Cart.objects.create(user=request.user, product_id=product_id, product_qty=product_qty)
                    return JsonResponse({'status': 'Product Added to Cart'}, status=200)
                else:
                    return JsonResponse({'status': 'Product Stock Not Available'}, status=200)
        else:
            return JsonResponse({'status': 'Login to Add to Cart'}, status=403)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=400)

# ✅ Logout
def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged Out Successfully")
    return redirect("/")

# ✅ Login
def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            name = request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(request, username=name, password=pwd)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in Successfully")
                return redirect("/")
            else:
                messages.error(request, "Invalid Username or Password")
                return redirect('/login')
        return render(request, "shop/login.html")

# ✅ Register
def register(request):
    form = CustomUserForm()
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Successful! You Can Now Login.")
            return redirect('/login')
    return render(request, "shop/register.html", {'form': form})

# ✅ View Categories
def collections(request):
    category = Category.objects.filter(status=0)
    return render(request, "shop/collections.html", {"category": category})

# ✅ View Products in Category
def collectionsview(request, name):
    if Category.objects.filter(name=name, status=0).exists():
        products = Product.objects.filter(category__name=name)
        return render(request, "shop/products/index.html", {"products": products, "category_name": name})
    messages.error(request, "No Such Category Found")
    return redirect('collections')

# ✅ Product Details
def product_details(request, cname, pname):
    if Category.objects.filter(name=cname, status=0).exists():
        if Product.objects.filter(name=pname, status=0).exists():
            product = Product.objects.filter(name=pname, status=0).first()
            return render(request, "shop/products/product_details.html", {"product": product})
    messages.error(request, "No Such Product Found")
    return redirect('collections')

# ✅ Razorpay Order Creation
@csrf_exempt
def create_razorpay_order(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            amount = int(data.get("amount", 0)) * 100  # Convert Rs to Paise

            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            order = client.order.create({
                "amount": amount,
                "currency": "INR",
                "payment_capture": "1"
            })
            return JsonResponse({"order_id": order["id"], "amount": order["amount"]})
        except Exception as e:
            print("Razorpay Order Error:", str(e))
            return JsonResponse({"error": "Failed to create order"}, status=500)
    return JsonResponse({"error": "Invalid request"}, status=400)

# ✅ Payment Verification
@csrf_exempt
def verify_payment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            razorpay_order_id = data.get("order_id")
            razorpay_payment_id = data.get("payment_id")
            razorpay_signature = data.get("signature")

            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            params_dict = {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature,
            }

            if client.utility.verify_payment_signature(params_dict):
                # Save payment in DB
                RazorpayPayment.objects.create( # type: ignore
                    user=request.user,
                    order_id=razorpay_order_id,
                    payment_id=razorpay_payment_id,
                    amount=data.get("amount"),
                    status="Success"
                )
                # Clear cart after successful payment
                Cart.objects.filter(user=request.user).delete()
                return JsonResponse({"status": "Payment Successful"})
            else:
                return JsonResponse({"status": "Payment Verification Failed"}, status=400)

        except Exception as e:
            return JsonResponse({"status": "Payment Failed", "error": str(e)}, status=400)
    
    return JsonResponse({"status": "Invalid request"}, status=400)
