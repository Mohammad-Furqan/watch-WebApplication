from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import F, Sum
from watches.models import Watch ,Cart, CartItem,Order,OrderItem,Contact
from django.contrib import messages
from users.models import UserDetail
from users.forms import AddressUpdateForm
# Create your views here.
# /views.py


def watch_list(request):
    watches = Watch.objects.all()
    return render(request, 'watch_list.html', {'watches': watches})

def watch_detail(request, watch_id):
    watch = get_object_or_404(Watch, pk=watch_id)
    return render(request, 'watch_detail.html', {'watch': watch})

def get_featured_watches():
    # attribute set to True
    return Watch.objects.filter(is_featured=True)

def home(request):
    featured_watches = get_featured_watches()
    return render(request, 'home.html', {'featured_watches': featured_watches})

def invoice(request, order_uuid):
    order = get_object_or_404(Order, order_uuid=order_uuid)
    return render(request, 'invoice.html', {'order': order})
 


def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    # Calculate total price for each item before passing it to the template
    for item in cart_items:
        item.total_price = item.watch.price * item.quantity
    # Calculate total price for all items in the cart
    total_cart_price = cart_items.aggregate(total_price=Sum(F('watch__price') * F('quantity')))['total_price'] or 0
    return render(request, 'cart.html', {'cart_items': cart_items, 'cart': cart, 'total_cart_price': total_cart_price})




def add_to_cart(request, watch_id):
    watch = get_object_or_404(Watch, pk=watch_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, watch=watch)
    
    # Increment quantity only if the item was not already in the cart
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    

    
    return redirect(('cart'))



def remove_from_cart(request, watch_id):
    if request.method == 'GET' and 'action' in request.GET and request.GET['action'] == 'remove':
        watch = get_object_or_404(Watch, pk=watch_id)
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=cart, watch=watch)
        cart_item.delete()

        messages.success(request, f'{watch.name} removed from your cart.')

    return redirect('cart')

def update_cart(request, watch_id):
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        if quantity:
            watch = get_object_or_404(Watch, pk=watch_id)
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(cart=cart, watch=watch)
            cart_item.quantity = quantity
            cart_item.save()

            messages.success(request, f'Cart updated successfully. Quantity:: {cart_item.quantity} ::')

    # If the request method is not POST or if there's an issue with the request, redirect to the cart
    return redirect('cart')



# ...

def checkout(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    for item in cart_items:
        item.total_price = item.watch.price * item.quantity

    total_cart_price = cart_items.aggregate(total_price=Sum(F('watch__price') * F('quantity')))['total_price'] or 0
    user_detail = UserDetail.objects.get(user=request.user)

    # Initialize the address update form with the user's current address
    address_form = AddressUpdateForm(instance=user_detail)

    if request.method == 'POST':
        # Process the form submission for address update
        address_form = AddressUpdateForm(request.POST, instance=user_detail)
        if address_form.is_valid():
            address_form.save()
            return redirect('checkout')

    return render(request, 'checkout.html', {
        'cart': cart,
        'cart_items': cart_items,
        'total_cart_price': total_cart_price,
        'user_address': user_detail.address,
        'address_form': address_form,  # Pass the address update form to the template
    })


def order_list(request):
    # Retrieve orders for the current user
    orders = Order.objects.filter(user=request.user)

    return render(request, 'order_list.html', {'orders': orders})

def invoice_page(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'invoice_page.html', {'orders': orders})

def download_invoice(request, order_uuid):
    order = get_object_or_404(Order, order_uuid=order_uuid)

    # Generate invoice content
    invoice_content = f"Order ID: {order.order_uuid}\n"
    invoice_content += f"Status: {'Paid' if order.payment_successful else 'Pending'}\n\n"

    for item in order.orderitem_set.all():
        invoice_content += f"{item.watch.name} x {item.quantity} - ${item.total_price}\n"

    invoice_content += f"\nTotal: ${order.total_price}"

    # Create a response with the invoice content
    response = HttpResponse(invoice_content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename=invoice_{order.order_uuid}.txt'

    return response


def dummy_payment(request):
    return render(request, 'dummy_payment.html')

# def process_payment(request):
#     # Perform any necessary actions related to the payment (in a real application)
#     messages.success(request, 'Payment successful!')
#     return render(request, 'payment_successful.html')

def process_payment(request):
    # Perform any necessary actions related to the payment (in a real application)

    # Simulate a successful payment (replace with your actual logic)
    if True:  # Replace with your actual logic to determine if the payment was successful
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)

        # Calculate total price for each item before passing it to the template
        for item in cart_items:
            item.total_price = item.watch.price * item.quantity

        total_cart_price = cart_items.aggregate(total_price=Sum(F('watch__price') * F('quantity')))['total_price'] or 0

        # Save the cart before creating the order and order items
        cart.save()

        order = Order.objects.create(user=request.user, total_price=total_cart_price)

        for item in cart_items:
            OrderItem.objects.create(order=order, watch=item.watch, quantity=item.quantity, total_price=item.total_price)

        # Clear the cart items
        cart.items.clear()
        
        order.payment_successful = True
        order.save()


        messages.success(request, 'Payment successful! Order placed successfully!')

        # Redirect to the cart page after successful payment
        #return redirect('cart')
        return render(request, 'payment_successful.html')
    # If the payment is not successful, you might want to handle it accordingly
    else:
        messages.error(request, 'Payment failed. Please try again.')
        return render(request, 'payment_failed.html')  # You can create a template for payment failure



def cancel_order(request, id):
    try:
        order = Order.objects.get(id=id)
        # Performing cancellation logic 
        # you can update the order status to "Cancelled"
        order.status = 'cancelled'
        order.save()

        # Add a success message
        messages.success(request, 'Order canceled! You will be refunded soon.')

        # Redirect to the order list page or a success page
        return redirect('order_list')
    except Order.DoesNotExist:
        # Handle the case when the order does not exist
        messages.error(request, 'Order not found.')
        return redirect('order_list')
    


def contact(request):
    if request.method == "POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')

        contact=Contact(name=name,email=email,subject=subject,message=message,date=datetime.today())
        contact.save()
    return render(request,'contact.html')
