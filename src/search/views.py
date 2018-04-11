
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from products.models import Product


# Create your views here.
class SearchProductView(ListView):
    template_name = "search/view.html"

    def get_context_data(self, *args, **kwargs):
        context = super(SearchProductView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        #For analytics Data Modeling, with model "SearchQuery"
        #SearchQuery.objects.create(query=query)
        return context

    def get_queryset(self, *args, **kwargs):
        print ("Hello Qaisar Khan")
        request = self.request
        print("REQUEST:",request.GET)
        query = request.GET.get('q')
        print("QUERY:", query)
        if query is not None:
            # lookups = Q(title__icontains=query)|Q(description__icontains=query)
            # return Product.objects.filter(lookups).distinct()
            return Product.objects.search(query)
        return Product.objects.featured()
