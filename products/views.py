from django.shortcuts import render
from .models import Product
from django.core.paginator import Paginator
from django.db.models import Q

def product_list(request):
    queryset = Product.objects.all()

    search_query = request.GET.get('search', '')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    availability = request.GET.get('availability')

    # Search by name or brand
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) | Q(brand__icontains=search_query)
        )
    
    # Filter by price range
    if price_min:
        queryset = queryset.filter(price__gte=price_min)
    if price_max:
        queryset = queryset.filter(price__lte=price_max)

    # Filter by availability
    if availability == 'available':
        queryset = queryset.filter(is_available=True)
    elif availability == 'not_available':
        queryset = queryset.filter(is_available=False)

    total_results = queryset.count()

    # Pagination: 10 products per page
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'total_results': total_results,
        'search_query': search_query,
        'price_min': price_min or '',
        'price_max': price_max or '',
        'availability': availability or '',
    }
    return render(request, 'products/product_list.html', context)
