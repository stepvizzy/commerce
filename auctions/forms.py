from django import forms

from auctions.models import *


class CreateListing(forms.ModelForm):
    class Meta:
        model = Listing
        fields = '__all__'
        exclude = ('auctioneer',)
        widgets = {
            'title': forms.TextInput(attrs={'placeholder':'Title','class':'form-control w-50'}),
            'category': forms.TextInput(attrs={'placeholder': 'Category', 'class': 'form-control w-50'}),
            'description': forms.TextInput(attrs={'placeholder': 'Description', 'class': 'form-control w-50'}),
            'bid': forms.NumberInput(attrs={'class':'form-control w-auto'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'})
        }
    
    def check_data(self):
        title = self.cleaned_data.get("title")
        if (title == ""):
            raise forms.ValidationError("This field cannot be empty")
        
        for instance in Listing.objects.all():
            if instance.title == title:
                raise forms.ValidationError("This title is not available")
        return title
        
class AddToWatchlist(forms.ModelForm):
    class Meta:
        model = Watchlist
        fields = '__all__'
        widgets = {
            'name': forms.HiddenInput(),
            'product': forms.HiddenInput()
        }