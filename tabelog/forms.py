from django import forms
from .models import Category, Pref, User, Review
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


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


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['score', 'comment']
