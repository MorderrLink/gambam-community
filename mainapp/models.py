from django.db import models
from django.contrib.auth.models import User

from django.utils.text import slugify
# Create your models here.
from django.forms.widgets import ClearableFileInput

class MyClearableFileInput(ClearableFileInput):
    initial_text = 'currently'
    input_text = 'change'
    clear_checkbox_label = 'clear'


class Post(models.Model):
    text = models.CharField(max_length=150, verbose_name='')
    author = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False)
    image = models.ImageField(null=True, blank=True, upload_to='mainapp/photos')
    date = models.DateTimeField(auto_now_add=True)


    

    def __str__(self):
        return  self.author.username + ' - ' + str(self.id)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''

        return url
    




class Product(models.Model):
    name = models.CharField(verbose_name='name', max_length=35)
    description = models.TextField(verbose_name='description')
    photo = models.ImageField('Изображение', upload_to="mainapp/photos", default='', blank=True)
    price = models.IntegerField(verbose_name='price')
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def imageURL(self):
        try:
            url = self.photo.url
        except:
            url = ''

        return url
        
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name']




class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered =  models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False, verbose_name="Completed", null=True, blank=False)
    transaction_id = models.CharField("Transaction id", max_length=30)
    finished = models.BooleanField(default=False, verbose_name="finished", null=True, blank=False)

    def __str__(self):
        return str(self.id)
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    class Meta:
        ordering = ['-completed', 'finished', '-transaction_id']

class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, verbose_name="Quantity")
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.order.id)
    
    @property
    def get_total(self):
        total = self.quantity * self.product.price
        return total
    

class Picture(models.Model):
    image = models.ImageField(upload_to="mainapp/photos", default='', blank=True)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''

        return url