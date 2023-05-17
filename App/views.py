from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .filters import *
from django.utils.timezone import now
from anyascii import anyascii
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from .forms import *
import requests
import json
from decimal import Decimal
from requests.auth import HTTPBasicAuth
from django.http import JsonResponse
from django.core.serializers import serialize
import uuid
from django.core.mail import send_mail
from django.conf import settings


def index(request):
    items = Item.objects.all()
    time = datetime.datetime.now()

    context = {
        'items': items,

    }

    return render(request, 'App/index.html', context)


def payment_check(request):
    status = request.GET.get('error')
    if status == "501":
        messages.warning(
            request, 'Płatność nie powiodła się, spróbuj ponownie')
        return redirect('index')
    else:
        messages.success(
            request, 'Płatność zakończona pomyślnie, dziękujemy za zakupy w naszym sklepie!')
        return redirect('index')


def about(request):

    context = {

    }

    return render(request, 'App/about.html', context)


def add_item_to_order(request, slug):
    item = Item.objects.get(slug=slug)
    try:
        item_variant = ItemVariant.objects.get(item=item)
        if item_variant.size == None and item_variant.color == None:
            pass
        else:
            messages.success(request, 'Proszę wybrać rozmiar/kolor')
            return redirect('product', slug)
    except:
        messages.success(request, 'Proszę wybrać rozmiar/kolor')
        return redirect('product', slug)
    customer = get_or_create_customer(request)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(
        order=order, item=item)
    if 'quantity' not in request.POST:
        orderItem.quantity += 1
    else:
        orderItem.quantity = request.POST.get['quantity']
    if item_variant.amount_in_stock < 1:
        messages.warning(request, f"Przedmiot niedostępny")
        return redirect('products')
    orderItem.save()
    messages.success(request, 'Pomyślnie dodano przedmiot do koszyka')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def products(request):
    categories = Category.objects.all()
    search = request.GET.get('q')
    order_by = request.GET.get('order_by')

    if search is None:
        if order_by is None:
            items = Item.objects.filter(
                item_variant__amount_in_stock__gte=1).order_by('title').distinct()
        else:
            items = Item.objects.filter(
                item_variant__amount_in_stock__gte=1).order_by(order_by).distinct()
    else:
        items = Item.objects.filter(
            item_variant__amount_in_stock__gte=1, title__icontains=search, ).distinct()

    context = {
        'items': items,
        'categories': categories,


    }

    return render(request, 'App/products.html', context)


def products_gender(request, gender):
    categories = Category.objects.filter(
        gender__gender__contains=gender, gender__gender__startswith=gender)
    order_by = request.GET.get('order_by')
    if order_by is None:
        products = Item.objects.filter(
            Q(gender__contains=gender) & Q(gender__startswith=gender) & Q(
                item_variant__amount_in_stock__gte=1)
        ).order_by('title').distinct()
    else:
        products = Item.objects.filter(
            Q(gender__contains=gender) & Q(gender__startswith=gender) & Q(
                item_variant__amount_in_stock__gte=1)
        ).order_by(order_by).distinct()

    context = {
        'products': products,
        'categories': categories,
        'gender': gender,
    }
    return render(request, 'App/products_gender.html', context)


def products_category(request, gender, category):
    category = category.replace('-', ' ')
    categories = Category.objects.filter(
        gender__gender__contains=gender, gender__gender__startswith=gender)
    order_by = request.GET.get('order_by')
    if order_by is None:
        products = Item.objects.filter(
            Q(gender__contains=gender) & Q(category__name__icontains=category) & Q(
                gender__startswith=gender) & Q(item_variant__amount_in_stock__gte=1)
        ).order_by('title').distinct()
    else:
        products = Item.objects.filter(
            Q(gender__contains=gender) & Q(category__name__icontains=category) & Q(
                gender__startswith=gender) & Q(item_variant__amount_in_stock__gte=1)
        ).order_by(order_by).distinct()

    context = {
        'products': products,
        'categories': categories,
        'gender': gender,
        'category': category,
    }

    return render(request, 'App/products_category.html', context)


def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        send_mail(
            'Email wysłany przez strone Ecommerce.Przez uzytkownika: ' +
            name + 'o adresie email: ' + email,
            message,
            email,
            ['jakubsmorag1999@gmail.com'],

        )
        messages.success(request, 'Successfully sent email')
    context = {

    }

    return render(request, 'App/contact.html', context)


def product(request, slug):
    product = Item.objects.get(slug=slug)
    main_image = product.item_images.get(main=True)
    images = product.item_images.all
    sizes = ItemSize.objects.filter(
        item_size__item=product, item_size__amount_in_stock__gte=1)
    if request.method == 'POST':
        customer = get_or_create_customer(request)
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        size = request.POST.get('product-size')
        quanity = request.POST.get('product-quanity')
        try:
            item_variant = ItemVariant.objects.get(
                item=product, size__size=size)
            orderItem, created = OrderItem.objects.get_or_create(
                order=order, item=product, item_variant=item_variant)
        except:
            item_variant = ItemVariant.objects.get(item=product)
            orderItem, created = OrderItem.objects.get_or_create(
                order=order, item=product)
        if item_variant.amount_in_stock < int(quanity):
            if orderItem.quantity == 0:
                orderItem.delete()
            messages.success(
                request, f"Nie udało się dodać przedmiotu do koszyka, dostępna ilość: {item_variant.amount_in_stock}")
            return redirect('product', slug)
        orderItem.quantity += int(quanity)
        orderItem.save()
        messages.success(request, 'Pomyślnie dodano przedmiot do koszyka')
        return redirect('product', slug)

    else:
        pass
    context = {
        "product": product,
        'main_image': main_image,
        'images': images,
        'sizes': sizes,

    }

    return render(request, 'App/product.html', context)


def get_or_create_customer(request):
    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    return customer


def shopping_cart(request):
    customer = get_or_create_customer(request)
    try:
        order = Order.objects.get(customer=customer, complete=False)
    except Order.DoesNotExist:
        messages.warning(request, 'Nie posiadasz zamowienia')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    if request.method == "POST":
        cupon = request.POST.get('cupon')
        cupon = cupon.upper()

        try:
            get_cupon = Cupon.objects.get(name=cupon)
            order.cupon = get_cupon
            order.save()
            messages.success(request, 'Pomyślnie dodano kod rabatowy')
        except:
            messages.warning(request, 'Nie istnieje taki kod rabatowy')
    ordered_items = OrderItem.objects.filter(order=order)

    context = {
        'order': order,
        'ordered_items': ordered_items,

    }

    return render(request, 'App/shopping_cart.html', context)


def remove_cupon(request, id):
    order = Order.objects.get(id=id)
    order.cupon = None
    order.save()
    messages.success(request, 'Usunięto kupon')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def shopping_cart2(request):

    if request.user.is_authenticated:
        return redirect('address_and_payment')
    else:
        form = LoginForm()
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                user = authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                )
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Pomyślnie zalogowano')
                    return redirect('index')
            else:
                messages.warning(request, 'Coś poszło nie tak')

    context = {
        'form': form,
    }

    context = {
        'form': form,
    }

    return render(request, 'App/shopping_cart2.html', context)


def add_single_item_to_cart(request, id):
    orderItem = OrderItem.objects.get(id=id)
    orderItem.quantity += 1
    orderItem.save()
    messages.success(request, 'Pomyślnie dodano przedmiot do koszyka')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def remove_single_item_from_cart(request, id):
    orderItem = OrderItem.objects.get(id=id)
    orderItem.quantity -= 1
    orderItem.save()
    if orderItem.quantity == 0:
        orderItem.delete()
        messages.success(request, 'Pomyślnie usunięto przedmiot  koszyka')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        messages.success(request, 'Pomyślnie usunięto przedmiot  koszyka')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def remove_item_from_cart(request, id):
    orderItem = OrderItem.objects.get(id=id)
    orderItem.delete()
    messages.success(request, 'Pomyślnie usunięto przedmiot  koszyka')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


# accounts


def signout(request):
    logout(request)
    messages.success(request, 'Pomyślnie wylogowano')
    return redirect('index')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            phone_number = form.cleaned_data.get('phone')
            NewCustomer = Customer.objects.create(
                user=new_user,
                name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
            )
            authenticated_user = authenticate(
                username=new_user.username,
                password=request.POST['password1'])
            login(request, authenticated_user)
            messages.success(request, 'Pomyślnie założno konto')
            try:
                device = request.COOKIES['device']
                customer = Customer.objects.get(device=device)
                order = Order.objects.get(customer=customer, complete=False)
                order.customer = NewCustomer
                order.save()
            except:
                pass
            messages.success(request, 'Pomyślnie założno konto')
            return redirect('index')
        else:
            messages.success(request, 'Cos poszlo nie tak')
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
    }
    return render(request, 'App/register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        messages.success(request, 'Jesteś już zalogowany')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = LoginForm()
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                user = authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                )
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Pomyślnie zalogowano')
                    return redirect('index')
            else:
                messages.success(request, 'Coś poszło nie tak')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    context = {
        'form': form,
    }

    return render(request, 'App/login.html', context)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def address_and_payment(request):
    customer = get_or_create_customer(request)
    order = Order.objects.get(customer=customer, complete=False)
    if not OrderItem.objects.filter(order=order).exists():
        messages.success(request, 'Nie posiadasz przedmiotow w koszyku')
        return redirect('index')
    ordered_items = OrderItem.objects.filter(order=order)
    if request.method == 'POST':
        form = DeliveryAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.customer = customer
            address.save()
            order.address = address
            order.save()
            parcel_machine = request.POST.get('parcel_machine')
            if parcel_machine == '':
                messages.success(request, 'Proszę wybrać punkt odbioru!')
                return redirect('address_and_payment')
            else:
                address.parcel_machine_id = parcel_machine
                address.save()
                check = check_available_stock(request, ordered_items)
                if check == "Error":
                    return redirect('shopping_cart')
            return redirect('create_payu_order', order.id, customer.id, address.id)

        else:
            messages.warning(request, 'Coś poszło nie tak')
    else:
        try:
            address_info = AddressInformation.objects.get(id=order.address.id)
            form = DeliveryAddressForm(instance=address_info)
        except:
            form = DeliveryAddressForm()

    context = {
        'form': form,
    }

    return render(request, 'App/address_and_payment.html', context)


# #dashboard

def dashboard_orders(request):
    orders = Order.objects.all()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    paginator = Paginator(orders, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'myFilter': myFilter,
    }

    return render(request, 'App/dashboard_orders.html', context)


def dashboard_order(request, id):
    order = Order.objects.get(id=id)
    order_address = order.address
    if request.method == "POST":
        form = EditOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
    else:
        form = EditOrderForm(instance=order)

    context = {
        'order': order,
        'form': form,
        'order_address': order_address,
    }

    return render(request, 'App/dashboard_order.html', context)


def dashboard_items(request):
    items = Item.objects.all()

    myFilter = ItemFilter(request.GET, queryset=items)
    items = myFilter.qs

    context = {
        'myFilter': myFilter,
        'items': items,

    }
    return render(request, 'App/dashboard_items.html', context)


def dashboard_item(request, id):
    item = Item.objects.get(id=id)
    item_images = ItemImages.objects.filter(item=item)
    item_variants = ItemVariant.objects.filter(item=item)

    context = {
        'item': item,
        'item_images': item_images,
        'item_variants': item_variants,
    }

    return render(request, 'App/dashboard_item.html', context)


def dashboard_add_item(request):
    if request.method == "POST":
        form = AddItemForm(request.POST)
        images = request.FILES.getlist('images')
        if form.is_valid():
            new_item = form.save()
        ItemImages.objects.create(
            item=new_item,
            main=True,
            img=request.FILES.get('main_image'),
        )
        for image in images:
            new_image = ItemImages.objects.create(
                item=new_item,
                img=image,
            )

    else:
        form = AddItemForm()

    context = {
        'form': form,
    }

    return render(request, 'App/dashboard_add_item.html', context)


def dashboard_edit_item(request, id):
    item = Item.objects.get(id=id)

    context = {

    }

    return render(request, 'App/dashboard_edit_item.html', context)


def dashboard_add_stock_item(request, id):
    item = Item.objects.get(id=id)
    item_variants = ItemVariant.objects.filter(item=item)

    if request.method == "POST":
        form = AddItemVariantForm(request.POST)
        form.fields["size"].queryset = ItemSize.objects.filter(
            category=item.category)
        if form.is_valid():
            new_item_variant = form.save(commit=False)
            size = form.cleaned_data.get('size')
            amount_in_stock = form.cleaned_data.get('amount_in_stock')
            new_item_variant.item = item
            try:
                if size is None:
                    d = ItemVariant.objects.get(item=item)
                else:
                    d = ItemVariant.objects.get(item=item, size_id=size.id)
                messages.success(
                    request, 'Taki stock już istnieje, zsumowano ilość')
                d.amount_in_stock += amount_in_stock
                d.save()
                return redirect('dashboard_add_stock_item', id)
            except:

                new_item_variant.save()
                messages.success(request, 'Pomyślnie dodano stock')
                return redirect('dashboard_add_stock_item', id)
        else:
            messages.warning(request, 'Coś poszło nie tak')
    else:
        form = AddItemVariantForm()
        form.fields["size"].queryset = ItemSize.objects.filter(
            category=item.category)

    context = {
        'form': form,
        'item': item,
    }

    return render(request, 'App/dashboard_add_stock_item.html', context)


# Payu integration

def create_payu_order(request, order, customer, address):
    address = AddressInformation.objects.get(id=address)
    get_order = Order.objects.get(id=order)
    if get_order.payment_in_progress == True:
        get_order.transaction_id += '1'
        get_order.payment_in_progress = False
        get_order.save()
    ordered_items = OrderItem.objects.filter(order=order)
    products = []
    for product in ordered_items:
        product_data = {
            'name': product.item.title,
            'unitPrice': int(product.item.price * 100),
            'quantity': product.quantity,
        }
        products.append(product_data)
    order_amount = get_order.get_cart_total * 100
    order_amount = int(order_amount)

    token = get_token_payu(request)
    token = token['access_token']
    customer_ip = get_client_ip(request)
    url = "https://secure.snd.payu.com/api/v2_1/orders"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token,
        'Accept': 'application/json',
    }

    data = {
        "notifyUrl": "https://kubalonek99.usermd.net/payu_notification/",
        'continueUrl': 'https://kubalonek99.usermd.net/payment_check/',
        "customerIp": customer_ip,
        "merchantPosId": "463032",
        "description": "Example order",
        "currencyCode": "PLN",
        "totalAmount": order_amount,
        "extOrderId":  get_order.transaction_id,
        "buyer": {
            "email": address.email,
            "phone": address.phone,
            "firstName": address.name,
            "lastName": address.last_name,
            "language": "pl",
        },
        "products": products,
    }
    response = requests.post(url, headers=headers,
                             data=json.dumps(data), allow_redirects=False)
    print(response.json())
    response = response.json()['redirectUri']
    get_order.payment_in_progress = True
    get_order.save()
    return redirect(response)


def check_available_stock(request, ordered_items):
    # Check that the ordered  items are in stock
    for d in ordered_items:
        if d.quantity > d.item_variant.amount_in_stock:
            status = "Error"
            if d.item_variant.size == None:
                messages.warning(
                    request, f"Nie posiadamy: {d.item} w ilości {d.quantity} na stanie ")
                return status
            else:
                messages.warning(
                    request, f"Nie posiadamy: {d.item} rozmiar {d.item_variant.size} w ilości {d.quantity} na stanie. Dostępna ilość: {d.item_variant.amount_in_stock}")
                return status


def get_token_payu(request):

    client_id = '463032'
    client_secret = settings.CLIENT_SECRET

    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
    }

    data = {
        'grant_type': 'client_credentials',
    }

    response = requests.post('https://secure.snd.payu.com/pl/standard/user/oauth/authorize',
                             headers=headers, data=data, auth=HTTPBasicAuth(client_id, client_secret))
    response = response.json()
    return response


@csrf_exempt
def payu_notification(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        status = data['order']['status']
        orderId = data['order']['orderId']
        extOrderId = data['order']['extOrderId']
        order = Order.objects.get(transaction_id=extOrderId)
        if status == "PENDING":
            print('W trakcie realizacji')
            return HttpResponse(status=200)
        elif status == "COMPLETED":
            order.complete = True
            order.payment_in_progress = False
            order.completion_date = datetime.datetime.now()
            order.save()
            ordered_items = OrderItem.objects.filter(order=order)
            for item in ordered_items:
                item.item_variant.amount_in_stock -= item.quantity
                item.item_variant.save()
            print('Zamowienie ukonczone')
            return HttpResponse(status=200)
        elif status == "CANCELED":
            print('Zamowienie anulowane')
            order.payment_in_progress = False
            order.transaction_id += '1'
            order.save()
            return HttpResponse(status=200)


def custom_page_not_found_view(request, exception):
    return render(request, "App/404.html", {})

