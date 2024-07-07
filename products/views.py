from typing import Any
from django.db.models.query import QuerySet
from django.http import Http404
from django.views.generic import DetailView, ListView
from products.models import Products
from products.utils import q_search


class CatalogView(ListView):
    model = Products
    # queryset = Products.objects.all().order_by('-id')
    template_name = "products/catalog.html"
    context_object_name = "products"
    paginate_by = 3
    allow_empty = False
    
    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        on_sale = self.request.GET.get('on_sale')
        order_by = self.request.GET.get('order_by')
        query = self.request.GET.get('q')
        
        if category_slug == 'all':
            products = super().get_queryset()
        elif query:
            products = q_search(query)
        else:
            products = super().get_queryset().filter(category__slug=category_slug)
            if not products.exists():
                raise Http404()
        
        if on_sale:
            products = products.filter(discount__gt=0)
        if order_by and order_by != 'default':
            products = products.order_by(order_by)
            
        return products
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Catalog"
        context["slug_url"] = self.kwargs.get("category_slug")
        return context
    
    
class ProductView(DetailView):
    # model = Products
    # slug_field = "slug"
    template_name = "products/product.html"
    slug_url_kwarg = "product_slug"
    context_object_name = "product"

    def get_object(self, queryset=None):
        product = Products.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        return product
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.name
        return context
    
    
# def catalog(request, category_slug=None):
#     page = request.GET.get('page', 1)
#     on_sale = request.GET.get('on_sale', None)
#     order_by = request.GET.get('order_by', None)
#     query = request.GET.get('q', None)
    

#     if category_slug == 'all':
#         products = Products.objects.all()
#     elif query:
#         products = q_search(query)
#     else:
#         products = Products.objects.filter(category__slug=category_slug)
#         if not products.exists():
#             raise Http404()
    
#     if on_sale:
#         products = products.filter(discount__gt=0)
#     if order_by and order_by != 'default':
#         products = products.order_by(order_by)
        
#     paginator = Paginator(products, 3)
#     current_page = paginator.page(int(page))    
#     context = {
#         "title": "Catalog",
#         "products": current_page,
#         "slug_url": category_slug,
#     }
#     return render(request, "products/catalog.html", context)


# def product(request, product_slug): # separate product
#     product = Products.objects.get(slug=product_slug)
    
#     context = {
#         'product': product
#     }
#     return render(request, "products/product.html", context)
