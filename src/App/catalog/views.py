import datetime
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.models import BookInstance, Book, Author, Genre
from catalog.forms import RenewBookForm

# Create your views here.
def index(request):
    # Home page

    # Enumera a quantidade de livros e de copias
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Livros disponiveis
    num_instances_available = BookInstance.objects.filter(status__exact='d').count()

    # Numero de autores
    num_authors = Author.objects.all().count()

    # Numero de visitas
    num_visites = request.session.get('num_visites', 0)
    request.session['num_visites'] = num_visites + 1

    # Passa as variaveis para o template
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visites': num_visites,
    }

    # Renderiza o template HTML index.html com os dados da variavel context
    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = 2

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 2

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    # View com a lista dos livros alugados pelo usuario
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        # Retorna todos os exemplares de livros que estao com status 'alugado' pelo usuario e os ordena pela data de devoluçao
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='a').order_by('due_back')

class AllBooksLoanedListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all_users.html'
    paginate_by = 10

    def get_queryset(self):
        # Retorna todos os exemplares com status 'a' alugado e ordena pela data de devoluçao
        return BookInstance.objects.filter(status__exact='a').order_by('due_back')

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    # Funçao view para renovar um aluguel de um livro
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renew_date']
            book_instance.save()
            return HttpResponseRedirect(reverse('all-borrowed'))

    else:
        proposed_renew_date = datetime.date.today() + datetime.timedelta(weeks=2)
        form = RenewBookForm(initial={'renew_date': proposed_renew_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)