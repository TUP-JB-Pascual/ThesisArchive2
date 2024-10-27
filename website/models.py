from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from django.urls import reverse
import os
import pymupdf
from django.db import transaction
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

def rename_pdf(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.title, ext)
    #filename = "%s_%s.%s" % (instance.title, filetype, ext)
    return os.path.join('thesis_pdf', filename)

class Thesis(models.Model):
    upload_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateField(null=True, blank=True)
    title = models.TextField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    pdf_file = models.FileField(upload_to=rename_pdf, max_length=256)

    # visits = models.IntegerField(default=0)

    def __str__(self):
        return(f"{self.title} by {self.author}")
    
    def get_absolute_url(self):
        return reverse('thesis_detail', kwargs= {'pk': self.id})


@receiver(post_save, sender=Thesis)
def create_extra_pdf(sender, instance, created, *args, **kwargs):
    if created:
        pdf_name = 'media/' + instance.pdf_file.name
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

@receiver(post_delete, sender=Thesis)
def delete_extra_pdf(sender, instance, *args, **kwargs):
    print("call delete")
    pdf_name = 'media/' + instance.pdf_file.name
    print(pdf_name)
    # FOR ABSTRACT
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

