from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from carts.models import Cart
from .models import Product

# Create your views here.
class ProductListView(ListView):
    #queryset = Product.objects.all()
    template_name = "products/list.html"
    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        print(context)
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()

class ProductDetailSlugView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        print(context)
        return context

    def get_objects(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('slug')
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesnotExist:
            raise Http404("Not Found")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Something is wrong")
        return instance


# class ProductFeaturedListView(ListView):
#     #queryset = Product.objects.all()
#     template_name = "products/list.html"
#
#     def get_queryset(self, *args, **kwargs):
#         request = self.request
#         #return Product.objects.features()
#         #return Product.objects.all().featured()
#         return Product.objects.all()
#         #return Product.objects.features()
#
# class ProductFeaturedDetailView(DetailView):
#     #queryset = Product.objects.features()
#     #queryset = Product.objects.all().featured()
#     #queryset = Product.objects.all()
#     #queryset = Product.objects.features()
#     queryset = Product.objects.all()
#
#
#     template_name = "products/feature_detail.html"


# def product_list_view(request):
#     queryset = Product.objects.all()
#     context = {
#         'object_list' : queryset,
#     }
#     return render(request, "products/product_list_view.html", context)


# class ProductDetailView(DetailView):
#     queryset = Product.objects.all()
#     template_name = "products/detail.html"
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
#         print(context)
#         return context
#
#     def get_objects(self, *args, **kwargs):
#         request = self.request
#         pk = self.kwargs.get('pk')
#         instance = Product.objects.get_by_id(pk)
#         if instance is None:
#             raise Http404("Product doesn't exist")
#
#
# def product_detail_view(request, pk=None, *args, **kwargs):
#    #instance = Product.objects.get(pk=pk) #id
#     print ("PK: ", pk)
#     # instance = get_object_or_404(Product, id=pk)
#     # print (instance)
#     instance = Product.objects.get_by_id(pk)
#     if instance is None:
#         raise Http404("Product doesn't exist")
#
#     context = {
#         'object' : instance
#     }
#     return render(request, "products/product_detail_view.html", context)
