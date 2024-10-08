from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from .forms import FileForm
from .models import File
import re, random


def scramble_word(word):
    if len(word) <=3:
        return word

    first_letter = word[0]
    last_letter = word[-1]
    middle = list(word[1:-1])  
    random.shuffle(middle)
    return first_letter + ''.join(middle) + last_letter
    

def scramble_text(text):
    words = re.findall(r'\w+|[^\w\s]', text)

    scrambled_words = []
    for word in words:
        if word.isalpha():
            scrambled_words.append(scramble_word(word))
        else:
            if scrambled_words:
                scrambled_words[-1] += word
    scrambled_text = ' '.join(scrambled_words).strip()
    return scrambled_text


class  UploadFileView(CreateView):
    model = File
    form_class = FileForm
    template_name = 'upload.html'
    success_url = reverse_lazy('result')
    
    def form_valid(self,form):
        text_file = form.cleaned_data['file']
        content = text_file.read().decode('utf-8')
        content_scrambled = scramble_text(content)
        print(content_scrambled)
        self.request.session['content_scrambled'] = content_scrambled
        return redirect('result')
    

class ResultView(TemplateView):
    template_name = 'result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['result'] = self.request.session.get('content_scrambled', 'No content available')
        return context
