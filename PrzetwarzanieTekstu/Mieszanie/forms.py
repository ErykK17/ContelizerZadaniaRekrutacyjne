from django import forms

from .models import File


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if not file.name.endswith('.txt'):
                raise forms.ValidationError('Plik musi mieć rozszerzenie .txt')
        return file
    