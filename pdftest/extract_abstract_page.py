import pymupdf

doc = pymupdf.open("pdf.pdf")

num_of_pages = doc.page_count
abstract_page_num = 0

for i in range(doc.page_count):
    if doc.search_page_for(i, 'Abstract', quads=False):
        abstract_page_num = i
        break

print(abstract_page_num)
doc.select([abstract_page_num])
doc.save('extracted_abstract_page.pdf')