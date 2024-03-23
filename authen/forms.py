from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
import re
from .models import CustomUser
from enums import E_Teachers
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, help_text='Required. 100 charaters of fewer.')
    email = forms.EmailField(max_length=100, help_text='Required. Enter a valid email address.',
                             widget=forms.EmailInput(attrs={'placeholder': 'ex@mbstu.ac.bd'}))

    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('full_name', 'age', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_regex = r'^\w+@mbstu\.ac\.bd$'
        if email and not re.match(email_regex, email):
            raise ValidationError('Email is not valid.Please confirm the valid email.')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('This email address is already in use.')
        return email
