from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from App.models import *
from django.core.paginator import Paginator
from django.db.models import Q
from .filters import *
from .forms import *
from django.shortcuts import get_object_or_404, redirect


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

    return render(request, 'Dashboard/dashboard_orders.html', context)


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

    return render(request, 'Dashboard/dashboard_order.html', context)


def dashboard_items(request):
    items = Item.objects.all()

    myFilter = ItemFilter(request.GET, queryset=items)
    items = myFilter.qs

    context = {
        'myFilter': myFilter,
        'items': items,

    }
    return render(request, 'Dashboard/dashboard_items.html', context)


def dashboard_item(request, id):
    item = Item.objects.get(id=id)
    item_images = ItemImages.objects.filter(item=item)
    item_variants = ItemVariant.objects.filter(item=item)

    context = {
        'item': item,
        'item_images': item_images,
        'item_variants': item_variants,
    }

    return render(request, 'Dashboard/dashboard_item.html', context)


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

    return render(request, 'Dashboard/dashboard_add_item.html', context)


def dashboard_edit_item(request, id):
    item = Item.objects.get(id=id)

    context = {

    }

    return render(request, 'Dashboard/dashboard_edit_item.html', context)


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

    return render(request, 'Dashboard/dashboard_add_stock_item.html', context)