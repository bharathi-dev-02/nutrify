from django.urls import path  # type: ignore
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register', views.register, name="register"),
    path('login', views.login_page, name="login"),
    path('logout', views.logout_page, name="logout"),
    
    # 🛒 Cart & Wishlist
    path('cart', views.cart_page, name="cart"),
    path('fav', views.fav_page, name="fav"),
    path('favviewpage', views.favviewpage, name="favviewpage"),
    path('remove_fav/<str:fid>', views.remove_fav, name="remove_fav"),
    path('remove_cart/<str:cid>', views.remove_cart, name="remove_cart"),
    path('addtocart', views.add_to_cart, name="addtocart"),

    # 🛍️ Collections & Products
    path('collections', views.collections, name="collections"),
    path('collections/<str:name>', views.collectionsview, name="collections"),
    path('collections/<str:cname>/<str:pname>', views.product_details, name="product_details"),

    # 🔹 Razorpay Payment Integration
    path('create-order/', views.create_razorpay_order, name="create_razorpay_order"),  # 🛒 Create Razorpay Order
    path('verify-payment/', views.verify_payment, name="verify_payment"),  # ✅ Verify Razorpay Payment
]
