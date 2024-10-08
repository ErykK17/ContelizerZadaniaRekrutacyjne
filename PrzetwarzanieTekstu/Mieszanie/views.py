import random
import re

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import FileForm
from .models import File


def scramble_word(word):
    """ Funkcja mieszająca środkowe litery pojedyńczego słowa. """
    if len(word) <=3:
        return word #Jeśli słowo ma 3 lub mniej liter, jest zwracany od razu, ponieważ ma maksymalnie jedną środkową literę

    first_letter = word[0]
    last_letter = word[-1]
    middle = list(word[1:-1]) #Wydzielenie części słowa.
    random.shuffle(middle) #Pomieszanie środka słowa
    return first_letter + ''.join(middle) + last_letter #Połączenie pomieszanego środka z resztą liter
    

def scramble_text(text):
    """Funkcja mieszająca wszystkie słowa w tekście z pominięciem znaków interpunkcyjnych"""
    words = re.findall(r'\w+|[^\w\s]', text) #Wyrażenie regularne które pozyskuje słowa i znaki interpunkcyjne z tekstu

    scrambled_words = []
    for word in words:
        if word.isalpha():
            scrambled_words.append(scramble_word(word)) #Jeśli word składa się z samych liter, jest mieszane i dodawane do listy
        else:
            if scrambled_words:
                scrambled_words[-1] += word #Jeśli word to znak interpunkcyjny, dodawany jest na koniec ostatniego wyrazu
    scrambled_text = ' '.join(scrambled_words).strip() #Łączenie wyrazów w zdanie (wyrazy oddzielone spacjami) 
    return scrambled_text


class  UploadFileView(CreateView): #Widok uploadowania pliku tekstowego
    model = File
    form_class = FileForm
    template_name = 'upload.html'
    success_url = reverse_lazy('result')
    
    def form_valid(self,form): # Jeśli formularz jest prawidłowy, na tekśćie z pliku wykonywana jest funkcja mieszania
        text_file = form.cleaned_data['file']
        content = text_file.read().decode('utf-8')
        content_scrambled = scramble_text(content)
        self.request.session['content_scrambled'] = content_scrambled #Wynik zapisywany jest w sesji
        return redirect('result')
    

class ResultView(TemplateView): #Widok wyświetlający rezultat
    template_name = 'result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['result'] = self.request.session.get('content_scrambled', 'Brak tekstu') #Jeśli tekst został
        #prawidłowo pozyskany, jest wyświetlany. Jeśli nie wyświetlony jest odpowiedni komunikat.
        return context
