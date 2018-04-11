"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

from accounts.views import (login_page,
                            register_page,
                            guest_register_view,
                            RegisterView,
                            LoginView,user_login)
from .views import home_page, about_page, contact_page
from addresses.views import checkout_address_create_view, checkout_address_reuse_view
from django.views.generic import TemplateView
from carts.views import cart_detail_api_view



urlpatterns = [
    url(r'^$', home_page, name='home'),
    url(r'^about/$', about_page, name='about'),
    url(r'^contact/$', contact_page, name='contact'),
    url(r'^login/$', user_login, name='login'),
    #url(r'^login/$', login_page, name='login'),
    #url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/guest/$', guest_register_view, name='guest_register'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^checkout/address/create/$', checkout_address_create_view, name='checkout_address_create'),
    url(r'^checkout/address/reuse/$', checkout_address_reuse_view, name='checkout_address_reuse'),
    #url(r'^register/$', register_page, name='register'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^api/cart', cart_detail_api_view, name='api-cart'),
    url(r'^cart/', include('carts.urls', namespace='cart')),
    url(r'^products/', include('products.urls', namespace='product')),
    url(r'^search/', include('search.urls', namespace='search')),
    url(r'^bootstrap/$', TemplateView.as_view(template_name='bootstrap/example.html')),
    url(r'^admin/', admin.site.urls),
    # url(r'^products_fbv/$', product_list_view),
    # #url(r'^products/(?P<pk>\d+)$', ProductDetailView.as_view()),
    # url(r'^products/(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view()),
    # url(r'^products_fbv/(?P<pk>\d+)$', product_detail_view),
    # url(r'^feature/$', ProductFeaturedListView.as_view()),
    # url(r'^feature/(?P<pk>\d+)$', ProductFeaturedDetailView.as_view()),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
