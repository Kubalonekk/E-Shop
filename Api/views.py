from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from App.models import *
from .serializers import *
from rest_framework.filters import SearchFilter
from .filters import *
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN
import requests
from django.http import HttpResponse


def test(request):

    context = {

    }

    return render(request, 'Api/test.html', context)


def get_or_create_customer(request):
    try:
        customer = request.user.customer
    except:
        device = request.session.get('device')
        if request.session.get('device') is None:
            request.session['device'] = str(uuid.uuid4())
            device = request.session.get('device')              
        customer, created = Customer.objects.get_or_create(device=device)
    return customer


@api_view(['GET'])
def products(request):
    order_by = request.query_params.get('order_by', None)
    if order_by is None:
        items = Item.objects.all()
    else:
        items = Item.objects.all().order_by(order_by)
    filterset = ItemFilter(request.GET, queryset=items)
    if filterset.is_valid():
        items = filterset.qs
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def products_gender(request, gender):
    order_by = request.query_params.get('order_by', None)
    if order_by is None:
        items = Item.objects.filter(
            Q(gender__contains=gender) & Q(gender__startswith=gender) & Q(
                item_variant__amount_in_stock__gte=1)
        ).order_by('title').distinct()
    else:
        items = Item.objects.filter(
            Q(gender__contains=gender) & Q(gender__startswith=gender) & Q(
                item_variant__amount_in_stock__gte=1)
        ).order_by(order_by).distinct()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def products_category(request, gender, category):
    category = category.replace('-', ' ')
    categories = Category.objects.filter(
        gender__gender__contains=gender, gender__gender__startswith=gender)
    order_by = request.query_params.get('order_by', None)
    if order_by is None:
        items = Item.objects.filter(
            Q(gender__contains=gender) & Q(category__name__icontains=category) & Q(
                gender__startswith=gender) & Q(item_variant__amount_in_stock__gte=1)
        ).order_by('title').distinct()
    else:
        items = Item.objects.filter(
            Q(gender__contains=gender) & Q(category__name__icontains=category) & Q(
                gender__startswith=gender) & Q(item_variant__amount_in_stock__gte=1)
        ).order_by(order_by).distinct()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_item_to_order(request, slug):
    item = Item.objects.get(slug=slug)
    try:
        item_variant = ItemVariant.objects.get(item=item)
        if item_variant.size == None and item_variant.color == None:
            pass
        else:
            return Response({"message": "Prosze wybrac rozmiar/kolor"}, status=HTTP_400_BAD_REQUEST)
    except:
        return Response({"message": "Prosze wybrac rozmiar/kolor"}, status=HTTP_400_BAD_REQUEST)
    try:
        customer = request.user.customer
    except:
        customer = get_or_create_customer(request)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    print('dupa')
    orderItem, created = OrderItem.objects.get_or_create(
        order=order, item=item, item_variant=item_variant)
    orderItem.quantity += 1
    if item_variant.amount_in_stock < 1:
        return Response({"message": "Produkt niedostępny"}, status=HTTP_400_BAD_REQUEST)
    orderItem.save()
    return Response({"message": "Dodano przedmiot do kosztyka"}, status=HTTP_200_OK)


@api_view(['POST', 'GET'])
def product(request, slug):
    product = Item.objects.get(slug=slug)
    if request.method == "GET":
        serializer = ItemSerializer(product, many=False)
        return Response(serializer.data)
    else:
        customer = get_or_create_customer(request)
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        size = request.data.get('product-size')
        quanity = request.data.get('product-quanity')
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
            return Response({"message": f"Nie udało się dodać przedmiotu do koszyka, dostępna ilość: {item_variant.amount_in_stock}"}, status=HTTP_400_BAD_REQUEST)
        orderItem.quantity += int(quanity)
        orderItem.save()
        return Response({"message": "Dodano przedmiot do kosztyka"}, status=HTTP_200_OK)


@api_view(['GET'])
def product_images(request, slug):
    item = Item.objects.get(slug=slug)
    product_images = ItemImages.objects.filter(item=item)
    serializer = ItemImagesSerializer(product_images, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def shopping_cart(request):
    try:
        customer = get_or_create_customer(request)
        order = Order.objects.get(customer=customer, complete=False)
    except Order.DoesNotExist:
        return Response({"message": "Produkt niedostępny"}, status=HTTP_404_NOT_FOUND)
    ordered_items = OrderItem.objects.filter(order=order)
    serializer = OrderItemSerializer(ordered_items, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def order(request):
    customer = get_or_create_customer(request)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    serializer = OrderSerializer(order, many=False)
    return Response(serializer.data, status=HTTP_200_OK)
        


@api_view(['POST'])
def add_single_item_to_cart(request, id):
    orderItem = OrderItem.objects.get(id=id)
    orderItem.quantity += 1
    orderItem.save()
    serializer = OrderItemSerializer(orderItem, many=False)
    return Response(serializer.data, status=HTTP_200_OK)


@api_view(['PUT','DELETE'])
def single_item_cart(request, id):
    customer = get_or_create_customer(request)
    orderItem = OrderItem.objects.get(id=id)
    if request.method == "PUT":
        orderItem.quantity += 1
        orderItem.save()
        serializer = OrderItemSerializer(orderItem, many=False)
        return Response({"message": "Pomyślnie dodano przedmiot do koszyka", 'data': serializer.data,}, status=HTTP_200_OK)
    else:
        orderItem.quantity -= 1
        orderItem.save()
        if orderItem.quantity == 0:
            orderItem.delete()
            serializer = OrderItemSerializer(orderItem, many=False)
            return Response({"message": "Usunięto przedmiot z koszyka", 'data': serializer.data,}, status=HTTP_200_OK)
        else:
            serializer = OrderItemSerializer(orderItem, many=False)
            return Response({"message": "Usunięto przedmiot z koszyka", 'data': serializer.data,}, status=HTTP_200_OK)



@api_view(['DELETE'])
def remove_item_from_cart(request, id):
    orderItem = OrderItem.objects.get(id=id)
    orderItem.delete()
    serializer = OrderItemSerializer(orderItem, many=False)
    return Response({"message": "Usunięto przedmiot z koszyka", 'data': serializer.data,}, status=HTTP_200_OK)


@api_view(['GET'])
def sizes(request, slug):
    product = Item.objects.get(slug=slug)
    sizes = ItemSize.objects.filter(
        item_size__item=product, item_size__amount_in_stock__gte=1)
    serializer = ItemSizeSerializer(sizes, many=True)
    return Response(serializer.data, status=HTTP_200_OK)


@api_view(['POST', 'DELETE'])
def cupon(request):
    customer = get_or_create_customer(request)
    order = Order.objects.get(customer=customer, complete=False)
    if request.method == "POST":     
        cupon = request.data.get('cupon')
        cupon = cupon.upper()
        try:
            get_cupon = Cupon.objects.get(name=cupon)
            if order.cupon == get_cupon:
                return Response({"message": "Posiadasz już ten kupon"}, status=HTTP_403_FORBIDDEN)     
            order.cupon = get_cupon
            order.save()
            return Response({"message": "Dodano kupon"}, status=HTTP_200_OK)
        except:
            return Response({"message": "Nie ma takiego kuponu"}, status=HTTP_404_NOT_FOUND) 
    else:
        order.cupon = None
        order.save()
        return Response({"message": "Usunięto kupon"}, status=HTTP_200_OK)
        
    
@api_view(['GET'])
def categories(request, gender):
    categories = Category.objects.filter(
        gender__gender__contains=gender, gender__gender__startswith=gender)
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data, status=HTTP_200_OK)


