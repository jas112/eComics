from __future__ import unicode_literals
from django.db import models
from decimal import Decimal
import re
import bcrypt
# import settings
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
CHAR_DIGIT_REGEX = re.compile(r'^[a-zA-Z0-9_.-]*$')
CATEGORY_REGEX = re.compile(r'^[A-Za-z]*$')
PRICE_REGEX = re.compile(r'^(?!0+(\.0+)?$)\d{0,5}(.\d{1,2})?$')
NO_LET_REGEX = re.compile(r'^[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[A-Za-z\s]{1,}[\.]{0,1}[A-Za-z\s]{0,}$')
STREET_ADDRESS_REGEX = re.compile(r'\b[0-9]{1,3}(?:\s\p{L}+)+')
PRODUCT_REGEX = re.compile(r'[^ ][ A-Za-z\d\D]*$')
class UserManager(models.Manager):
    def admin_login(self, post_data):
        error_msgs = []
        if User.userManager.get(email=post_data['email']) and User.userManager.get(email=post_data['email']).admin_auth:
            stored_pw = User.userManager.get(email=post_data['email']).password
            if stored_pw == post_data['password']:
                return {"admin": User.userManager.get(email=post_data['email'])}
            else:
                error_msgs.append("Invalid Login")
                return {"errors":error_msgs}
        else:
            error_msgs.append("Invalid Login")
            return {"errors":error_msgs}

    def user_login(self, post_data):
        error_msgs = []
        if User.userManager.get(email=post_data['email']):
            stored_pw = User.userManager.get(email=post_data['email']).password
            if stored_pw == post_data['password']:
                return {"theuser": User.userManager.get(email=post_data['email'])}
            else:
                error_msgs.append("Invalid Login")
                return {"errors":error_msgs}
        else:
            error_msgs.append("Invalid Login")
            return {"errors":error_msgs}

    def user_registration(self, post_data):
        error_msgs = []
        u_fname = post_data['u_fname']
        u_lname = post_data['u_lname']
        u_email = post_data['u_email']
        u_pw = post_data['u_pw']
        u_confirm_pw = post_data['u_confirm_pw']
        u_addr_street = post_data['u_addr_street']
        u_street_two = post_data['u_street_two']
        u_addr_city = post_data['u_addr_city']
        u_addr_state = post_data['u_addr_state']
        u_addr_zip = post_data['u_addr_zip']
        if len(u_fname) < 1:
            error_msgs.append('First name field is blank')
        elif len(u_fname) < 2:
            error_msgs.append('First name is too short')
        elif not NAME_REGEX.match(u_fname):
            error_msgs.append('First name field is blank')
        if len(u_lname) < 1:
            error_msgs.append('Last name field is blank')
        elif len(u_lname) < 2:
            error_msgs.append('Last name is too short')
        elif not NAME_REGEX.match(u_lname):
            error_msgs.append('Last name field is blank')
        if len(u_email) < 1:
            error_msgs.append('Email address field is blank')
        elif not EMAIL_REGEX.match(u_email):
            error_msgs.append('Invalid email address')
        if len(u_pw) < 1:
            error_msgs.append('Password field is blank')
        elif len(u_pw) < 8:
            error_msgs.append('Password must be 8 characters or longer')
        if u_pw != u_confirm_pw:
            error_msgs.append('Passwords do not match')
        if len(u_addr_street) < 1:
            error_msgs.append('Address field is blank')
        elif not STREET_ADDRESS_REGEX.match(u_addr_street):
            error_msgs.append('Invalid street address')
        if len(u_addr_city) < 1:
            error_msgs.append('City field is blank')
        # u_addr_city regex
        elif not NAME_REGEX.match(u_addr_city):
            error_msgs.append('Invalid city name')
        if len(u_addr_state) < 1:
            error_msgs.append('State field is blank')
        # u_addr_state regex
        if len(u_addr_zip) < 1:
            error_msgs.append('Zip code field is blank')
        # u_addr_zip regex
        if error_msgs:
            return {'errors': error_msgs}
        else:
            pw = u_pw.encode('utf-8')
            hashed = bcrypt.hashpw(pw, bcrypt.gensalt())
            user_location = Location.objects.create(addr_street=u_addr_street, street_two=u_street_two, addr_city=u_addr_city, addr_state=u_addr_state, addr_zip=u_addr_zip)
            the_user = User.objects.create(first_name=u_fname, last_name=u_lname, email=u_email, password=hashed, user_location=user_location)
            return {'the_user': the_user}


class OrderManager(models.Manager):
    def create_order(self, post_data, user_id, shopping_cart):
        error_msgs = []
        product_total = 0
        # shipping information
        s_fname = post_data['s_fname']
        s_lname = post_data['s_lname']
        s_addr_street = post_data['s_addr_street']
        s_street_two = post_data['s_street_two']
        s_addr_city = post_data['s_addr_city']
        s_addr_state = post_data['s_addr_state']
        s_addr_zip = post_data['s_addr_zip']
        if len(s_fname) < 1:
            error_msgs.append('First name field is blank')
        elif len(s_fname) < 2:
            error_msgs.append('First name is too short')
        elif not NAME_REGEX.match(s_fname):
            error_msgs.append('First name field is blank')
        if len(s_lname) < 1:
            error_msgs.append('Last name field is blank')
        elif len(s_lname) < 2:
            error_msgs.append('Last name is too short')
        elif not NAME_REGEX.match(s_lname):
            error_msgs.append('Last name field is blank')
        if len(s_addr_street) < 1:
            error_msgs.append('Address field is blank')
        #elif not STREET_ADDRESS_REGEX.match(s_addr_street):
            #error_msgs.append('Invalid street address')
        if len(s_addr_city) < 1:
            error_msgs.append('City field is blank')
        # u_addr_city regex
        elif not NAME_REGEX.match(s_addr_city):
            error_msgs.append('Invalid city name')
        # u_addr_state regex
        if len(s_addr_zip) < 1:
            error_msgs.append('Zip code field is blank')
        # u_addr_zip regex
        if error_msgs:
            return {'errors': error_msgs}
        else:
            shipping_location = Location.objects.create(addr_street=s_addr_street, street_two=s_street_two, addr_city=s_addr_city, addr_state=s_addr_state, addr_zip=s_addr_zip)
            the_user = User.userManager.get(id=user_id)
            the_order = Order.orderManager.create(s_fname=s_fname, s_lname=s_lname, user=the_user, shipping_location=shipping_location)
            the_order.user.add(the_user)
            for product in shopping_cart:
                # add product to order object
                the_product = Product.productManager.get(id=product.id)
                product_total += the_product.price
                the_order.products.add(the_product)
            # depending on what we return, change this following line
            the_order.total.add(product_total)
            return {'the_order': the_order}

class ProductManager(models.Manager):
    def validate_product(self, post_data, submitted_image):
        error_msgs = []
        p_name = post_data['p_name']
        p_description = post_data['p_description']
        if 'p_category' in post_data:
            p_category = post_data['p_category']
        new_p_category = post_data['new_p_category']
        p_price = Decimal(post_data['p_price'])
        p_quantity = int(post_data['p_quantity'])
        print submitted_image
        if len(p_name) < 2:
            error_msgs.append('Product name must be 2 or more characters')
        elif not PRODUCT_REGEX.match(p_name):
            error_msgs.append('Invalid product name')
        if len(p_description) < 1:
            error_msgs.append('Product description cannot be blank')
        if not CATEGORY_REGEX.match(new_p_category):
            error_msgs.append('Invalid category')
        # price form
        if p_price < 0:
            error_msgs.append('Cannot have negative price')
        elif p_price >= 1000:
            error_msgs.append('Price must be between $0 and $999.99')
        if not submitted_image:
            error_msgs.append('You failed to upload a picture')
        if new_p_category:
            category = new_p_category
        else:
            category = p_category
        # regex for price
        # elif not PRICE_REGEX.match(p_price):
        #     error_msgs.append('Invalid price')
        if error_msgs:
            return {'errors': error_msgs}
        else:
            if new_p_category:
                new_cat = Category.objects.create(name=category)
                the_product = Product.productManager.create(name=p_name, description=p_description, image=submitted_image, price=p_price, quantity=p_quantity, category=new_cat)
            else:
                old_cat = Category.objects.get(name=category)
                the_product = Product.productManager.create(name=p_name, description=p_description, image=submitted_image, price=p_price, quantity=p_quantity, category=old_cat)
            # depending on what we return
            return {'the_product': the_product}

    def update_product(self, post_data, product_id):
        error_msgs = []
        new_name = post_data['edit_name']
        new_desc = post_data['edit_description']
        if 'edit_category' in post_data:
            edit_category = post_data['edit_category']
        new_edit_category = post_data['new_edit_category']
        new_price         = post_data['edit_price']
        new_quantity      = post_data['edit_quantity']
        if new_edit_category:
            new_cat = Category.objects.create(name=new_edit_category)
            Product.productManager.filter(id=product_id).update(name=new_name, description=new_desc, price=new_price, quantity=new_quantity, category=new_cat)
        else:
            old_category = Category.objects.get(name=edit_category)
            Product.productManager.filter(id=product_id).update(name=new_name, description=new_desc, price=new_price, quantity=new_quantity, category=old_category)

class User(models.Model):
    email       =   models.CharField(max_length=100, default=None)
    password    =   models.CharField(max_length=100, default=None)
    first_name  =   models.CharField(max_length=60)
    last_name   =   models.CharField(max_length=60)
    admin_auth  =   models.BooleanField(default=False)
    created_at  =   models.DateTimeField(auto_now_add=True)
    updated_at  =   models.DateTimeField(auto_now=True)
    userManager =   UserManager()

class Category(models.Model):
    name        =   models.CharField(max_length=60)
    created_at  =   models.DateTimeField(auto_now_add=True)
    updated_at  =   models.DateTimeField(auto_now=True)

class Product(models.Model):
    name        =   models.CharField(max_length=60)
    description =   models.TextField(max_length=1000)
    image       =   models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/default.jpg')
    #price       =   models.DecimalField(max_digits=5,decimal_places=2)
    price       =   models.IntegerField(default=0)
    quantity    =   models.IntegerField(default=0)
    created_at  =   models.DateTimeField(auto_now_add=True)
    updated_at  =   models.DateTimeField(auto_now=True)
    category    =   models.ForeignKey(Category, related_name="product_category", default=None)
    productManager = ProductManager()

class Order(models.Model):
    products    =   models.ManyToManyField(Product, related_name="product_orders")
    user        =   models.ForeignKey(User, related_name="user_orders")
    s_fname     =   models.CharField(max_length=60, default=None)
    s_lname     =   models.CharField(max_length=60, default=None)
    total       =   models.IntegerField(default=0)
    status      =   models.IntegerField(default=0)
    created_at  =   models.DateTimeField(auto_now_add=True)
    updated_at  =   models.DateTimeField(auto_now=True)
    orderManager = OrderManager()

class Location(models.Model):
    addr_street =   models.CharField(max_length=100)
    street_two  =   models.CharField(max_length=100, default=None)
    addr_city   =   models.CharField(max_length=100)
    addr_state  =   models.CharField(max_length=20)
    addr_zip    =   models.IntegerField()
    user        =   models.OneToOneField(User, related_name='user_location')
    order       =   models.OneToOneField(Order, related_name='shipping_location')

# ============== #
# === STRIPE === #
# ============== #
class Sale(models.Model):
    def __init__(self, *args, **kwargs):
        super(Sale, self).__init__(*args, **kwargs)

        # bring in stripe, and get the api key from settings.py
        import stripe
        stripe.api_key = "sk_test_5HJSvP0XKmzN122N5ntJ3zfM"

        self.stripe = stripe

    # store the stripe charge id for this sale
    charge_id = models.CharField(max_length=32)

    # you could also store other information about the sale
    # but I'll leave that to you!

    def charge(self, price_in_cents, number, exp_month, exp_year, cvc):
        """
        Takes a the price and credit card details: number, exp_month,
        exp_year, cvc.

        Returns a tuple: (Boolean, Class) where the boolean is if
        the charge was successful, and the class is response (or error)
        instance.
        """

        if self.charge_id: # don't let this be charged twice!
            return False, Exception(message="Already charged.")

        try:
            response = self.stripe.Charge.create(
                amount = price_in_cents,
                currency = "usd",
                card = {
                    "number" : number,
                    "exp_month" : exp_month,
                    "exp_year" : exp_year,
                    "cvc" : cvc,

                    #### it is recommended to include the address!
                    #"address_line1" : self.address1,
                    #"address_line2" : self.address2,
                    #"daddress_zip" : self.zip_code,
                    #"address_state" : self.state,
                },
                description='Thank you for your purchase!')

            self.charge_id = response.id

        except self.stripe.CardError, ce:
            # charge failed
            return False, ce

        return True, response

    def validate_card(request, post_data):
        error_msgs=[]
        if not NO_LET_REGEX.match(post_data['number']):
            error.msgs.append('Card Number invalid')
        if len(post_data['number']) < 16:
            error.msgs.append('Card number invalid')
        if len(post_data['cvc']) != 3:
            error.msgs.append('CVC is invalid')

        if error_msgs:
            return {'errors',error_msgs}
        else:
            return {'validated_card': 'validated'}

# ===================== #
# === END OF STRIPE === #
# ===================== #
