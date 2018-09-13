from django.shortcuts import render, get_object_or_404
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse

from catalog.forms import RenewBookForm
# Create your views here.
def index(request):
	num_books = Book.objects.all().count()
	num_instances = BookInstance.objects.all().count()

	num_instances_available = BookInstance.objects.filter(status__exact='a').count()

	num_authors = Author.objects.count()

	num_visits = request.session.get('num_visits',0)
	request.session['num_visits'] = num_visits+1

	context = {
		'num_books':num_books,
		'num_instances':num_instances,
		'num_instances_available':num_instances_available,
		'num_authors': num_authors,
		'num_visits': num_visits
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

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
	model = BookInstance
	template_name = 'catalog/bookinstance_list_borrowed_user.html'
	paginate_by = 10

	def get_queryset(self):
		return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
	model = BookInstance
	permission_required = 'catalog.can_mark_returned'
	template_name= 'catalog/bookinstance_list_borrowed_all.html'
	paginate_by=10

	def get_query_set(self):
		return BookInstance.objects.filter(status__exact='o').order_by('due_back')


import datetime
from django.contrib.auth.decorators import permission_required

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
	book_instance = get_object_or_404(BookInstance,pk=pk)

	if request.method =='POST':

		# Create a form instance and populate it with data from the request (binding):
		book_renewal_form = RenewBookForm(request.POST)

		if book_renewal_form.is_valid():
			 # process the data in form.cleaned_data as required (here we just write it to the model due_back field
			book_instance.due_back = book_renewal_form.cleaned_data['renewal_date']
			book_instance.save()

			return HttpResponseRedirect(reverse('all-borrowed'))

	else:
		proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
		book_renewal_form = RenewBookForm(initial={'renewal_date':proposed_renewal_date,})

	context = {
		'form':book_renewal_form,
		'book_instance':book_instance,
	}

	return render(request, 'catalog/book_renew_librarian.html',context)

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from catalog.models import Author

class AuthorCreate(CreateView):
	model = Author
	fields = '__all__'
	initial = {'date_of_birth':'05/01/2018' }

class AuthorUpdate(UpdateView):
	model = Author
	fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(DeleteView):
	model = Author
	success_url = reverse_lazy('authors')
	