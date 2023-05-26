from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify
from anyascii import anyascii
import uuid
from django.core.validators import RegexValidator


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='customer', null=True)
    device = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    creation_date = models.DateTimeField(auto_now_add=True, null=True)
    phone_number = PhoneNumberField(blank=True)
    full_name = models.CharField(max_length=250, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.user is not None:
            self.full_name = self.name + ' ' + self.last_name
        super().save(*args, **kwargs)

    def __str__(self):
        if self.user:
            name = f"{self.name} {self.last_name}"
        else:
            name = self.device
        return name


class AddressInformation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    email = models.EmailField(null=True)
    name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    street_address = models.CharField(max_length=150, null=True,)
    postcode = models.CharField(max_length=100,
                                null=True,
                                validators=[RegexValidator(r"^[0-9]{2}-[0-9]{3}", message='Wprowadź kod pocztowy w formacie xx-xxx')])
    city = models.CharField(max_length=100, null=True)
    phone = models.CharField(
        max_length=12,
        null=True,
        validators=[RegexValidator(
            r'(?<!\w)(\(?(\+|00)?48\)?)?[ -]?\d{3}[ -]?\d{3}[ -]?\d{3}(?!\w)', message="Wprowadź numer w formacie 123456789")],

    )
    parcel_machine_id = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"Address: {self.customer} "


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Item(models.Model):
    GENDER_CHOICES = (
        ('Man', 'Man'),
        ('Woman', 'Woman'),
    )

    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="gender")
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES, null=True)
    description = models.TextField(null=True)
    slug = models.SlugField(max_length=50, blank=True, null=True)
    main_img = models.ImageField(null=True)
    

    def save(self, *args, **kwargs):
        # Overrides the basic save method, adding a slug field if it doesn't exist and checks
        # if the slug already exists creates a unique
        if self.slug is None:
            title_ascii = self.title
            title_ascii = anyascii(title_ascii)
            slug = slugify(title_ascii, allow_unicode=True)
            qs = Item.objects.filter(slug=slug)
            if qs.count() >= 1:
                self.slug = f"{slug}-{qs.count()+1}"
            else:
                self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ItemSize(models.Model):
    size = models.CharField(max_length=50)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.size


class ItemColor(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ItemVariant(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE,
                             related_name='item_variant', blank=True, null=True)
    size = models.ForeignKey(ItemSize,
                             on_delete=models.CASCADE, null=True, blank=True,
                             related_name='item_size',
                             help_text="Jeśli przedmiot jest uniwersalnego rozmiaru zostaw to pole puste")
    color = models.ForeignKey(
        ItemColor, on_delete=models.CASCADE, null=True, blank=True)
    amount_in_stock = models.IntegerField()

    def __str__(self):
        return f"{self.item} size {self.size}, color {self.color}, amount: {self.amount_in_stock}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['item', 'color', 'size'],
                name='unique_prod_color_size_combo'
            )
        ]


class ItemImages(models.Model):
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="item_images")
    img = models.ImageField(null=True)


class Cupon(models.Model):
    name = models.CharField(max_length=30)
    discount = models.IntegerField(help_text="Wartość procentowa kuponu")
    active = models.BooleanField(default=False)
    display_on_page = models.BooleanField(default=False)

    def __str__(self):
        return f"KOD: {self.name}, zniża: {self.discount}%"


class Order(models.Model):

    SHIPMNET_STATUS_CHOICES = (
        ('Do wysłania', 'Do wysłania'),
        ('Wysłana', 'Wysłana'),
        ('Dostarczona', 'Dostarczona'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.ForeignKey(AddressInformation, on_delete=models.SET_NULL,
                                null=True, blank=True, related_name="address_order")
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    payment_in_progress = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    shipment_status = models.CharField(
        max_length=15, choices=SHIPMNET_STATUS_CHOICES, null=True, default="Do wysłania")
    cupon = models.ForeignKey(
        Cupon, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.transaction_id is None:
            self.transaction_id = uuid.uuid4()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.transaction_id

    @property
    # returns the value of the ordered items without cupon
    def get_cart_total_without_cupon(self):
        ordered_items = self.ordered_item.all()
        total = sum([item.get_total for item in ordered_items])
        return total

    @property
    # returns the value of the ordered items with cupon if exist
    def get_cart_total(self):
        ordered_items = self.ordered_item.all()
        total = sum([item.get_total for item in ordered_items])
        if self.cupon:
            discount = total * self.cupon.discount / 100
            total -= discount
        return total

    @property
    # returns the number of items ordered
    def get_cart_objects_quantity(self):
        ordered_items = self.ordered_item.all()
        total = sum([item.quantity for item in ordered_items])
        return total

    @property
    # returns cupon value
    def get_cupon_value(self):
        if self.cupon:     
            ordered_items = self.ordered_item.all()
            total = sum([item.get_total for item in ordered_items])
            discount = total * self.cupon.discount / 100
            return discount
        return 0


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    order = models.ForeignKey(
        Order,  on_delete=models.SET_NULL, null=True, related_name="ordered_item")
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    item_variant = models.ForeignKey(
        ItemVariant, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.item_variant is None:
            return f"{self.item} x {self.quantity}"
        else:
            return f"{self.item} x {self.quantity} {self.item_variant.size}"

    @property
    def get_total(self):
        total = self.item.price * self.quantity
        return total
