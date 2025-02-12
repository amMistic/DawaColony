from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order


# Create your views here.
@login_required
def order_list(request):
    orders = Order.objects.filter(seller=request.user).order_by("-created_at")
    context = {"orders": orders}
    return render(request, "orders/order_list.html", context)


@login_required
def update_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk, seller=request.user)
    if request.method == "POST":
        status = request.POST.get("status")
        if status in dict(Order.STATUS_CHOICES):
            order.status = status
            order.save()
            messages.success(request, "Order status updated sucessfully!!")
        else:
            messages.success(request, "Invalid Status!!")

    return redirect("products:listall-products")

