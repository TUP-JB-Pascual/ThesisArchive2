from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import generic
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
import os
import pymupdf

User = get_user_model()

from .forms import ThesisForm
from .models import Thesis

def home(request):
    context = {}
    return render(request, 'home.html', context)

class HomePageView(generic.ListView):
    model = Thesis
    template_name = 'home.html'

class ThesisPublishView(generic.CreateView):
    model = Thesis
    template_name = 'thesis_publish.html'
    form_class = ThesisForm
    #messages.success(request, "Upload Successful.")

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)
    
    def get_initial(self):
        initial = super().get_initial()
        initial['author'] = self.request.user.id
        return initial
    
    def post(self, request, *args, **kwargs):
        print(request.POST)
        return super().post(request, *args, **kwargs)

class ThesisListView(generic.ListView):
    model = Thesis
    template_name = 'thesis_list.html'

class XFrameOptionsExemptMixin:
    @xframe_options_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ThesisDetailView(XFrameOptionsExemptMixin, generic.DetailView):
    model = Thesis
    template_name = 'thesis_detail.html'

def ThesisUpdateView(request, pk):
    if request.user.is_authenticated:
        instance = Thesis.objects.get(id=pk)
        form = ThesisForm(request.POST or None, request.FILES or None, instance=instance)
        if form.is_valid():
            current_val = Thesis.objects.get(id=pk)
            update_delete(current_val.pdf_file.name)
            form.save()
            create_update_pdf(instance.pdf_file.name)
            return redirect('thesis_detail', pk = instance.pk)
        context = {'form': form}
        return render(request, 'thesis_update.html', context)
    else:
        messages.success(request, "You must be logged in")
        return ('login')
    
def update_delete(pdf_name):
    pdf_name = 'media/' + pdf_name
    if os.path.exists(pdf_name):
        os.remove(pdf_name)
        print(pdf_name, " has been deleted.")
        abstract_pdf_name = pdf_name.split('.')
        abstract_pdf_name = abstract_pdf_name[0] + '_abstract.' + abstract_pdf_name[1]
        if os.path.exists(abstract_pdf_name):
            os.remove(abstract_pdf_name)
            print(abstract_pdf_name, " has been deleted.")
        # FOR WATERMARK
        water_pdf_name = pdf_name.split('.')
        water_pdf_name = water_pdf_name[0] + '_water.' + water_pdf_name[1]
        if os.path.exists(water_pdf_name):
            os.remove(water_pdf_name)
            print(water_pdf_name, " has been deleted.")

def create_update_pdf(pdf_name):
    pdf_name = 'media/' + pdf_name
    doc = pymupdf.open(pdf_name)
    # GET ABSTRACT PAGE
    abstract_page_num = 0
    for i in range(doc.page_count):
        if doc.search_page_for(i, 'Abstract', quads=False):
            abstract_page_num = i
            break
    # WATERMARK
    for page_index in range(abstract_page_num + 1, doc.page_count): # iterate over pdf pages
        page = doc[page_index] # get the page
        # insert an image watermark from a file name to fit the page bounds
        # page.insert_image(page.bound(),filename="watermark.png", overlay=True)
        page.insert_image(page.bound(),filename='media/samplemark.png', overlay=True)
    water_pdf_name = pdf_name.split('.')
    water_pdf_name = water_pdf_name[0] + '_water.' + water_pdf_name[1]
    doc.save(water_pdf_name) # save the document with a new filename
    # WATERMARK END

    # SAVE ABSTRACT
    doc.select([abstract_page_num])
    abstract_pdf_name = pdf_name.split('.')
    abstract_pdf_name = abstract_pdf_name[0] + '_abstract.' + abstract_pdf_name[1]
    doc.save(abstract_pdf_name)

'''
class ThesisUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Thesis
    template_name = 'thesis_update.html'
    #form_class = ThesisForm
    form_class = ThesisForm
    reverse_lazy = 'thesis_list'
    
    def post(self, request, *args, **kwargs):
        print(request.POST)
        return super().post(request, *args, **kwargs)
'''
class ThesisDeleteView(generic.DeleteView):
    model = Thesis
    template_name = 'thesis_delete.html'
    success_url = reverse_lazy('thesis_list')
