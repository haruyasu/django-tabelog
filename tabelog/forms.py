from django import forms
from .models import Category, Pref


class SearchForm(forms.Form):
    selected_pref = forms.ModelChoiceField(
        label='都道府県',
        required=False,
        queryset=Pref.objects,
    )
    selected_category = forms.ModelChoiceField(
        label='業態',
        required=False,
        queryset=Category.objects,
    )
    freeword = forms.CharField(
        min_length=2, max_length=100, label='', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        selected_pref = self.fields['selected_pref']
        selected_category = self.fields['selected_category']
