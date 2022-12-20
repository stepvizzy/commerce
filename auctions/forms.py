from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from auctions.models import Category, Listing


class CreateListing(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'category', 'imageUrl', 'startPrice']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder':'Title', 'autocomplete': 'off', 'class':'form-control w-50 mb-4'}),
            'category': forms.Select(attrs={'placeholder': 'Category', 'autocomplete': 'off', 'class': 'form-control w-50 mb-4'}),
            'description': forms.TextInput(attrs={'placeholder': 'Description', 'autocomplete': 'off', 'class': 'form-control w-50 mb-4'}),
            'startPrice': forms.NumberInput(attrs={'class':'form-control w-auto mb-4'}),
            'imageUrl': forms.TextInput(attrs={'placeholder':'ImageUrl','class':'form-control w-50 mb-4'}),
        }
    
        
# class AddToWatchlist(forms.ModelForm):
#     class Meta:
#         model = Watchlist
#         fields = '__all__'
#         widgets = {
#             'name': forms.HiddenInput(),
#             'product': forms.HiddenInput()
#         }