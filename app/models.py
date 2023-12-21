from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
# Create your models here.
#Change form register django
#Category

class Category(models.Model):
    sub_category = models.ForeignKey('self',on_delete=models.CASCADE, related_name='sub_categories', null=True, blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200,null=True)
    slug = models.SlugField(max_length=200,unique=True)
    def __str__(self):
        return self.name
class CreateUserForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']
        
    
class Product(models.Model):
    default_size = '36'  # Thay thế 'M' bằng giá trị mặc định mong muốn
    default_value = timezone.now()
    category = models.ManyToManyField(Category,related_name='product')
    name = models.CharField(max_length=200,null=True)
    is_discounted = models.BooleanField(default=False)
    sales_price = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    price = models.FloatField()
    size = models.CharField(max_length=10, choices=[ ('4','35'),('5','36'), ('6','37'), ('7','38'), ('8','39'), ('9','40'), ('10','41'), ('11','42'), ('12','43'), ('13','44') ], default=default_size)
    digital = models.BooleanField(default=False,null=True,blank=False)
    image = models.ImageField(null=True,blank=True)
    detail = models.TextField(null=True,blank=True)

    
    def get_discounted_price(self):
        discount_amount = (self.sales_price / 100) * self.price
        discounted_price = self.price - discount_amount
        return discounted_price
    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
class Order(models.Model):
    customer = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.discounted_total for item in orderitems])
        return total
    def discounted_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total_discounted for item in orderitems])
        return total
class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    # Thêm trường discounted_price để lưu giá giảm giá
    discounted_price = models.FloatField(default=0)
    @property
    def discounted_total(self):
        return self.product.get_discounted_price() * self.quantity if self.product.is_discounted else self.product.price * self.quantity
    @property
    def get_total(self):
        total = self.discounted_price * self.quantity
        return total
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    @property
    def get_total_discounted(self):
        if self.product.is_discounted:
            return self.quantity * self.product.get_discounted_price()
        else:
            return self.quantity * self.product.price
class ShippingAddress(models.Model):
    customer = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    mobile = models.CharField(max_length=200,null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    

    