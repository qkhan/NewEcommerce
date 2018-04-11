from django.shortcuts import render, redirect
from accounts.forms import LoginForm, GuestForm
from .models import Cart
from orders.models import Order
from products.models  import Product
from billing.models import BillingProfile
from accounts.models import GuestEmail
from addresses.forms import AddressForm
from addresses.models import Address
from django.http import JsonResponse


def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [{
                    "id": x.id,
                    "url": x.get_absolute_url(),
                    "name":x.name,
                    "price":x.price
                 }
                 for x in cart_obj.products.all()]
    cart_data = {"products": products, "sub_total": cart_obj.sub_total, "total": cart_obj.total }
    return JsonResponse(cart_data)

# Create your views here.
def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    print ("COUNT: ", cart_obj.products.count())
    request.session['cart_total'] = cart_obj.products.count()
    return render(request, "carts/home.html", { "cart": cart_obj })


def cart_update(request):
    product_id = request.POST.get('product_id')
    print(request.POST)
    try:
        product_obj = Product.objects.get(id=product_id)
    except Product.DoesnotExist:
        print("Product is gone")
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    if product_obj in cart_obj.products.all():
        cart_obj.products.remove(product_obj)
        added = False
    else:
        cart_obj.products.add(product_obj)
        added = True
    request.session['cart_items'] = cart_obj.products.count()
    if (request.is_ajax()):
        print ("Ajax Request")
        json_data = {
            "added": added,
            "removed" : not added,
            "cartItemCount": cart_obj.products.count(),
        }
        return JsonResponse(json_data, status=200)
        #return JsonResponse({"message": "Error 400"}, status=400)
    return redirect("cart:home")


def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")

    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)

    print ("BILLING ID:", billing_address_id)
    print ("SHIPPING ID:", shipping_address_id)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None
    if billing_profile is not None:
        if request.user.is_authenticated():
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile,cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]

        if billing_address_id or shipping_address_id:
            order_obj.save()

    if request.method == "POST":
        "some check that order is done"
        is_done = order_obj.check_done()
        if is_done:
            order_obj.mark_paid()
            del request.session['cart_id']
            del request.session['cart_total']
        return redirect("cart:success")

    context = {
        "order": order_obj,
        "billing_profile": billing_profile,
        "login_form" : login_form,
        "guest_form" : guest_form,
        "address_form" : address_form,
        "address_qs" : address_qs,
    }
    return render(request, "carts/checkout.html", context)

def checkout_done_view(request):
    return render(request, "carts/checkout-done.html", {})



    # user = request.user
    # billing_profile = None
    # login_form = LoginForm()
    # guest_form = GuestForm()
    # guest_email_id = request.session.get('guest_email_id')
    # print("Guest email id: ", guest_email_id)
    # if user.is_authenticated():
    #     'logged in user checkout; remember payment stuff'
    #     billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(user=user, email=user.email)
    #     print("Billing Profile:", billing_profile, " | ", billing_profile_created)
    # elif guest_email_id is not None:
    #     'guest user checkout; auto reloads payment stuff'
    #     guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
    #     billing_profile, billing_guest_profile_created = BillingProfile.objects.get_or_create(email=guest_email_obj.email)
    # else:
    #     pass

    #                                                            cart_obj)
        # order_qs = Order.objects.filter(billing_profile=billing_profile,cart = cart_obj, active=True)
        #
        # if order_qs.count() == 1:
        #     order_obj = order_qs.first()
        # else:
        #     order_obj = Order.objects.create(billing_profile=billing_profile, cart=cart_obj)
