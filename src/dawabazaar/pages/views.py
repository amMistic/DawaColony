from django.shortcuts import render
from accounts.views import auth_required

# Create your views here.
@auth_required(allowed_roles=['Seller','Customer'])
def home_page_view(request):
    return render(request, 'pages/home.html')
    
def no_access_page_view(request):
    return render(request,'pages/no_access.html', {})