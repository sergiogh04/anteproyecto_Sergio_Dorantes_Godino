from django import forms
from .models import Review, UserAnimeList

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'min': 1,
                'max': 5,
                'class': 'form-rating'
            }),
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-comment'
            })
        }

class StatusForm(forms.ModelForm):
    class Meta:
        model = UserAnimeList
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'status-select',
                'onchange': 'this.form.submit()'
            })
        }