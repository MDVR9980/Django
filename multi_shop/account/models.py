from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, phone, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not phone:
            raise ValueError('Users must have an email address')

        user = self.model(
            # email=self.normalize_email(email),
            phone=phone
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            phone,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='آدرس ایمیل',
        max_length=255,
        unique=True, 
        null=True,
        blank=True
    )
    fullname = models.CharField(max_length=50, verbose_name="نام کامل")
    phone = models.CharField(max_length=12, unique=True, verbose_name="شماره تلفن")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False, verbose_name="ادمین")

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
class Otp(models.Model):
    token = models.CharField(max_length=200, null=True, verbose_name="توکن")
    phone = models.CharField(max_length=11, verbose_name="شماره تلفن")
    code = models.SmallIntegerField(verbose_name="کد تایید")
    expiration_date = models.DateTimeField(verbose_name="تاریخ انقضاء کد تخفیف")

    def __str__(self):
        return self.phone
    
    class Meta:
        verbose_name = "لاگین otp"
        verbose_name_plural = "لاگین otps"
    

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name="کاربر")
    fullname = models.CharField(max_length=30, verbose_name="نام کامل")
    email = models.EmailField(blank=True, null=True, verbose_name="ایمیل")
    phone = models.CharField(max_length=12, verbose_name="شماره تلفن")
    address = models.CharField(max_length=300, verbose_name="آدرس")
    zip_code = models.CharField(max_length=30, verbose_name="کدپستی")

    def __str__(self):
        return self.user.phone
    
    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس ها"
    
class Message(models.Model):
    name = models.CharField(max_length=30, verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل")
    subject = models.CharField(max_length=100, verbose_name="موضوع")
    text = models.TextField(verbose_name="پیغام")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "پیام"
        verbose_name_plural = "پیام ها"