from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from .forms import PeselForm
from django.shortcuts import redirect


def get_gender(pesel):
    """Zwraca płeć na podstawie numeru PESEL."""
    return 'Kobieta' if int(pesel[9]) % 2 == 0 else 'Mężczyzna'


def get_birthday(pesel):
    """Zwraca datę urodzenia w formacie YYYY-MM-DD na podstawie numeru PESEL."""
    month = pesel[3] if int(pesel[2]) % 2 == 0 else '1' + pesel[3] #jeśli 3 cyfru peselu jest nieparzysta 
    #to oznacza ze miesiac urodzenia jest wyzszy bądź równy 10
    year_prefix = {0: '19', 80: '18', 20: '20', 40: '21', 60: '22'}
    year_code = int(pesel[2:4]) - int(month) #Sprawdzane jest ile dodano do miesiąca, żeby określić przediał lat urodzenia 
    year = year_prefix[year_code] + pesel[0:2]
    day = pesel[4:6]
    return f'{year}-{int(month):02d}-{day}'


def validate_pesel(pesel):
    """Sprawdza długość PESEL oraz poprawność numeru kontrolnego."""
    weights = {1: 1, 2: 3, 3: 7, 4: 9, 5: 1, 6: 3, 7: 7, 8: 9, 9: 1, 10: 3, 11: 1}
    length_is_valid = len(pesel) == 11 # jeśli pesel ma 11 cyfr, zmienna przyjmuje wartość True
    
    total_sum = sum(int(digit) * weights[index] for index, digit in enumerate(pesel, start=1))
    control_number_is_valid = (total_sum % 10) == 0 #Jeśli ostatnia cyfra sumy iloczynow cyfr PESEL z ich przypisanymi wagami
    #wynosi zero, liczba kontrolna jest prawidłowa

    birth_month_is_valid = int(pesel[2]) % 2 ==0 or int(pesel[2]) % 2 != 0 and int(pesel[3]) <= 2

    return length_is_valid, control_number_is_valid, birth_month_is_valid


class PeselValidation(FormView):
    """Widok z formularzem do podania PESELU do sprawdzenia."""
    template_name = 'validate_pesel.html'
    form_class = PeselForm
    success_url = reverse_lazy('result')

    def form_valid(self, form):
        pesel = form.cleaned_data['pesel']
        self.request.session['pesel'] = pesel
        return redirect('result')


class ResultView(TemplateView):
    """Widok wyświetlający wynik walidacji PESEL oraz pobrane infromacje o osobie."""
    template_name = 'result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pesel = self.request.session.get('pesel')
        
        if pesel:
            length_is_valid, control_number_is_valid, birth_month_is_valid = validate_pesel(pesel)
            context['pesel'] = pesel
            context['length'] = "Prawidłowa długość" if length_is_valid else "Nieprawidłowa długość"
            context['control_number'] = "Numer kontrolny prawidłowy" if control_number_is_valid else "Nieprawidłowy numer kontrolny"
            context['birth_month_valid'] = "Miesiąc urodzenia poprawny" if birth_month_is_valid else "Nieprawidłowy miesiąc urodzenia"
            context['birthday'] = get_birthday(pesel)
            context['gender'] = get_gender(pesel)
        else:
            context['pesel'] = 'Brak peselu'
        
        return context
