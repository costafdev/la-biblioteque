import datetime
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from catalog.models import BookInstance

class RenewBookForm(forms.Form):
    # Formulario para renovaçao do aluguel do livro
    renew_date = forms.DateField(help_text="Merci de saisir un jour jusqu'à 2 semaines.")

    def clean_renew_date(self):
        # Funçao que valida a data
        data = self.cleaned_data['renew_date']

        # Verifica se a data nao esta no passado
        if data < datetime.date.today():
            raise ValidationError(_("Renouver pour le passé ce n'est pas possible... encore."))

        # Verifica se a data esta na faixa permitida (hj + 2 semanas)
        if data > datetime.date.today() + datetime.timedelta(weeks=2):
            raise ValidationError(_("C'est trop !"))

        # LEMBRAR: sempre retornar a data validade
        return data

class RenewBookModelForm(ModelForm):
    # Faz a mesma coisa que RenewBookForm() mas em ModelForm
    """
    Ao invés de recriar as definiçoes do modelo no Form, é mais facil usar ModelForm para criar
    um formulario a partir do modelo
    """
    def clean_due_back(self):
        # Funçao que valida a data de renovaçao
        
        data = self.cleaned_data['due_back']

        if data < datetime.date.today():
            raise ValidationError(_('J\'ai dit déjà: ce n\'est pas possible renouveler poru le passé'))
        if data > datetime.date.today() + datetime.timedelta(weeks=2):
            raise ValidationError(_('C\'est trop longtemps !'))

        return data

    class Meta:
        model = BookInstance
        fields = [
            'due_back',
        ]
        labels = {
            'due_back': _('Nouveau jour de retour'),
        }
        help_texts = {
            'due_back': _('Nouveau jour d\'ici à 2 semaines.'),
        }