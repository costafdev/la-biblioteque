from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
"""
Todas as vezes que os modelos forem atualizados é necessario fazer no console:
    py manage.py makemigrations
    py manage.py migrate 
"""

class Genre(models.Model):
    # Modelo Genre para definir o genero dos livros
    # é feito um modelo p/ permitir que os tipos de livros sejam gerenciados no banco de dados
    name = models.CharField(max_length=200, help_text='Adicione um gênero (e.g. Romance, Ficçao)')

    def __str__(self):
        # String para representar o obj
        return self.name

class Language(models.Model):
    # Modelo language para definir o idioma do livro
    # é feito um modelo p/ permitir que os idiomas sejam gerenciados no banco de dados
    name = models.CharField(max_length=200, help_text='Idioma do livro')

    def __str__(self):
        # String represento o obj
        return self.name

class Book(models.Model):
    # Este modelo representa um livro (obra) e nao um exemplar de um livro
    title = models.CharField(max_length=200)

    # ForeignKey pq um livro pode ter um autor, mas um autor pode ter varios livros
    # Autor vai ser uma string pq o obj ainda nao foi declarado
    # null=True permite armazenar NULL se nenhum autor for selecionado
    # on_delete=models.SET_NULL armazena NULL se o autor for excluido
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    # Sinopse do livro
    summary = models.TextField(max_length=1000, help_text='Breve descriçao do livro')

    # ISBN do livro
    isbn = models.CharField('ISBN', max_length=13, help_text='13 caracteres <a href="https://www.isbn-international.org/content/what-isbn">ISBN</a>')

    # ManyToManyField é usado pq um genero pode ter muitos livros e um livro pode abranger muitos generos
    # Note que como a classe Genre ja foi declarada entao podemos chama-la diretamente
    genre = models.ManyToManyField(Genre, help_text='Selecione um genero')

    # ForeignKey pq um livro so pode ter um idiomas, mas um idioma abrange muitos livros
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def display_genre(self):
        # Cria uma string para visualizaçao do genero do livro
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    display_genre.short_description = 'Genre'

    def __str__(self):
        # String representando o obj
        return self.title

    def get_absolute_url(self):
        # Retorna a url para acessar detalhes desse livro
        """
        TODO:
        * definir um mapa de url com nome book-detail
        * associar à uma view e um template
        """
        return reverse('book-detail', args=[str(self.id)])

import uuid

class BookInstance(models.Model):
    # Esta classe representa um exemplar de um livro

    # UUIDField define o 'id' como primary_key desse modelo
    # Este tipo aloca um unico valor global pra cada obj
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='ID unico')

    # ForeignKey pq um livro pode ter muitos exemplares, mas um exemplar é de apenas um livro
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)

    # Exemplar do livro
    imprint = models.CharField(max_length=200, blank=True)

    # due_back define a data que o livro deve ficar disponivel
    # Pode ser blank ou null (se o exemplar estiver disponivel)
    due_back = models.DateField(null=True, blank=True)

    # Usuario que pegou o livro
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # Estado do exemplar
    LOAN_STATUS = (
        ('i', 'Indisponivel'),
        ('a', 'Alugado'),
        ('d', 'Disponivel'),
        ('r', 'Reservado'),
    )

    # status define uma lista de opçoes
    # default='i' para quando os exemplares forem criados e nao estiverem disponiveis para locaçao ainda
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='i', help_text='Disponibilidade')

    class Meta:
        # Ordena o 'due_back' quando é retornado em uma query
        ordering = ['due_back']
        permissions = (
            ("can_mark_returned", "Marquer comme retourné"), # Permissao para bibliotecarios
        )

    def __str__(self):
        return f'{self.id} ({self.book.title})'

    @property
    def is_overdue(self):
        # Verifica se o livro esta atrasado
        if self.due_back and date.today() > self.due_back:
            return True
        return False

class Author(models.Model):
    # Esta classe representa um(a) autor(a)

    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    data_nascimento = models.DateField(null=True, blank=True)
    data_morte = models.DateField('Data de Morte', null=True, blank=True)

    class Meta:
        ordering = ['sobrenome', 'nome']

    def get_absolute_url(self):
        # Retorna uma URL para acessar um autor especifico
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        # String representando este obj
        return f'{self.sobrenome}, {self.nome}'