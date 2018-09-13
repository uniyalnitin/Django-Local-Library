from django.contrib import admin
from catalog.models import Author, Genre, Book, BookInstance

# Register your models here.
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
	list_display= ('last_name','first_name','date_of_birth','date_of_death')
	fields = ['first_name','last_name',('date_of_birth','date_of_death')]
# admin.site.register(Author, AuthorAdmin)

class BooksInstanceInline(admin.TabularInline):
	model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ('title','author','display_genre')
# admin.site.register(Book, BookAdmin)
	inlines = [BooksInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
	list_display=('book', 'status','borrower','due_back','id')
	list_filter = ('status','due_back')

	fieldsets= (
		(None, {
			'fields':('book','imprint','id')
			}),
		('Availablity',{
			'fields':('status','due_back', 'borrower')
			}),
		)
# admin.site.register(BookInstance, BookInstanceAdmin)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
	pass
# admin.site.register(Genre, GenreAdmin)

