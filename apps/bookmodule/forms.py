from django import forms
from django.core.exceptions import ValidationError

from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'price', 'quantity', 'pubdate', 'rating', 'publisher', 'authors']
        widgets = {
            'pubdate': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
            'authors': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pubdate'].input_formats = ['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M:%S']
        self.fields['authors'].required = False
        self.fields['publisher'].required = False

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise ValidationError("Title is required.")
        return title

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None or price < 0:
            raise ValidationError("Price must be 0 or greater.")
        return price

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is None or quantity < 0:
            raise ValidationError("Quantity must be 0 or greater.")
        return quantity

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is None or rating < 1 or rating > 5:
            raise ValidationError("Rating must be between 1 and 5.")
        return rating
