from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Author, Quote, Tag


def main(request, page=1):
    # page_number = request.GET.get('page', 1)
    quotes = Quote.objects.all().order_by('-created_at')  # Отримання всіх цитат із бази даних SQLite
    per_page = 10
    paginator = Paginator(quotes, per_page)
    quotes_on_page = paginator.get_page(page)
    return render(request, "quotes/index.html", context={"quotes": quotes_on_page})


def author_create(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname', '')
        born_date = request.POST.get('born_date', '')
        born_location = request.POST.get('born_location', '')
        description = request.POST.get('description', '')
        quote_text = request.POST.get('quote', '')

        # Створення автора
        author = Author(fullname=fullname, born_date=born_date, born_location=born_location, description=description)
        author.save()

        # Створення цитати та збереження її з автором
        quote = Quote(quote=quote_text, author=author)
        quote.save()

        return redirect('quotes:root')  # Перенаправлення на сторінку зі списком авторів
    return render(request, 'author/author_create.html')


def author_page(request, author_id):
    # Отримати об'єкт автора за його ідентифікатором
    author = Author.objects.get(id=author_id)
    return render(request, 'author/author_page.html', {'author': author})


def quote_page(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    quotes = Quote.objects.filter(tags=tag)
    author = Author.objects.filter(quote__tags=tag).first()
    paginator = Paginator(quotes, 10)  # Показує 10 цитат на сторінці
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'author/quote_page.html', {'tag': tag, 'quotes': quotes, 'author': author, 'page_obj': page_obj})


