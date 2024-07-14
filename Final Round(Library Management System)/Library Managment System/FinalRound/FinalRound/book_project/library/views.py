
from django.shortcuts import render, redirect
import requests
from .models import Book
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .forms import BookSearchForm
from django.contrib import messages
from .forms import BookSearchForm


def search_books(request):
    form = BookSearchForm(request.GET or None)
    books = []
    if request.method == 'GET' and form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            # Replace with the actual API endpoint
            api_url = f'https://www.googleapis.com/books/v1/volumes?q={query}'
            response = requests.get(api_url)
            data = response.json()
            books = data.get('items', [])
    return render(request, 'search.html', {'form': form, 'books': books})



@require_POST
def add_to_store(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        book_title = request.POST.get('title')
        book_author = request.POST.get('author')
        book_publisher = request.POST.get('publisher', '')
        book_year = request.POST.get('year', '')
        book_isbn = request.POST.get('isbn')
        book_rating = request.POST.get('rating', '')
        book_thumbnail = request.POST.get('thumbnail', '')
        book_description = request.POST.get('description', '')
        book_quantity = int(request.POST.get('quantity', 0))

        # Validate and convert year and rating to appropriate types
        year = int(book_year) if book_year else None
        rating = float(book_rating) if book_rating else None

        # Create or update the book entry
        book, created = Book.objects.update_or_create(
            isbn=book_isbn,
            defaults={
                'title': book_title,
                'author': book_author,
                'publisher': book_publisher,
                'year': year,
                'rating': rating,
                'thumbnail': book_thumbnail,
                'description': book_description,
                'quantity': book_quantity
            }
        )
        book.save()

        return redirect('search_books')  # Redirect to the search results page

    return HttpResponse("Invalid request method.", status=400)


