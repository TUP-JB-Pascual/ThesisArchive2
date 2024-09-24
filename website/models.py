from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Thesis(models.Model):
    upload_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateField(null=True, blank=True)
    title = models.TextField(max_length=255)
    author = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='thesis_pdf', max_length=256)
    # visits = models.IntegerField(default=0)

    def __str__(self):
        return(f"{self.title} by {self.author}")
    
    def get_absolute_url(self):
        return reverse('thesis_detail', kwargs= {'pk': self.id})

