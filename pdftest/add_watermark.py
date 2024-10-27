import pymupdf

doc = pymupdf.open("pdf.pdf") # open a document
num_of_pages = doc.page_count

for page_index in range(num_of_pages): # iterate over pdf pages
    page = doc[page_index] # get the page

    # insert an image watermark from a file name to fit the page bounds
    # page.insert_image(page.bound(),filename="watermark.png", overlay=True)
    page.insert_image(page.bound(),filename="samplemark.png", overlay=True)
    
doc.save("watermarked-document.pdf") # save the document with a new filename