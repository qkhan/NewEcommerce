from django.shortcuts import render, redirect
from billing.models import BillingProfile
from addresses.forms import AddressForm
from django.utils.http import is_safe_url
from .models import Address

def checkout_address_create_view(request):
    form = AddressForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next_url')
    redirect_path = next_ or next_post or None
    address_type = request.POST.get('address_type')
    print ("Address Type:", address_type)
    print ("next_post",next_post)
    print ("redirect_path", redirect_path)
    if form.is_valid():
        print (form.cleaned_data)
        print ("REQUEST")
        print(request)
        instance = form.save(commit=False)
        #address_type = form.cleaned_data.get("address_type", "shipping")


        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if billing_profile is not None:
            instance.billing_profile = billing_profile
            instance.address_type = address_type
            instance.save()
        else:
            print("Error here")
            return redirect("cart:checkout")

        request.session[address_type + "_address_id"]  = instance.id
        print("Address Type: {0} | ID: {1}".format(address_type, instance.id))
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("cart:checkout")

    return redirect("cart:checkout")


def checkout_address_reuse_view(request):
    if request.user.is_authenticated():
        context = {}
        next_ = request.GET.get('next')
        next_post = request.POST.get('next_url')
        redirect_path = next_ or next_post or None
        #address_type = request.POST.get('address_type')
        #print ("ReUse Address Type:", address_type)
        print ("ReUse next_post",next_post)
        print ("ReUse redirect_path", redirect_path)
        if request.method == "POST":
            print(request.POST)
            shipping_address = request.POST.get('shipping_address', None)
            address_type = request.POST.get('address_type', 'shipping')
            billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

            if shipping_address is not None:
                print ("Shipping Address ID: ", shipping_address)
                qs = Address.objects.filter(billing_profile=billing_profile, id=shipping_address)
                if qs.exists():

                    request.session[address_type + "_address_id"] = shipping_address
            print(address_type + "_address_id")
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect(redirect_path)
    return redirect("cart:checkout")
