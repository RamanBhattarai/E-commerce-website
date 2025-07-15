from django import forms
from .models import UserProfile

class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'full_name', 'phone_number', 'address', 'preferred_shipping_address']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = UserProfile.objects.filter(email=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Email is already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = UserProfile.objects.filter(username=username)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Username is already taken.")
        return username
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        qs = UserProfile.objects.filter(phone_number=phone_number)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Phone number is already in use.")
        return phone_number
