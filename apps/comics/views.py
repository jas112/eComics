from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from models import *
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from forms import SalePaymentForm
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
import re
NO_LET_REGEX = re.compile(r'^-?[0-9]+$')
def add_test(request):
    # ============== #
    # ADD QUERY HERE #
    # ============== #
    # Add category
    # Category.objects.create(
    #     name = 'Category1'
    # )
    # Category.objects.create(
    #     name = 'Category2'
    # )
    # Category.objects.create(
    #     name = 'Category3'
    # )

    # Add Product
    # Product.productManager.create(
    #     name='ProductThree',
    #     description='the desc',
    #     image = 'guardians1.jpg',
    #     price = 91.10,
    #     quantity = 5,
    # )
    # category = Category.objects.get(name='Category2')
    # product = Product.productManager.get(name='ProductThree')
    # category.products.add(product)

    return redirect('/test')
def test(request):
    # ============== #
    # ADD QUERY HERE #
    # ============== #
    # products = Product.productManager.all()
    context = {
        'categories' : Category.objects.all(),
        'products' : Product.productManager.all()
    }
    return render(request,'comics/test.html', context)

def index(request):

    if 'shopping_cart' not in request.session:
        request.session['shopping_cart'] = []
    if 'product_total' not in request.session:
        request.session['product_total'] = 0
    if 'user_id' not in request.session:
        request.session['user_id'] = 'null'

    ##################################################################
    # commented so it doesnt keep making new prods for every refresh #
    ##################################################################

    # Product.productManager.create(
    # name        =   "Superman",
    # description =   "Some dork in a cape",
    # image       =   "guardians1.jpg",
    # price       =   6.20,
    # category    =   "Superhero",
    # quantity    =   42
    # )
    # create product
    #print the_product
    # User.userManager.create(
    # email       =   "brian@gmail.com",
    # password    =   "12345678",
    # first_name  =   "Brian",
    # last_name   =   "Sung",
    # admin_auth  =   True
    # )
    # User.userManager.create(
    # email       =   "james@gmail.com",
    # password    =   "12345678",
    # first_name  =   "James",
    # last_name   =   "Sanders",
    # admin_auth  =   True
    # )
    # User.userManager.create(
    # email       =   "kerub@gmail.com",
    # password    =   "12345678",
    # first_name  =   "kerub",
    # last_name   =   "Q",
    # admin_auth  =   True
    # )

    # Category.objects.create(
    #     name = 'SciFi'
    # )
    # Category.objects.create(
    #     name = 'Western'
    # )
    # Category.objects.create(
    #     name = 'Samurai'
    # )
    #the_category = Category.objects.create(name='Horror')
    #Product.productManager.create(name='Dope Shit', description='The shit description', image=None, price=900, quantity=300, category=the_category)
    #product1 = Product.productManager.get(id=31)
    #product2 = Product.productManager.get(id=32)
    #request.session['product_ids'].append(product1)
    #request.session['product_ids'].append(product2)
    #price1 = product1.price
    #price2 = product2.price
    #print total_price
    #Order.orderManager.create(s_fname='Test', s_lname='Tester', user=None,

    # User.userManager.create(email='usetwo@usertwo.com',password='12345678',first_name='usertwo',last_name='lastname')
    # user = User.userManager.get(email='usetwo@usertwo.com')
    # Order.orderManager.create(user=user,s_fname='twouser',s_lname='thelastname',total=3.99,status=2)
    context = {
        "products":Product.productManager.all()
    }
    return render(request, 'comics/index.html', context)

def admin(request):
    return render(request, 'comics/admin.html')

def admin_login(request):
    if request.method=="POST":
        admin = User.userManager.admin_login(request.POST)
        if 'errors' in admin:
            for error in admin['errors']:
                messages.error(request, error)
            return redirect('/admin')
        else:
            request.session['id'] = admin['admin'].id
            request.session['auth'] = admin['admin'].admin_auth
            context = {
            "admin": User.userManager.get(id=request.session['id'])
            }
            return render(request, 'comics/admin_main.html', context)
    return redirect('/admin')

def admin_logout(request):
    if 'auth' in request.session:
        del request.session['auth']
        del request.session['id']
    return redirect('/admin')

def register(request):
    if request.method=="POST":
        User.userManager.create(
        email       =   request.POST['email'],
        password    =   request.POST['password'],
        first_name  =   request.POST['first_name'],
        last_name   =   request.POST['last_name'],
        admin_auth  =   request.POST['admin'],
        )
    return redirect('/admin')

####ADMIN PRODUCTS#######
def product_view(request):
    if 'auth' in request.session:
        product_list = Product.productManager.all()
        paginator = Paginator(product_list, 5)

        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
        	products = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
        	products = paginator.page(paginator.num_pages)
        context = {
        	'products': products,
            'categories': Category.objects.all()
        }
        return render(request, 'comics/admin_products.html', context)
    else:
        return redirect('/')

def admin_prod_search(request):
    if 'auth' in request.session:
        if request.method=="POST":
            products = Product.productManager.filter(name__contains=request.POST['prod_search'])
            context = {
            	'products': products,
                'categories': Category.objects.all()
            }
            return render(request, 'comics/admin_products.html', context)
    else:
        return redirect('/')


def orders_view(request):
    if 'auth' in request.session:
        context = {
        "orders": Order.orderManager.all()
        }
        return render(request, 'comics/admin_orders.html', context)
    else:
        return redirect('/')

def products_main(request):
    if 'cart' not in request.session:
        request.session['cart'] = []

    products_list = Product.productManager.all()
    paginator = Paginator(products_list, 8) # Show 8 products per page

    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    context={
        "products" : products,
        "categories" : Category.objects.annotate(sum_prod=Count('product_category')).filter(sum_prod__gt=0)
    }

    return render(request, 'comics/products_main.html', context)


def add_cart(request, product_id):
    if request.method == 'POST':
        print request.session['shopping_cart']
        print 'hello aoeifjoaeiwjfoiejwfaowiefja;eowifjae;owieowifjaweoi;fj'
        product_details = {}
        the_product = Product.productManager.get(id=product_id)
        prod_total = int(request.POST['product_quantity']) * the_product.price
        request.session['product_total'] = (int(request.POST['product_quantity']) * the_product.price) + request.session['product_total']
        product_details = {
                'id': the_product.id,
                'name': the_product.name,
                'price': the_product.price,
                'quantity': request.POST['product_quantity'],
                'prod_total': prod_total
                }
        shopping_cart = request.session['shopping_cart']
        shopping_cart.append(product_details)
        request.session['shopping_cart'] = shopping_cart
        messages.success(request, the_product.name+' has been added to the shopping cart')
        print request.session['shopping_cart']
        return redirect('/product_spotlight/'+str(product_id))

def search_comics(request):
    if request.method == 'POST':
        # if request.POST['product_name'] == Product.productManager.filter(name_contains= request.POST['name']):
        products = Product.productManager.filter(Q(name__contains= request.POST['name']) | Q(category__name__contains= request.POST['name']))
        context = {
            "products" : products,
            "categories" : Category.objects.all(),
        }
        return render(request,'comics/products_main.html', context)

# def sort_comics(request):
#     if request.method == 'POST':
#         if request.POST['product_selection_drop_down'] == "Price":
#             products = Product.productManager.all().order_by('price')
#             context = {
#                 "products" : products,
#                 "categories" : Category.objects.all(),
#             }
#         if request.POST['product_selection_drop_down'] == "Category":
#             products = Product.productManager.order_by('category')
#             context = {
#                 "products" : products,
#                 "categories" : Category.objects.all(),
#             }
#         return render(request,'/products_main.html', context)


def product_category(request,category_id):

    products_list = Product.productManager.all()
    paginator = Paginator(products_list, 8) # Show 8 products per page

    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    context = {
        'products' : Product.productManager.filter(category__id= category_id),
        'categories': Category.objects.annotate(sum_prod=Count('product_category')).exclude(sum_prod__lt=1)
    }

    return render(request,'comics/prod_category.html', context)

def product_spotlight(request, product_id):
    product = Product.productManager.get(id=product_id)
    category_id = product.category_id
    context = {
        "the_product": product,
        "prod_total": request.session['product_total'],
        "products": Product.productManager.filter(category__id= category_id).exclude(id= product_id)
    }
    return render(request, 'comics/product_spotlight.html', context)

def shopping_cart(request):
    context = {
            #'the_product': Product.productManager.all()
            'the_product': request.session['shopping_cart'],
            'prod_total': request.session['product_total']
            }
    return render(request, 'comics/shopping_cart.html', context)

def product_adder(request):
    if 'auth' in request.session:
        if request.method=="POST":
            print request.POST
            print type(request.POST['p_price'])
            image = request.FILES['image']
            product = Product.productManager.validate_product(request.POST, image)
            if 'errors' in product:
                for error in product['errors']:
                    messages.error(request, error)
                return redirect('/dashboard/products')
            if 'the_product' in product:
                messages.success(request, "Successfully added product!")
                return redirect('/dashboard/products')
        return redirect('/dashboard/products')
    else:
        return redirect('/')

def order_create(request):
    if request.method == 'POST':
        the_order = Order.orderManager.create_order(request.POST, request.session['user_id'], request.session['shopping_cart'])
        if 'errors' in the_order:
            for error in the_order['errors']:
                messages.error(request, error)
                return redirect('/shopping_cart')
        if 'the_order' in the_order:
            print the_order
            return redirect('/charge/'+str(the_order.id))

def admin_users(request):
    if 'auth' in request.session:
        context = {
        "users": User.userManager.all()
        }
        return render(request, 'comics/users.html', context)
    else:
        return redirect('/')

def user_update(request, user_id):
    if 'auth' in request.session:
        User.userManager.filter(id=user_id).update(admin_auth=request.POST['new_auth'])
        return redirect('/dashboard/users')
    else:
        return redirect('/')

def user_delete(request, user_id):
    if 'auth' in request.session:
        User.userManager.get(id=user_id).delete()
        return redirect('/dashboard/users')
    else:
        return redirect('/')

def display_login_registration(request):
    return render(request, 'comics/login_register.html')

def user_registration(request):
    if request.method == 'POST':
        user = User.userManager.user_registration(request.POST)
        if 'errors' in user:
            for error in user['errors']:
                messages.error(request, error)
            return redirect('/register/me')
        if 'the_user' in user:
            messages.success(request, "Successfully registered")
            return redirect('/')

def user_login(request):
    if request.method == 'POST':
        # get order id somehow
        existing_user = User.userManager.validate_login(request.POST)
        if 'error' in existing_user:
            messages.error(request, existing_user['error'])
            return redirect('/')
        if 'logged_in_user' in existing_user:
            request.session['user_id'] = existing_user.id
            return redirect('/')


def display_test(request):
    # stop creating the the best product
    #Product.productManager.create(name='Superman 1 1939', description='Worth over a million dollars', image='superman', price=100.00, quantity=1)

    # stop creating the user
    #User.userManager.create(first_name='Brian', last_name='Sung', email='thisiscool@gmail.com', password='Thisisapassword')

    #the_user = User.userManager.get(id=2)
    the_order = Order.orderManager.get(id=1)
    #the_product = Product.productManager.get(id=10)
    #the_order = Order.orderManager.create(s_fname='Dan', s_lname='Smith', total=4.00, user=the_user, status=0)
    #the_order.products.add(the_product)
    #the_order.save()
    context = {
            'order': the_order,
            'products': Product.productManager.all(),
            'order_products': the_order.products.all()
            }
    return render(request, 'comics/product_test.html', context)

def product_edit(request, product_id):
    if 'auth' in request.session:
        context = {
        "product": Product.productManager.get(id=product_id),
        "categories": Category.objects.all()
        }
        print context['product'].description
        return render(request, 'comics/product_edit.html', context)
    else:
        return redirect('/')

def product_delete(request, product_id):
    if 'auth' in request.session:
        Product.productManager.get(id=product_id).delete()
        print "Successfully deleted " + product_id
        return redirect('/dashboard/products')
    else:
        return redirect('/')

def product_update(request, product_id):
    if 'auth' in request.session:
        if request.method=="POST":
            update_product = Product.productManager.update_product(request.POST, product_id)
        return redirect('/dashboard/products')
    else:
        return redirect('/')

# ============== #
# === STRIPE === #
# ============== #
@csrf_exempt
def charge(request,order_id):
    order = Order.orderManager.get(id=order_id)
    if 'total' not in request.session:
        request.session['total'] = 'null'
    request.session['total'] = order.id
    print order.total
    context = {
        'orders' : Order.orderManager.filter(id=order_id)
    }
    # if 'total' not in request.session:
    #     request.session['total'] = 300
    # request.session['total'] = 4000
    # # the_amount = request.session['total']
    # # print the_amount
    # if request.method == "POST":
    #     # total = charge_me(10000)
    #     form = SalePaymentForm(request.POST)
    #
    #     if form.is_valid(): # charges the card
    #         sale = Sale()
    #         sale.charge(100000,4242424242424242,01,2019,424)
    #         return HttpResponse("Success! We've charged your card!")
    # else:
    #     form = SalePaymentForm()

    return render(request , "includes/card.html" , context)

def charge_process(request,order_id):
    if request.method == 'POST':
        # sale = sale()
        # card = sale.validate_card(request.POST)
        if not NO_LET_REGEX.match(request.POST['number']):
            # error.msgs.append('Card Number invalid')
            messages.error(request,'Card Number invalid')
            return redirect('/charge/' + str(order_id))
        if len(request.POST['number']) != 16:
            # error.msgs.append('Card number invalid')
            messages.error(request,'Card number invalid')
            return redirect('/charge/' + str(order_id))
        if len(request.POST['cvc']) != 3:
            # error.msgs.append('CVC is invalid')
            messages.error(request,'CVC is invalid')
            return redirect('/charge/' + str(order_id))

        # if 'errors' in card:
        #     for error in card['errors']:
        #         messages.error(request,error)
        #     return redirect('/charge/' + str(order_id))
        # if 'validated_card' in card:

        order = Order.orderManager.get(id=order_id)
        total_amount = order.total

        #total_amount = request.session['total']

        sale = Sale()
        sale.charge(total_amount,request.POST['number'],request.POST['exp_month'],request.POST['exp_year'],request.POST['cvc'])
        return redirect('/order/success')

# ===================== #
# === END OF STRIPE === #
# ===================== #

def order_success(request):
    return render(request,'comics/success.html')
def register_me(request):
    return render(request,'comics/reg.html')
