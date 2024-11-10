from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import generic
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
import os
import pymupdf

import random
import string
from django.utils import timezone
from datetime import timedelta
from django.http import Http404
from .models import TempURL
from .forms import RequestForm

from django.http import FileResponse
from django.conf import settings

User = get_user_model()

from .forms import ThesisForm
from .models import Thesis

from django.core.mail import send_mail
from django.http import HttpResponseRedirect

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

def ThesisDetailView(request, pk):
    thesis = get_object_or_404(Thesis, pk=pk)
    abstract_pdf_name = thesis.pdf_file.name
    abstract_pdf_name = abstract_pdf_name.split('.')
    abstract_pdf_name = abstract_pdf_name[0] + '_abstract.' + abstract_pdf_name[1]
    thesis.visits += 1
    thesis.save()
    return render(request, 'thesis_detail.html', {'thesis': thesis, 'abstract_pdf_name': abstract_pdf_name})

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

class ThesisDeleteView(generic.DeleteView):
    model = Thesis
    template_name = 'thesis_delete.html'
    success_url = reverse_lazy('thesis_list')

def generate_random_key(length=32):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_temp_url(pk, email, first_name, last_name):
    requested_pdf = get_object_or_404(Thesis, pk=pk)
    requested_pdf.downloads += 1
    requested_pdf.save()
    title = requested_pdf.title
    pdf_file_path = requested_pdf.pdf_file.name
    pdf_file_path = pdf_file_path.split('.')
    pdf_file_path = pdf_file_path[0] + '_water.' + pdf_file_path[1]
    url_key = generate_random_key()
    expiration_date = timezone.now() + timedelta(days=3)
    pdf_file = TempURL.objects.create(
        url_key=url_key,
        title=title,
        pdf_file=pdf_file_path,
        expiration_date=expiration_date,
        email = email,
        first_name = first_name,
        last_name = last_name
    )

def temp_url_redirect(request, url_key):
    try:
        temp_pdf = TempURL.objects.get(url_key=url_key)
        if temp_pdf.is_expired():
            raise Http404("This temporary PDF link has expired.")
        pdf_file_path = temp_pdf.pdf_file.path
        if os.path.exists(pdf_file_path):
            return FileResponse(open(pdf_file_path, 'rb'), content_type='application/pdf')
        raise Http404("PDF file not found.")
    except TempURL.DoesNotExist:
        raise Http404("Temporary PDF URL does not exist.")

def ThesisDownload(request, pk):
    pass

def ThesisRequestView(request, pk):
    thesis = Thesis.objects.get(id=pk)
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            generate_temp_url(pk, email, first_name, last_name)
            messages.success(request, f'Thank you, {first_name}  {last_name}! Your request has been sent.')
            return redirect('thesis_detail', pk=pk)
        else:
            messages.error(request, 'There was an error with your form submission. Please try again.')
    else:
        form = RequestForm()
    return render(request,'thesis_request.html', {'form': form, 'thesis': thesis})

class ThesisRequestListView(generic.ListView):
    model = TempURL
    template_name = 'request_list.html'
    context_object_name = 'request_list'
    #paginate_by = 10

def RequestDetailView(request, pk):
    thesis_request = get_object_or_404(TempURL, pk=pk)
    if request.method == 'POST':
        print(request.POST)
        # Email content
        subject = "Thesis Request"
        message = "Good day! {} {}, your request for a PDF copy of the thesis titled {} has been accepted. DO NOT CLICK ON ANOTHER TAB UNTIL YOU HAVE CLICKED 'DOWNLOAD', IT WILL CLOSE!!! This link will expire in three days. http://127.0.0.1:8000/temp/pdf/{}".format(thesis_request.first_name, thesis_request.last_name, thesis_request.title, thesis_request.url_key)
        recipient_list = [thesis_request.email]  # The recipient's email

        # Send the email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False,
        )
        messages.success(request, "Request Acceptance Email has been sent to {}.".format(thesis_request.email))
        return redirect('request_list')
    return render(request, 'request_detail.html', {'thesis_request': thesis_request})

def RequestReject(request, pk):
    thesis_request = get_object_or_404(TempURL, pk=pk)
    if request.method == 'POST':
        print(request.POST)
        return redirect('request_list')
    return render(request, 'request_reject.html', {'thesis_request': thesis_request})
