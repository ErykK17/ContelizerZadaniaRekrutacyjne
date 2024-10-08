from django import forms

class PeselForm(forms.Form):
    pesel = forms.CharField(
        max_length=11,
        widget=forms.TextInput(attrs={'placeholder': 'Wprowadź numer PESEL'})
    )
    def pesel_clean(self):
        pesel = self.cleaned_data.get('pesel')
        return pesel
    