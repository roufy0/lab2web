from django import forms
from django.core.exceptions import ValidationError

from .models import Book, Address, Student, Address2, Student2, Product


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'price', 'quantity', 'pubdate', 'rating', 'publisher', 'authors']
        widgets={
            'pubdate':forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


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



class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'age', 'address']

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is None or age < 0:
            raise ValidationError("Age must be 0 or greater.")
        return age


class Address2Form(forms.ModelForm):
    class Meta:
        model = Address2
        fields = ['city']




class Student2Form(forms.ModelForm):
    class Meta:
        model = Student2
        fields = ['name', 'age', 'addresses']
        widgets = {
            'addresses': forms.CheckboxSelectMultiple(),
        }

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is None or age < 0:
            raise ValidationError("Age must be 0 or greater.")
        return age


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image']
