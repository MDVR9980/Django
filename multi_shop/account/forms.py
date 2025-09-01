from django import forms 
from account.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core import validators
from django.core.exceptions import ValidationError
from account.models import Address, Message

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='گذرواژه', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تکرار گذرواژه', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('phone', 'email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
    

# def start_with_zero(value):
#     if value[0] != '0':
#         raise forms.ValidationError("Phone should start with 0", code="invlid_phone")
    
class LoginForm(forms.Form):
    # phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control '}, validators=[validators.MaxLengthValidator(11)]))
    # phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control '}), validators=[start_with_zero])
    # phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control '}))
    identifier = forms.CharField(
        label='ایمیل یا شماره تلفن',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل یا شماره تلفن'}),
        max_length=254    
    )
    
    password = forms.CharField(
        label='پسورد',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "پسورد"})
    )

    def clean_identifier(self):
        value = self.cleaned_data.get('identifier')
        if '@' in value:
            if value.count('@') !=1:
                raise ValidationError("invalid email format.", code="invalid_email")
        else:
            if not value.isdigit():
                raise ValidationError("Phone number must contain only digits.", code='invalid_phone')
            if len(value) != 11:
                raise ValidationError("Phone number must be exactly 11 digits.")
        
        return value

    # def clean(self):
    #     cd = super().clean()
    #     phone = cd['phone']
    #     if(len(phone) > 11):
    #         raise ValidationError(
    #             "Invalid value: %(value)s is invalid",
    #             code='invalid',
    #             params={'value': f'{phone}'}
    #         )
        
    #     return phone

class AddressCreationForm(forms.ModelForm):
    user = forms.IntegerField(required=False)
    class Meta:
        model = Address
        fields = '__all__'

class OtpLoginForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره تلفن'}), validators=[validators.MaxLengthValidator(11)])

class CheckOtpForm(forms.Form):
    code = forms.CharField(
        max_length=4,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[validators.MaxLengthValidator(4)]
    )

class MessageContactUsForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('name', 'email', 'subject', 'text')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'موضوع',
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'پیام شما برای ما',
            }),
        }