from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.db.models import Q , Count
import razorpay
from django.conf import settings
from django.views import View

from Admin.models import Product,Category,Customer,Cart,Payment,OrderPlaced,Wishlist
from .forms import Registration,CustomerForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

def homepage(request):
    cats = Category.objects.all()
    Products = Product.objects.all()
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,'index.html',locals())
@login_required
def ShowPdt(request,id):
    id = Category.objects.get(id=id)
    cats = Category.objects.all()
    Products = Product.objects.filter(cat = id)
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render (request,'index.html',{"cats":cats,"Products":Products})


def ViewDetails(request,id):
    Products = Product.objects.get(id=id)
    user = request.user                     # (Field Id Expected Number) Debug Point
    user_id = user.id
    wishlist = Wishlist.objects.filter(Q(product=Products) & Q(user_id = user.id))
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render (request,'ViewDetails.html',locals())

def signup(request):
    if(request.method == "GET"):
        form = Registration()
        return render(request,'signup.html',{'form':form})
    else:
        form = Registration(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulation ! User Register Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,'signup.html',{'form':form})
    
def profile(request):
    if(request.method == "GET"):
        form = CustomerForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request,'profile.html',{'form':form})
    else:
        form = CustomerForm(request.POST)
        if form.is_valid():
            user= request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user,name=name,locality=locality,city=city,mobile=mobile,
                           state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulation ! Profile Save Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,'profile.html',{})
    

def Address(request):
    if(request.method == 'GET'):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        add = Customer.objects.filter(user=request.user)
        return render (request,'address.html',{'add':add})

def update(request,id):
    if(request.method == 'GET'):
        add = Customer.objects.get(id=id)
        form = CustomerForm(instance=add)
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render (request,'update.html',{'form':form})
    else:
        form = CustomerForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(id=id)
            add.user= request.user
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congratulation ! Profile Save Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect(Address)
        #return render (request,'address.html',{})
@login_required
def cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return redirect(showcart)

@login_required
def showcart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.price
        amount = amount + value
    totalamount = amount + 50
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,'addcart.html',locals())

def checkout(request):
    if(request.method == "GET"):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.price
            famount = famount + value
        totalamount = famount +50
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount":razoramount,"currency": "INR","receipt":"order_receipt_12"}
        payment_response = client.order.create(data=data)
        print(payment_response)
        {'id': 'order_LbaDYoTA83Jddz', 'entity': 'order', 'amount': 184900, 'amount_paid': 0, 'amount_due': 184900, 'currency': 'INR', 'receipt': 'order_receipt_12', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1681019349}
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user=user,
                amount = totalamount,
                razorpay_order_id = order_id,
                razorpay_payment_status = order_status
            ) 
            payment.save()

        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))

        return render(request,'checkout.html',locals())
    
def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    
    customer = Customer.objects.get(id=cust_id)
    #To update payment status and payment_id
    payment = Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    #To save order details
    user = request.user                     # (Field Id Expected Number) Debug Point
    user_id = user.id
    cart = Cart.objects.filter(user_id=user_id)
    for c in cart:
        OrderPlaced(user_id=user_id,customer=customer,product=c.product,quantity = c.quantity,payment=payment).save()
        c.delete()
    return redirect(orders)

def orders(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    user = request.user
    user_id = user.id
    order_placed = OrderPlaced.objects.filter(user_id=user_id)
    return render(request,'orders.html',locals())





def pluscart(request):

    if (request.method == 'GET'):
        prod_id = request.GET["prod_id"]
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.price
            amount = amount + value
        totalamount = amount + 50
        data = {
            'quantity':c.quantity,
            'amount' : amount,
            'totalamount' : totalamount
        }
        return JsonResponse(data)
    else:
        pass
    
def minuscart(request):
    if(request.method == 'GET'):
        prod_id = request.GET["prod_id"]
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.price
            amount = amount + value
        totalamount = amount + 50
        data = {
            'quantity':c.quantity,
            'amount' : amount,
            'totalamount' : totalamount
        }
        return JsonResponse(data)

def removecart(request):
    if request.method == 'GET':
        prod_id = request.GET["prod_id"]
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.price
            amount = amount + value
        totalamount = amount + 50
        data = {
            'amount' : amount,
            'totalamount' : totalamount
        }
        return JsonResponse(data)

def search(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    query = request.GET["search"]
    product = Product.objects.filter(Q(pname__icontains=query))
    return render(request,'search.html',locals())

def plus_wishlist(request):
    if(request.method == "GET"):
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user,product=product).save()
        data = {
            'message':'Wishlist Added Successfully'
        }
        return JsonResponse(data)
    
def minus_wishlist(request):
    if(request.method == "GET"):
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user,product=product).delete()
        data = {
            'message':'Wishlist Remove Successfully'
        }
        return JsonResponse(data)

@login_required
def show_wishlist(request):
    user = request.user
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    product = Wishlist.objects.filter(user=user)
    return render(request,"wishlist.html",locals())

