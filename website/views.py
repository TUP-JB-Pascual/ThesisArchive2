from django.shortcuts import render
from django.views import generic
from django.views.decorators.clickjacking import xframe_options_exempt
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

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
    
class ThesisUpdateView(generic.UpdateView):
    model = Thesis
    template_name = 'thesis_update.html'
    form_class = ThesisForm
    
class ThesisDeleteView(generic.DeleteView):
    model = Thesis
    template_name = 'thesis_delete.html'
    success_url = reverse_lazy('thesis_list')
