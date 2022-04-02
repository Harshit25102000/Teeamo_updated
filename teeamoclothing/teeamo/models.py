from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
# Create your models here.
class product(models.Model):
    product_id = models.AutoField
    is_featured = models.BooleanField(default=False)
    product_name = models.CharField(max_length=100)
    category=models.CharField(max_length=50,default="")
    color = models.CharField(max_length=50, default="")
    price=models.IntegerField(default=0)
    desc=models.CharField(max_length=300)
    pub_date = models.DateField()
    image1=models.ImageField(upload_to="teeamo/Product-images", default="")
    image2=models.ImageField(upload_to="teeamo/Product-images", default="")
    image3 = models.ImageField(upload_to="teeamo/Product-images", default="")
    image4 = models.ImageField(upload_to="teeamo/Product-images", default="")
    image5 = models.ImageField(upload_to="teeamo/Product-images", default="")

    def __str__(self):
        return self.product_name


class review(models.Model):
    review_id = models.AutoField
    name=models.CharField(max_length=100)
    content = models.CharField(max_length=200)
    image = models.ImageField(upload_to="teeamo/reviews-images",default="")

    def __str__(self):
        return self.name


# User customization goes down

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

from django.utils import timezone
class Order(models.Model):
    payment_status_choices = (
        (1, 'SUCCESS'),
        (2, 'FAILURE'),
        (3, 'PENDING'),
    )

    customer=models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    total = models.IntegerField(default=0)
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True, default=None)
    datetime_of_payment = models.DateTimeField(default=timezone.now)
    transaction_id = models.CharField(max_length=200,null=True)
    status = models.CharField(max_length=50,null=True,blank=True)
    razorpay_order_id = models.CharField(max_length=500,null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.datetime_of_payment and self.id:
            self.order_id = self.datetime_of_payment.strftime('TEE%Y%m%dAMO') + str(self.id)
        return super().save(*args, **kwargs)
    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    size=models.CharField(max_length=15,default="large")

    @property
    def get_total(self):
        total= self.product.price*self.quantity
        return total


    def __str__(self):

        return str(self.order)




class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    name=models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    phone1=models.CharField(max_length=20,null=True, blank=True)
    phone2 = models.CharField(max_length=20, null=True, blank=True)
    address1=models.CharField(max_length=200, null=True, blank=True)
    address2 = models.CharField(max_length=200, null=True, blank=True)
    city=models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    pincode = models.CharField(max_length=200, null=True, blank=True)
    date_added= models.DateField(auto_now_add=True, blank=True)
    additionalinfo = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.order)
