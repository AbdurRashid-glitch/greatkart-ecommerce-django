from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart,CartItem
# Create your views here.


def _cart_id(request): # _cart_id is a private function
    cart = request.session.session_key # get the session_id 
    if not cart:
        cart = request.session.create() # create a new session
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id) # get the product using product_id
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request) ) # get cart using the cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()
    # combining product(s) into cart:
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1 # increment by 1 after each item added
        cart_item.save() # save it into database
    except CartItem.DoesNotExist: # Creating a new Cart Item:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        cart_item.save()
    
    return redirect('cart')

def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity >1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def delete_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart) # to get the cart item
    cart_item.delete()
    return redirect('cart') # redirect to the cart page

def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) # taking cart object by cart_id
        cart_items = CartItem.objects.filter(cart=cart, is_active=True) # getting cart items
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity) # total of each cart item
            quantity += cart_item.quantity # total quantity of each cart item
        tax = ( 2 * total)/100 # how much tax you want to apply, here 2%
        grand_total = total + tax
    except:
        pass
    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)