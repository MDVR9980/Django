from django import forms
from django.core.validators import ValidationError

class ContactUsForm(forms.Form):
    name = forms.CharField(
        max_length=5,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
        }),
        label='Your Name'
    )
    text = forms.CharField(
        max_length=5,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
        }),
        label='Your Message'
    )

    Birth_YEAR_CHOICES = ['1380', '1385', '1363', '1354']
    FAVOITE_COLORS_CHOICES = [
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('red', 'Red'),
    ]
    birth_year = forms.DateField(widget=forms.SelectDateWidget(years=Birth_YEAR_CHOICES, attrs={'class': 'main-button'}))
    # colors = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=FAVOITE_COLORS_CHOICES)
    colors = forms.ChoiceField(widget=forms.RadioSelect(), choices=FAVOITE_COLORS_CHOICES)

    # def clean(self):
    #     name = self.cleaned_data.get('name')
    #     text = self.cleaned_data.get('text')
    #     if name == text:
    #         raise ValidationError('name and text are same', code='name_text_same')
        
    # def clean_name(self):
    #     name = self.cleaned_data.get('name')
    #     if 'a' in name:
    #         raise ValidationError('a can not be in name', code='a_in_name')
    #     return name
