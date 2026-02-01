from django import forms
from .models import reviewRating

class reviewRatingForm(forms.ModelForm):
    class Meta:
        model=reviewRating
        fields=('subject','review','rating')