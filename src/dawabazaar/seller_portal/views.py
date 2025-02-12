from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.db.models import Sum, Count
from django.contrib import messages

from .forms import UpdateSellerForm, SellerChangePasswordForm
from accounts.views import auth_required
from accounts.views import User
from products.models import Product
from orders.models import Order

# Create your views here.
@auth_required(allowed_roles=['Seller'])
@login_required
def dashboard(request):
    # Get statistics
    total_products = Product.objects.filter(seller=request.user).count()
    total_orders = Order.objects.filter(seller=request.user).count()
    total_sales = Order.objects.filter(
        seller=request.user,
        status='DELIVERED'
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    # Get recent orders
    recent_orders = Order.objects.filter(seller=request.user).order_by('-created_at')[:5]
    
    # Get top selling products
    top_products = Product.objects.filter(
        seller=request.user,
        order__status='DELIVERED'
    ).annotate(
        total_sold=Count('order')
    ).order_by('-total_sold')[:5]

    context = {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_sales': total_sales,
        'recent_orders': recent_orders,
        'top_products': top_products,
    }
    return render(request, 'seller_portal/dashboard.html', context)

@auth_required(allowed_roles=['Seller'])
@login_required
def seller_profile(request):
    return render(request, 'seller_portal/seller_profile.html',{})


@auth_required(allowed_roles=['Seller'])
@login_required
def update_seller_profile(request, id:int):
    user = get_object_or_404(User, id=id)
    form = UpdateSellerForm(instance=user)
    if request.method == 'POST':
        form = UpdateSellerForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Updated Sucessfully!!')
            return redirect('seller:user-profile')
        else:
            print(form.errors)
            messages.error(request, 'Unable to update profile!!')
    else:
        form = UpdateSellerForm(instance=user)
    
    context = {
        'form' : form,
        'user' : user
    }
    
    return render(request, 'seller_portal/update_profile.html', context)

@auth_required(allowed_roles=['Seller'])
@login_required
def change_password(request):
    if request.method == 'POST':
        form = SellerChangePasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            current_password = form.cleaned_data.get('current_password')
            new_password = form.cleaned_data.get('new_password')
            
            if user.check_password(current_password):
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request,user)
                messages.success(request, 'Password updated sucessfully!')
                return redirect('seller:user-profile')
            else:
                messages.error(request, 'Current Password is incorrect!!')
    else:
        form = SellerChangePasswordForm()
    
    context = {
        'form' : form,
    }
    
    return render(request, 'seller_portal/change_password.html',context)