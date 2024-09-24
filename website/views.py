from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.decorators.clickjacking import xframe_options_exempt
from django.urls import reverse_lazy

from .forms import ThesisForm
from .models import Thesis

class HomePageView(ListView):
    model = Thesis
    template_name = 'home.html'

class ThesisPublishView(CreateView):
    model = Thesis
    template_name = 'thesis_publish.html'
    form_class = ThesisForm
    #messages.success(request, "Upload Successful.")

class ThesisListView(ListView):
    model = Thesis
    template_name = 'thesis_list.html'

class XFrameOptionsExemptMixin:
    @xframe_options_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ThesisDetailView(XFrameOptionsExemptMixin, DetailView):
    model = Thesis
    template_name = 'thesis_detail.html'
    
class ThesisUpdateView(UpdateView):
    model = Thesis
    template_name = 'thesis_update.html'
    form_class = ThesisForm
    
class ThesisDeleteView(DeleteView):
    model = Thesis
    template_name = 'thesis_delete.html'
    success_url = reverse_lazy('thesis_list')
