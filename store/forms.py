from django import forms
from .models import RatingReview


class ReviewForm(forms.ModelForm):
    class Meta:
        model=RatingReview
        fields=['rating','subject','review']