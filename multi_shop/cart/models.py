from django.db import models
from account.models import User
from product.models import Product

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="کاربر")
    # address = models.CharField(max_length=100)
    # email = models.EmailField(blank=True, null=True)
    # phone = models.CharField(max_length=12)
    total_price = models.IntegerField(default=0, verbose_name="قیمت کل")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد سفارش")
    is_paid = models.BooleanField(default=False, verbose_name="پرداخت شده")
    address = models.TextField(blank=True, null=True, verbose_name="آدرس")

    def __str__(self):
        return self.user.phone
    
    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش ها"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="سفارش")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items', verbose_name="محصول")
    size = models.CharField(max_length=12, verbose_name="سایز")
    color = models.CharField(max_length=12, verbose_name="رنگ")
    quantity = models.SmallIntegerField(verbose_name="تعداد")
    price = models.PositiveIntegerField(verbose_name="قیمت")

    class Meta:
        verbose_name = "مورد سفارش"
        verbose_name_plural = "اقلام سفارش"


class DiscountCode(models.Model):
    name = models.CharField(max_length=10, unique=True, verbose_name="نام کدتخفیف")
    discount = models.SmallIntegerField(default=0, verbose_name="درصد تخفیف")
    quantity = models.SmallIntegerField(default=1, verbose_name="تعداد کد تخفیف")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "کد تخفیف"
        verbose_name_plural = "کد های تخفیف"