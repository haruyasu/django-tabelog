from django import forms
from .models import Category, Pref, Review


class SearchForm(forms.Form):
    selected_pref = forms.ModelChoiceField(
        label='都道府県',
        required=False,
        queryset=Pref.objects,
    )
    selected_category = forms.ModelChoiceField(
        label='カテゴリ',
        required=False,
        queryset=Category.objects,
    )
    freeword = forms.CharField(
        label='フリーワード',
        required=False,
        min_length=2,
        max_length=100
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        selected_pref = self.fields['selected_pref']
        selected_category = self.fields['selected_category']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['score', 'comment']
