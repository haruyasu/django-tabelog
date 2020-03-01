
from django.shortcuts import render, redirect

from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView

class IndexView(TemplateView):
  template_name = 'tabelog/index.html'

