from django import forms
from django.core.exceptions import ValidationError

from .models import Book, Address, Student, Address2, Student2, Product


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


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['city']

    def clean_city(self):
        city = self.cleaned_data.get('city', '').strip()
        if not city:
            raise ValidationError("City is required.")
        return city


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'age', 'address']
        widgets = {
            'address': forms.Select(),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise ValidationError("Name is required.")
        return name

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is None or age < 0:
            raise ValidationError("Age must be 0 or greater.")
        return age


class Address2Form(forms.ModelForm):
    class Meta:
        model = Address2
        fields = ['city']

    def clean_city(self):
        city = self.cleaned_data.get('city', '').strip()
        if not city:
            raise ValidationError("City is required.")
        return city


class Student2Form(forms.ModelForm):
    class Meta:
        model = Student2
        fields = ['name', 'age', 'addresses']
        widgets = {
            'addresses': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['addresses'].required = False

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise ValidationError("Name is required.")
        return name

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is None or age < 0:
            raise ValidationError("Age must be 0 or greater.")
        return age


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image']

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise ValidationError("Name is required.")
        return name
