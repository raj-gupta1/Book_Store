from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http import HttpResponse
from .models import Product,Category,Customer,Order
from django.contrib.auth.hashers import make_password,check_password
from django.views import View
from store.middlewares.auth import auth_middleware
# Create your views here.
# print(make_password('1234'))
# print(check_password('1234','pbkdf2_sha256$260000$13ogOr81RXXowrVUXv6SeC$xux9inZYGXShlFgK/uCWmh9rqJAVj4my7f0+fDqXc7g='))

class Index(View):
    def get(self,request):
        cart=request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        categories=Category.get_all_categories()
        products = None
        # print(products)
        categoryID=request.GET.get('category')
        if categoryID:
            products = Product.get_products_by_id(categoryID)
        else:
            products = Product.get_all_products()
        data= {}
        data['products']=products
        data['categories']=categories
        # print('you are:',request.session.get('email'))
        
        return render(request,'index.html',data)

    def post(self,request):
        product = request.POST.get('product')
        remove=request.POST.get('remove')

        cart=request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1
                    
                else:
                    cart[product] = quantity+1
            else:
                cart[product] = 1

            
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('Cart data is',request.session['cart'])
        return redirect('homepage')
        






# def index(request):
#     categories=Category.get_all_categories()
#     products = None
#     # print(products)
#     categoryID=request.GET.get('category')
#     if categoryID:
#         products = Product.get_products_by_id(categoryID)
#     else:
#         products = Product.get_all_products()
#     data= {}
#     data['products']=products
#     data['categories']=categories
#     print('you are:',request.session.get('email'))
    
#     return render(request,'index.html',data)

#     if request.method=='POST':
#         print(request.POST)

def validate(customer):
    error_mssg=None
    fname=customer.first_name
    lname=customer.last_name
    
    if(not fname):
        error_mssg="First Name Required !!"
    elif len(fname)<2:
        error_mssg="First Name must be 2 character long"
    elif(not lname):
        error_mssg="Last Name Reguired"
    elif len(lname)<2:
        error_mssg="Last Name must be 2 character Long"
    elif(not customer.phone):
        error_mssg="Phone number required"
    elif len(customer.phone)<10:
        error_mssg="Phone Number must be 10 char Long"
    elif(not customer.email):
        error_mssg="Email Required"
    elif customer.email.find("@gmail.com")==-1:
        error_mssg="Not a Valid Email"
    elif len(customer.email)<11:
        error_mssg="Email must have 11 characters"
    elif(not customer.password):
        error_mssg="Password Required"
    elif len(customer.password)<5:
        error_mssg="Password must be 5 character long"
    elif customer.isExist():
        error_mssg = "Email already registered"
    return error_mssg


def signup(request):
    if request.method == 'GET':

        return render(request,'signup.html')
    else:
        fname=request.POST.get('firstname')
        lname=request.POST.get('lastname')
        phone=request.POST.get('phonenumber')
        email=request.POST.get('email')
        password=request.POST.get('password')
        #validation
        value={
            'fname':fname,
            'lname':lname,
            'phone':phone,
            'email':email
        }
        error_mssg=None
        customer = Customer(first_name=fname,last_name=lname,phone=phone,email=email,password=password)
        error_mssg = validate(customer)

        if not error_mssg:
            customer.password=make_password(customer.password)
            customer.save()
            return redirect('homepage')
        else:
            data={
                'error':error_mssg,
                'values':value
            }
            return render(request,'signup.html',data)
        

# def login(request):


    if request.method == 'GET':
        return render(request,'login.html')
    else:
        email = request.POST.get('email')
        password=request.POST.get('password')
        try:
            customer = Customer.objects.get(email=email)
        except:
            customer = False
        error_mssg = None
        if customer:
            flag = check_password(password,customer.password)
            if flag:
                return redirect('homepage')
            else:
                error_mssg = "Wrong Password Entered"
        else:
            error_mssg = "Email is not registered"

        print(customer)
        return render(request,'login.html',{'error':error_mssg})

class Login(View):
    
    def get(self,request):
        
        return render(request,'login.html')
    
    def post(self,request):
        email = request.POST.get('email')
        password=request.POST.get('password')
        try:
            customer = Customer.objects.get(email=email)
        except:
            customer = False
        error_mssg = None
        if customer:
            flag = check_password(password,customer.password)
            if flag:
                request.session['customer_id']=customer.id
                request.session['email']=customer.email
                
                return redirect('homepage')
            else:
                error_mssg = "Wrong Password Entered"
        else:
            error_mssg = "Email is not registered"

        return render(request,'login.html',{'error':error_mssg})

def logout(request):
    request.session.clear()
    return redirect('homepage')

def cart(request):
    try:
        ids=list(request.session.get('cart').keys())
        # print(ids)
    except:
        request.session['cart'] = {}
        ids=list(request.session.get('cart').keys())
    products=Product.get_products(ids)
    return render(request,'cart.html',{'products':products,})

def checkout(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer_id')
        cart = request.session.get('cart')
        products = Product.get_products(list(cart.keys()))
        # print(address,phone,customer,cart,products)

        for product in products:
            order = Order(customer=Customer.objects.get(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
            order.save()
        
        request.session['cart'] = {}

        return redirect('cart')

# @auth_middleware
def orders(request):
    if request.method=='GET':
        customer=request.session.get('customer_id')
        order = Order.get_orders_by_customer(customer)
        # print(order)
        order.reverse()
        return render(request,'orders.html',{'orders':order})

