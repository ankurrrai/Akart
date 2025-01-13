from django import forms
from .models import RatingReview


class ReviewForm(forms.ModelForm):
    review=forms.CharField(required=False)
    subject=forms.CharField(required=False)
    class Meta:
        model=RatingReview
        fields=['rating','subject','review']