# forms.py
from django import forms

class BookSearchForm(forms.Form):
    query = forms.CharField(label='Search for a book', max_length=255)
