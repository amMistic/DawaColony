from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
    return render(request, "products/list_all.html", context)


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

    return render(request, "products/product_form.html", context)


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

    return render(request, "products/product_form.html", context)


@auth_required(allowed_roles=["Seller"])
@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted sucessfully!")
        return redirect("products:listall-products")

    context = {"product": product}

    return render(request, "products/product_deleted.html", context)
