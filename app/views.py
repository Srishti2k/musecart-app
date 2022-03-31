from django.shortcuts import render, redirect , HttpResponse
from django.http import JsonResponse
from django.db.models import Q
from django.views import View
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
    def get(self, request):
        topwear = Product.objects.filter(category = 'TW')
        bottomwear = Product.objects.filter(category = 'BW')
        mobile = Product.objects.filter(category = 'M')
        laptop = Product.objects.filter(category = 'L')

        context = {'topwear' : topwear , 'bottomwear' : bottomwear , 'mobile' : mobile , 'laptop' : laptop}

        return render(request , 'app/home.html' , context)


class product_detail(View):
	def get(self, request, pk):
		#totalitem = 0
		product = Product.objects.get(pk=pk)
		#print(product.id)
		item_already_in_cart=False
		if request.user.is_authenticated:
			#totalitem = len(Cart.objects.filter(user=request.user))
			item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
		return render(request, 'app/productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart})

def add_to_cart(request):
	user = request.user
	product = request.GET.get('prod_id')
	product_title = Product.objects.get(id=product)
	Cart(user=user, product=product_title).save()
	#messages.success(request, 'Product Added to Cart Successfully !!' )
    
	return redirect('/showcart')
	#else:
		#return redirect('/cart')
  # Below Code is used to return to same page
  # return redirect(request.META['HTTP_REFERER'])

def showcart(request):
	totalitem = 0
	if request.user.is_authenticated:
		#totalitem = len(Cart.objects.filter(user=request.user)) 
		user = request.user
		cart = Cart.objects.filter(user=user) #this gives query set
		amount = 0.0
		shipping_amount = 70.0
		totalamount=0.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user] #gives list/array of all the products issued by current user
		#print(cart_product)
		if cart_product: #agar products hai to
			for p in cart_product: #pick one by one  product
				tempamount = (p.quantity * p.product.discount_price) #and find price of each = (price *quantity of product)
				amount += tempamount #keep ading price of 1 product to another for calculating total
			totalamount = amount+shipping_amount #add shipping charges also
			return render(request, 'app/addtocart.html', {'cart':cart, 'amount':amount, 'totalamount':totalamount,})
		else:
			return render(request, 'app/emptycart.html',)
	else:
		return render(request, 'app/emptycart.html',)

def plus_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quantity+=1
		c.save()
		amount = 0.0
		shipping_amount= 70.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discount_price)
			amount += tempamount
		data = {
			'quantity':c.quantity,
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")

def minuscart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quantity-=1
		c.save()
		amount = 0.0
		shipping_amount= 70.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discount_price)
			amount += tempamount
		
		data = {
			'quantity':c.quantity,
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")


def removecart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
	
		c.delete()
		amount = 0.0
		shipping_amount= 70.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discount_price)
			amount += tempamount
		
		data = {
			
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")



def buy_now(request):
 return render(request, 'app/buynow.html')

#@method_decorator(login_required, name='dispatch')
class ProfileView(View):
	def get(self, request):
         form = CustomerProfileForm()
         return render(request, 'app/profile.html' , {'form' : form, 'active' : 'btn-primary'})
		
	def post(self, request):
		form = CustomerProfileForm(request.POST)
		if form.is_valid():
			usr = request.user
			name  = form.cleaned_data['name']
			locality = form.cleaned_data['locality']
			city = form.cleaned_data['city']
			state = form.cleaned_data['state']
			zipcode = form.cleaned_data['zipcode']
			reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
			reg.save()
			messages.success(request, 'Congratulations!! Profile Updated Successfully.')
		return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})


#@login_required
def address(request):
    details= Customer.objects.filter(user= request.user)
    return render(request, 'app/address.html' , {'details' : details , 'active' : 'btn-primary'}) 

#@login_required
def orders(request):
 return render(request, 'app/orders.html')

#@login_required
def change_password(request):
 return render(request, 'app/changepassword.html')


def mobile(request, data=None):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	if data==None :
			mobiles = Product.objects.filter(category='M')
	elif data == 'redmi' or data == 'samsung':
			mobiles = Product.objects.filter(category='M').filter(brand=data)
	elif data == 'below':
			mobiles = Product.objects.filter(category='M').filter(discount_price__lt=10000)
	elif data == 'above':
			mobiles = Product.objects.filter(category='M').filter(discount_price__gt=10000)
	return render(request, 'app/mobile.html', {'mobiles':mobiles, 'totalitem':totalitem})
	

def login(request):
 return render(request, 'app/login.html')

class customerregistration(View):
    def get(self, request): 
        form= CustomerRegistrationForm()
        context = {'form' : form}
        return render(request, 'app/customerregistration.html' , context )
    def post(self, request):
        form= CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Account has been registered!!')
            form.save()
            return render(request, 'app/customerregistration.html')

        context = {'form' : form}
        return render(request, 'app/customerregistration.html' , context )

#@login_required
def checkout(request):
	user = request.user
	add = Customer.objects.filter(user=user)
	cart_items = Cart.objects.filter(user=user)
	amount = 0.0
	shipping_amount = 70.0
	totalamount=0.0
	cart_product = [p for p in Cart.objects.all() if p.user == request.user]
	if cart_product:
		for p in cart_product:
			tempamount = (p.quantity * p.product.discount_price)
			amount += tempamount
		totalamount = amount+shipping_amount
	return render(request, 'app/checkout.html', {'cart_items':cart_items , 'add' : add , 'totalamount' : totalamount })


#@login_required(login_url='/login/')
def payment_done(request):
	custid = request.GET.get('custid')
	print("Customer ID", custid)
	user = request.user
	cartid = Cart.objects.filter(user = user)
	customer = Customer.objects.get(id=custid)
	print(customer)
	for cid in cartid:
		OrderedPlaced(user=user, customer=customer, product=cid.product, quantity=cid.quantity).save()
		print("Order Saved")
		cid.delete()
		print("Cart Item Deleted")
	return redirect("orders")

#@login_required(login_url='/accounts/login/')
def orders(request):
	op = OrderedPlaced.objects.filter(user=request.user)
	return render(request, 'app/orders.html', {'order_placed':op})