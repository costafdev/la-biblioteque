from django.contrib import admin
from catalog.models import Author, Genre, Book, BookInstance, Language

# Register your models here.

#ci-dessous c'est pas necessaire car les pages (genre et language) ont un seul champ
admin.site.register(Genre)
admin.site.register(Language)
"""
@admin.register(Book) == admin.site.register(Book, BookAdmin)
"""

class AuthorInline(admin.TabularInline):
    model = Book
    extra = 0

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('sobrenome', 'nome', 'data_nascimento', 'data_morte')
    fields = ['nome', 'sobrenome', ('data_nascimento', 'data_morte')]
    inlines = [AuthorInline]

"""

    isso serve para mostrar os dados das instancias dos livros como uma lista dentro da view do livro
    permitindo uma visualizacao mais completa com todas as copias dos livros e seus status
    
class BookInstanceInline(admin.TebularInline):
    model = BookInstance  # define o model 
    ...
    ...
    inlines = [BookInstanceInline]  # adiciona o modelo escolhido e todos os seus campos
    
"""

class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'imprint', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('book', 'status', 'due_back')
    fieldsets = (
        ('Dados da impressao', {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Disponibilidade', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )


"""admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)"""