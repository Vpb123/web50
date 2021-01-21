from django import forms
from .models import Listing


class Form(forms.ModelForm):
    class Meta:
        model=Listing
        fields=('title','description','price','imgURL','category')
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control'}),
            'price':forms.TextInput(attrs={'class':'form-control'}),
            'imgURL':forms.TextInput(attrs={'class':'form-control'}),
            }
        