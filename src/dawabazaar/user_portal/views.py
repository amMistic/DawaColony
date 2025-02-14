from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from accounts.views import auth_required
from accounts.models import User
from .forms import UpdateCustomerForm, AddressForm, ChangePasswordForm
from .models import Address


@login_required
def profile(request):
    user_id = request.user.id
    user = get_object_or_404(User, id=user_id)
    context = {"user": user}
    return render(request, "user_portal/profile/profile.html", context)


@login_required
def update_profile(request, id:int):
    
    user = get_object_or_404(User, id=id)
    form = UpdateCustomerForm(instance=user)
    if request.method == "POST":
        form = UpdateCustomerForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User Profile Update Sucessfully!!")
            return redirect("customer:user-profile")
        else:
            messages.error(request, 'Unable to update profile!!')
    else:
        form = UpdateCustomerForm(instance=user)

    context = {"user": user, "form": form}
    return render(request, "user_portal/profile/update_profile.html", context)


@login_required
def manage_addresses(request):
    addresses = Address.objects.filter(user=request.user)
    context = {"addresses": addresses}
    return render(request, "user_portal/manage_address/manage_address.html", context)


@login_required
def add_address(request):
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, "Address added sucessfully!!")
            return redirect("customer:manage-user-addresses")
    else:
        form = AddressForm()
    context = {"form": form, "is_edit": False}

    return render(request, "user_portal/manage_address/add_address.html", context)


@login_required
def edit_address(request, address_id: int):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Adderss updated sucessfully!')
            return redirect('customer:manage-user-addresses')
    else:
        form=AddressForm(instance=address)
    
    context = {
        'form' : form,
        'address' : address,
        'is_edit' : True 
    }
        
    return render(request,'user_portal/manage_address/add_address.html', context)


@login_required
def delete_address(request, address_id:int):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.delete()
    messages.success(request, 'Address Deleted Sucessfully!')
    return redirect('customer:manage-user-addresses')

@login_required
def set_default_address(request, address_id:int):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.is_default = True
    messages.success(request, 'Default Address updated sucessfully!')
    return redirect('customer:manage-user-addresses')
    
@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            if user.check_password(form.cleaned_data.get('current_password')):
                user.set_password(form.cleaned_data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password Update Sucessfully!')
                return redirect('customer:user-profile')
            else:
                messages.error(request, 'Current Password is incorrect!')
    else:
        form=ChangePasswordForm()
    
    context = {
        'form' : form,
        'user' : request.user
    }
    
    return render(request, 'user_portal/profile/change_password.html', context)