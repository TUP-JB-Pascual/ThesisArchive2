from .models import Thesis
from django import forms

class ThesisForm(forms.ModelForm):
    class Meta:
        model = Thesis
        fields = ['published_date', 'title', 'author', 'pdf_file']
        widgets = {
            'published_date': forms.DateInput(attrs={'type': 'date'}),
            'author': forms.HiddenInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super(ThesisForm, self).__init__(*args, **kwargs)
        self.fields['published_date'].widget.attrs['class'] = 'form-control'
        self.fields['published_date'].widget.attrs['placeholder'] = 'Published Date'
        self.fields['published_date'].label = 'Published Date:'

        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['title'].widget.attrs['placeholder'] = 'Title'
        self.fields['title'].widget.attrs['rows'] = '5'
        self.fields['title'].widget.attrs['style'] = 'resize:none'
        self.fields['title'].label = 'Title:'

        self.fields['author'].widget.attrs['class'] = 'form-control'
        self.fields['author'].widget.attrs['placeholder'] = 'Author'
        self.fields['author'].widget.attrs['id'] = 'author'
        #self.fields['author'].widget.attrs['readonly'] = 'readonly'
        self.fields['author'].label = 'Author:'
        
        self.fields['pdf_file'].widget.attrs['class'] = 'form-control'
        self.fields['pdf_file'].widget.attrs['placeholder'] = 'PDF'
        self.fields['pdf_file'].label = 'Thesis PDF File:'
