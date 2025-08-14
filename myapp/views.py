from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum
from .models import product, Cart
from django.conf import settings
from django.core.mail import send_mail


def index(request):
    return render(request, 'index.html')

# register
def register(request):
    return render(request, 'register.html')


def reg(request):
    uname = request.GET.get("uname")
    email = request.GET.get("email")
    password = request.GET.get("password")
    confirmpassword = request.GET.get("confirmpassword")

    if uname and email and password and confirmpassword:

        # Check if username already exists
        if User.objects.filter(username=uname).exists():
            param = {'msg': "Username already taken"}
            return render(request, 'register.html', param)

        # Check if email already exists (optional)
        # if User.objects.filter(email=email).exists():
        #     param = {'msg': "Email already registered"}
        #     return render(request, 'register.html', param)

        # Create new user
        user = User.objects.create_user(username=uname, email=email, password=password)
        user.save()
        param = {'msg': "User added successfully"}
        return render(request, 'register.html', param)

    else:
        param = {'msg': "Please fill full form"}
        return render(request, 'register.html', param)


# login
def login_page(request):
    return render(request, 'login_page.html')


def login_data(request):
    uname = request.GET.get("uname")
    password = request.GET.get("password")

    user = authenticate(username=uname, password=password)
    if user is not None:
        login(request, user)
        return render(request, 'index.html')

    else:
        param = {'msg': "Wrong username and password"}
        return render(request, 'login_page.html', param)


def logout_user(request):
    logout(request)
    return render(request, 'index.html')


# Men
def men(request):
    # Fetch men's products from database
    men_products = product.objects.filter(product_category='men')

    # Group products into rows of 4 for display
    rows = []
    for i in range(0, len(men_products), 4):
        rows.append(men_products[i:i + 4])

    context = {
        'rows': rows,
        'products': men_products
    }
    return render(request, 'men.html', context)


# Women
def women(request):
    # Fetch women's products from database
    women_products = product.objects.filter(product_category='women')

    # Group products into rows of 4 for display
    rows = []
    for i in range(0, len(women_products), 4):
        rows.append(women_products[i:i + 4])

    context = {
        'rows': rows,
        'products': women_products
    }
    return render(request, 'women.html', context)


# kids
def kids(request):
    # Fetch kids' products from database
    kids_products = product.objects.filter(product_category='kids')

    # Group products into rows of 4 for display
    rows = []
    for i in range(0, len(kids_products), 4):
        rows.append(kids_products[i:i + 4])

    context = {
        'rows': rows,
        'products': kids_products
    }
    return render(request, 'kids.html', context)


from django.contrib.auth.decorators import login_required
from django.db.models import Sum


# Profile
@login_required
def profile(request):
    user = request.user

    # Get user's cart items count
    cart_count = 0
    if user.is_authenticated:
        cart_count = Cart.objects.filter(user=user).count()

    # Get user's order history (you'll need to implement this model)
    # orders = Order.objects.filter(user=user).order_by('-order_date')[:5]

    context = {
        'user': user,
        'cart_count': cart_count,
        # 'orders': orders  # Uncomment when Order model is implemented
    }
    return render(request, 'profile.html', context)


# contact
def contact(request):
    return render(request, 'contact.html')


# product_insert
def product_insert(request):
    return render(request, 'product_insert.html')


# insert_data
def insert_data(request):
    btn = request.POST.get('submit')

    if btn == 'upload_p':
        p = product()
        p.product_category = request.POST['product_category']
        p.product_image = request.FILES['product_image']
        p.product_title = request.POST['product_title']
        p.product_description = request.POST['product_description']
        p.product_price = request.POST['product_price']
        p.product_detail = request.POST['product_detail']

        p.save()

        param = {'msg': "data inserted...."}
        return render(request, 'product_insert.html', param)
    return render(request, 'product_insert.html')


# product display
def product_list(request):
    # Fetch all products from DB
    products = product.objects.all().order_by('pid')

    # Group products by pid range (each row = same hundred range)
    rows = []
    current_row = []
    start_range = None

    for p in products:
        # Set the start range if it's the first product in the row
        if start_range is None:
            start_range = p.pid

        # If product falls within the same hundred range
        if start_range <= p.pid < start_range + 100:
            current_row.append(p)
        else:
            rows.append(current_row)
            current_row = [p]
            start_range = p.pid

    # Add last row if there are remaining products
    if current_row:
        rows.append(current_row)

    return render(request, 'store/product_list.html', {'rows': rows})


# product_page
def product_page(request, pid):
    product_obj = get_object_or_404(product, pid=pid)
    context = {
        'product': product_obj
    }
    return render(request, 'product_page.html', context)


# product detail
def product_detail(request, pid):
    product = get_object_or_404(product, pid=pid)
    context = {
        'product': product
    }
    return render(request, 'store/product_detail.html', context)


# Cart functionality
def add_to_cart(request, pid):
    if request.method == 'POST':
        product_obj = get_object_or_404(product, pid=pid)

        if request.user.is_authenticated:
            # For authenticated users, use the database
            cart_item, created = Cart.objects.get_or_create(
                user=request.user,
                product=product_obj,
                defaults={'quantity': 1}
            )
            if not created:
                cart_item.quantity += 1
                cart_item.save()
            messages.success(request, f'Added {product_obj.product_title} to cart!')
        else:
            # For non-authenticated users, use session
            cart = request.session.get('cart', {})
            if str(pid) in cart:
                cart[str(pid)]['quantity'] += 1
            else:
                cart[str(pid)] = {
                    'title': product_obj.product_title,
                    'price': float(product_obj.product_price),
                    'image': product_obj.product_image.url if product_obj.product_image else '',
                    'category': product_obj.product_category,
                    'quantity': 1
                }
            request.session['cart'] = cart
            messages.success(request, f'Added {product_obj.product_title} to cart!')

        return redirect('product_page', pid=pid)
    return redirect('product_list')


def cart_page(request):
    if request.user.is_authenticated:
        # For authenticated users, get cart from database
        cart_items = Cart.objects.filter(user=request.user)
        cart_data = []
        total_amount = 0

        for item in cart_items:
            item_total = item.product.product_price * item.quantity
            cart_data.append({
                'product': item.product,
                'quantity': item.quantity,
                'total_price': item_total,
                'id': item.id  # Include cart item ID for removal
            })
            total_amount += item_total
    else:
        # For non-authenticated users, get cart from session
        cart = request.session.get('cart', {})
        cart_data = []
        total_amount = 0

        for pid, item_data in cart.items():
            try:
                product_obj = product.objects.get(pid=pid)
                item_total = item_data['price'] * item_data['quantity']
                cart_data.append({
                    'product': product_obj,
                    'quantity': item_data['quantity'],
                    'total_price': item_total,
                    'id': pid  # Use product ID as the ID for session cart items
                })
                total_amount += item_total
            except product.DoesNotExist:
                continue

    context = {
        'cart_items': cart_data,
        'total_amount': total_amount,
        'total_items': len(cart_data)
    }
    return render(request, 'cart_page.html', context)


def remove_from_cart(request, item_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                cart_item = Cart.objects.get(id=item_id, user=request.user)
                product_title = cart_item.product.product_title
                cart_item.delete()
                messages.success(request, f'Removed {product_title} from cart!')
            except Cart.DoesNotExist:
                pass
        else:
            cart = request.session.get('cart', {})
            if str(item_id) in cart:
                product_title = cart[str(item_id)]['title']
                del cart[str(item_id)]
                request.session['cart'] = cart
                messages.success(request, f'Removed {product_title} from cart!')

    return redirect('cart_page')


def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please sign in to proceed to checkout.')
        return redirect('login_page')

    # For now, just show a simple checkout page
    # In a real application, you would implement payment processing here
    return render(request, 'checkout.html')

# forget_pass
def forget_pass(request):
    return render(request,'forget_pass.html')

def sell_form(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        subject = "New Sell Form Submission"
        message = f"Email: {email}"
        from_email = settings.EMAIL_HOST_USER

        send_mail(subject, message, from_email, ['sohambhuvad11@gmail.com'], fail_silently=False)

        # You may want to send some success message or redirect after sending mail
        return render(request, 'sell.html', {'success': True})

    return render(request, 'sell.html')