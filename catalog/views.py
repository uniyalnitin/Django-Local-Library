from django.shortcuts import render, get_object_or_404
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
from django.http import HttpResponse
# Create your views here.
def index(request):
	num_books = Book.objects.all().count()
	num_instances = BookInstance.objects.all().count()

	num_instances_available = BookInstance.objects.filter(status__exact='a').count()

	num_authors = Author.objects.count()

	context = {
		'num_books':num_books,
		'num_instances':num_instances,
		'num_instances_available':num_instances_available,
		'num_authors': num_authors
	}

	return render(request,'catalog/index.html',context=context)

class BookListView(generic.ListView):
	model = Book
	template_name = 'catalog/book_list.html'
	paginate_by=1
	
	def get_context_data(self, **kwargs):
		context = super(BookListView, self).get_context_data(**kwargs)
		context['some data']= 'This is just some data'
		return context

class BookDetailView(generic.DetailView):
	model = Book
	template_name = 'catalog/book_detail.html' 
	
	def book_detail_view(request, primary_key):
		book = get_object_or_404(Book, id=primary_key)
		return render(request, 'catalog/book_detail.html', context={'book': book})

class AuthorListView(generic.ListView):
	model = Author
	template_name = 'catalog/author_list.html'
	paginate_by=1

class AuthorDetailView(generic.DetailView):
	model = Author
	template_name ='catalog/author_detail.html'

	def author_detail_view(request,primary_key):
		author = get_object_or_404(Author,primary_key)
		return render(request,'catalog/author_detail.html', context={'author':author})