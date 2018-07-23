import datetime
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404,reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test



# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from .models import Category, Product, Client, Order
from .forms import  *

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        user = request.user

    else:
        user = ""
    cat_list = Category.objects.all().order_by('id')
    return render(request, 'myapp/index.html', {'cat_list': cat_list, 'user': user})


def about(request):

    response = render(request, 'myapp/about.html')  # store the response in response variable
    if not request.COOKIES.get('about_visits'):
        response.set_cookie('about_visits', '1', 300)
    else:
        about_visits = int(request.COOKIES.get('about_visits', '1')) + 1
        response.set_cookie('about_visits', str(about_visits), 300)
    return response


def detail(request,cat_no):
    category = get_object_or_404(Category, id=cat_no)
    product_name = category.products.all()
    return render(request, "myapp/detail.html", {'cat_no':cat_no,'category':category,'product' :product_name})


def products(request):
    prodlist = Product.objects.all().order_by('id')
    return render(request, 'myapp/products.html', {'prodlist': prodlist})


def place_order(request):
    msg = ''
    neg = 0
    if request.user.is_authenticated:
        testuser = request.user
        prodlist = Product.objects.all()
        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                if order.num_units <= order.product.stock:
                    product = Product.objects.get(name=order.product.name)
                    product.stock = product.stock - order.num_units
                    product.save()
                    msg = 'Your order has been placed successfully.'
                    neg = 0
                    pd = Product()
                    pd.refill(order.product.name)
                    order.save()
                else:
                    neg = 1
                    msg = 'We do not have sufficient stock to fill your order.'
                return render(request, 'myapp/order_response.html', {'msg': msg, 'neg': neg})
        else:
            form = OrderForm()
            return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg, 'prodlist': prodlist,'testuser':testuser})
    else:
        testuser = ""
        msg = 'You need to be logged in first!'
        request.session.set_test_cookie()
        return HttpResponseRedirect(reverse('myapp:login'))


def productdetail(request, prod_id):
    msg = ''
    prod_list = Product.objects.get(id=prod_id)
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            if request.POST['interested'] == '1':
                prod = Product.objects.get(id=prod_id)
                prod.interested += 1
                prod.save()
                msg = 'Your interest is updated successfully.'
            else:
                msg = 'Your interest is not updated successfully.'
        return render(request, 'myapp/index.html', {'form': form, 'prod_list': prod_list, 'msg': msg})
    else:
        form = InterestForm()
        return render(request, 'myapp/productdetail.html', {'form': form, 'prod': prod_list, 'msg': msg})


def user_login(request):
    form = LoginForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        cli = Client.objects.get(username=username)
        user = authenticate(request, username=username, password=password)
        request.session.set_expiry(3600)
        if user:
            if user.is_active:
                if 'last_login' in request.session:
                    last_login = request.session.get('last_login')
                else:
                    currentDT = datetime.datetime.now()
                    request.session['last_login'] = str(currentDT.strftime("%d-%m-%Y %H:%M"))
                login(request, user)
                if request.session.get('frommyorder'):
                    del request.session['frommyorder']
                    return HttpResponseRedirect(reverse('myapp:myorders'))
                elif request.session.test_cookie_worked():
                    request.session.delete_test_cookie()
                    prodlist = Product.objects.all()
                    # return render(request, 'myapp/placeorder.html', {'prodlist': prodlist })
                    return HttpResponseRedirect(reverse('myapp:place_order'))
                else:
                    return HttpResponseRedirect(reverse('myapp:index'))
                #return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled')
        else:
            msg = "Invalid login details."
            return render(request, 'myapp/login.html', {'msg': msg})
    else:
        return render(request, 'myapp/login.html')


@login_required()
def user_logout(request):
    logout(request)
    msg = "You successfully logged out"
    cat_list = Category.objects.all().order_by('id')
    return render(request, 'myapp/index.html', {'msg': msg, 'cat_list': cat_list})


def myorders(request):
    if request.user.is_authenticated:
        testuser = request.user
        myorder = Order.objects.filter(client__username=request.user)
        return render(request, 'myapp/myorders.html', {'myorder': myorder, 'testuser': testuser})

    else:
        testuser = ""
        message = 'login please'
        request.session['frommyorder'] = True
        return HttpResponseRedirect(reverse('myapp:login'))
        #return render(request, 'myapp/myorders.html', {'message': message, 'testuser': testuser})

def register(request):
    if request.method == 'POST':
        msg=''
        print(request.POST)
        username = request.POST.get('username')

        password = request.POST.get('password')
        company=request.POST.get('company')
        shipping_address=request.POST.get('shippingadd')
        city=request.POST.get('city')
        province=request.POST.get('prov')
        print(request.POST)
        print(username, password)
        client=Client.objects.create(username=username, password=password, company=company, shipping_address=shipping_address,city=city,province=province,is_superuser=True,is_staff=True)
        msg='Registered successfully'
        return render(request, 'myapp/index.html', {'msg': msg})
    else:
        return render(request, 'myapp/register.html')