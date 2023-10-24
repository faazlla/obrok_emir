from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Restaurant, City


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	


class CollaborationForm(forms.ModelForm):
    restaurant_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Restaurant Name'}))
    phone_number = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}))
    address = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}))
    city = forms.ModelChoiceField(label="", queryset=City.objects.all(), empty_label="Select City", widget=forms.Select(attrs={'class':'form-control'}))
    code = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Code'}))
    
    class Meta:
        model = Restaurant
        fields = ('restaurant_name', 'phone_number', 'address', 'code', 'city')


class DonationForm(forms.Form):
    city = forms.ModelChoiceField(label="", queryset=City.objects.all(), empty_label="Select City", widget=forms.Select(attrs={'class': 'form-control', 'id': 'city-selector'}))
    restaurant = forms.ModelChoiceField(label="", queryset=Restaurant.objects.none(), empty_label="Select Restaurant", widget=forms.Select(attrs={'class': 'form-control', 'id': 'restaurant-selector'}))
    amount = forms.DecimalField(label="", max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Amount'}))
    restaurant_code = forms.CharField(label="", max_length=10, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'CODE'}))


class DonationUserForm(forms.Form):
    city = forms.ModelChoiceField(label="", queryset=City.objects.all(), empty_label="Select City", widget=forms.Select(attrs={'class': 'form-control', 'id': 'city-selector'}))
    restaurant = forms.ModelChoiceField(label="", queryset=Restaurant.objects.none(), empty_label="Select Restaurant", widget=forms.Select(attrs={'class': 'form-control', 'id': 'restaurant-selector'}))
    amount = forms.DecimalField(label="", max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Amount'}))
    restaurant_code = forms.CharField(label="", max_length=10, widget=forms.TextInput(attrs={'class': 'form-control' , 'placeholder':'CODE'}))
    

class EditRestaurantForm(forms.ModelForm):
    restaurant_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Restaurant Name'}))
    phone_number = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}))
    address = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}))
    city = forms.ModelChoiceField(label="", queryset=City.objects.all(), empty_label="Select City", widget=forms.Select(attrs={'class':'form-control'}))
    code = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Code'}))
    
    class Meta:
        model = Restaurant
        fields = ['restaurant_name', 'city', 'phone_number', 'address', 'code']
        widgets = {
            'city': forms.Select(attrs={'class': 'form-control'}),
        }
