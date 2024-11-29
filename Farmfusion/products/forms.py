from django import forms
from.models import Product

class ProductForm(forms.ModelForm):
    class Meta :
        model = Product
        fields = ['name','price','quantity','image']



from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']