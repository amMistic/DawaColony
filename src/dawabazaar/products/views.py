from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.text import slugify
from django.contrib import messages
from django.db.models import Q

from accounts.views import auth_required
from .forms import CreateProductForm, TableSearch
from .models import Product


@auth_required(allowed_roles=["Seller"])
@login_required
def product_list(request):
    seller = request.user
    # Initialize products with all seller's products
    products = Product.objects.filter(seller=seller)

    form = TableSearch()
    if request.method == "GET":
        form = TableSearch(request.GET)
        if form.is_valid():
            search_query = form.cleaned_data.get("search_query")
            category = form.cleaned_data.get("category")

            # Filter existing products queryset
            if search_query:
                products = products.filter(name__icontains=search_query)

            if category:
                products = products.filter(category=category)

    context = {
        "products": products,
        "categories": Product.CATEGORY_CHOICES,
        "form": form,
        "selected_category": request.GET.get(
            "category", ""
        ),  # Add this to maintain selected value
    }
    return render(request, "seller/products/list_all.html", context)


@auth_required(allowed_roles=["Seller"])
@login_required
def create_product(request):
    if request.method == "POST":
        form = CreateProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, "Product added sucessfully!!")
            return redirect("products:listall-products")
        else:
            messages.error(
                request, f"Unable to get create product!! \n Error : {form.errors}"
            )
    else:
        form = CreateProductForm()

    context = {"form": form, "title": "Add New Product"}

    return render(request, "seller/products/product_form.html", context)


@auth_required(allowed_roles=["Seller"])
@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == "POST":
        form = CreateProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product details updated sucessfully!")
            return redirect("products:listall-products")
        else:
            messages.error(request, "Unable to update product details")
    else:
        form = CreateProductForm(instance=product)

    context = {"form": form, "title": "Edit Product", "product": product}

    return render(request, "seller/products/product_form.html", context)


@auth_required(allowed_roles=["Seller"])
@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted sucessfully!")
        return redirect("products:listall-products")

    context = {"product": product}

    return render(request, "seller/products/product_deleted.html", context)


@login_required
def category_base_view(request, category_name : str):
    sort_param = request.GET.get('sort', 'price_low')
    title = category_name.replace('-',' ').title()
    category_name = category_name.upper().replace('-','_')
    products = Product.objects.filter(
        category__iexact=category_name,
        is_active=True
    )
    
    sort_options = {
        'price_low': 'price',
        'price_high': '-price',
        'newest': '-created_at',
        'name_asc': 'name',
        'name_desc': '-name',
    }
    
    products = products.order_by(sort_options.get(sort_param, 'price_low'))
    
    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    context = {
        'Title' : title,
        'category_name': category_name,
        'products': products,
        'current_sort': sort_param
    }
    
    return render(request, 'customer/products/display_product.html', context)


@login_required
def search_products(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    sort = request.GET.get('sort', 'price_low')
    
    products = Product.objects.filter(is_active=True)
    
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(manufacturer__icontains=query)
        )
    
    if category:
        products = products.filter(category=category)
    
    # Apply sorting
    sort_options = {
        'price_low': 'price',
        'price_high': '-price',
        'newest': '-created_at',
        'name_asc': 'name',
        'name_desc': '-name',
    }
    products = products.order_by(sort_options.get(sort, 'price'))
    
    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    context = {
        'products': products,
        'query': query,
        'category': category,
        'current_sort': sort,
        'categories': Product.CATEGORY_CHOICES,
    }
    return render(request, 'products/search_results.html', context)


@login_required
def product_details(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'customer/products/product_detail.html', context)