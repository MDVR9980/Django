from django.db import models

class Category(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='subs', verbose_name="والد دسته بندی")
    title = models.CharField(max_length=100, verbose_name="عنوان دسته بندی")
    slug = models.SlugField(verbose_name="اسلاگ")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

class Size(models.Model):
    title = models.CharField(max_length=10, verbose_name="عنوان سایز")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "سایز"
        verbose_name_plural = "سایز ها"

class Color(models.Model):
    title = models.CharField(max_length=10, verbose_name="نام رنگ")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "رنگ"
        verbose_name_plural = "رنگ ها"


class Product(models.Model):
    category = models.ManyToManyField(Category, blank=True, null=True, verbose_name="دسته بندی محصول")
    title = models.CharField(max_length=30, verbose_name="عنوان محصول")
    description = models.TextField(verbose_name="توضیحات محصول")
    price = models.IntegerField(verbose_name="قیمت محصول")
    discount = models.SmallIntegerField(verbose_name="کد تخفیف")
    image = models.ImageField(upload_to="products", verbose_name="عکس محصول")
    size = models.ManyToManyField(Size, related_name='products', blank=True, null=True, verbose_name="سای هایز محصول")
    color = models.ManyToManyField(Color, related_name='products', verbose_name="رنگ های محصول")

    @property
    def discounted_price(self):
        return ((100 - self.discount) * self.price) // 100

    # class Meta:

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
    

class Information(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE, related_name="informations", verbose_name="محصول")
    text = models.TextField(verbose_name="ویژگی محصول")

    def __str__(self):
        return self.text[:30]
    
    class Meta:
        verbose_name = "اطلاعات"
        verbose_name_plural = "اطلاعات ها"