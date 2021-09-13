#!/usr/bin/env python
# coding: utf-8

# # Automate Data Intake from PDFs

# In[1]:


#Load packages
import os
'''
go to anaconda powershell prompt and enter:
pip install pdfminer
pip install pdfreader
make sure not connected to VPN
'''
import pdfreader
from pdfreader import SimplePDFViewer


# ## Step 1: Find all PDFs

# In[2]:


# For non-PDFs (ex word documents), need to manually convert prior to running this program
pdfs = [f for f in os.listdir('testpdfs/') if f.endswith(".pdf")]


# ## Step 2: Read in PDF Data

# In[5]:


pdfstring = "testpdfs/ALASKA_PACIFIC_UNIVERSITY__qber_form_january_2021.pdf"
fd = open(pdfstring, "rb")
[school, __] = pdfstring.split("__")
viewer = SimplePDFViewer(fd)
viewer.render()


# In[7]:


plain_text = "".join(tviewer.canvas.strings)
plain_text


# In[8]:


# only 25 $0 after second $422100 but should be 43
print("Azusa" in plain_text)


# In[ ]:





# In[12]:


import sys
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import resolve1


# In[14]:


filename = "testpdfs/ALASKA_CHRISTIAN_COLLEGE__Dec.-31-2020-ACC-HEERF-quarterly-reporting.pdf"
fp = open(filename, 'rb')

parser = PDFParser(fp)
doc = PDFDocument(parser)
fields = resolve1(doc.catalog['AcroForm'])['Fields']
form = {}
names = []
for i in fields:
    field = resolve1(i)
    name, value = field.get('T'), field.get('V')
    form[name] = value
    names.append(name)


# In[15]:


for name in names: print(name, form[name])


# In[ ]:


data_dict = {'Institution Name': 'name', 'Covering Quarter Ending': 'quarter', 'Total Amount of Funds Awarded Section a1 Institutional Portion': 'total_award_a1',
            } #finish this


# In[79]:


data_categories = ['name', 'quarter', 'totalaward_a1', 'totalaward_a2', 'totalaward_a3',
                  'finaid_a1', 'finaid_a2', 'finaid_a3', 'reimburse_a1', 'reimburse_a2', 'reimburse_a3',
                  'tuition_a2', 'tuition_a3', 'tech_a1', 'tech_a2', 'tech_a3',
                  'internet_a1', 'internet_a2', 'internet_a3', 'housing_a1', 'housing_a2', 'housing_a3',
                  'food_a1', 'food_a2', 'food_a3', 'class_a1', 'class_a2', 'class_a3',
                  'safety_a1', 'safety_a2', 'safety_a3', 'equipmentnum_a1', 'equipmentnum_a2', 'equipmentnum_a3',
                  'enrollment_a1', 'enrollment_a2', 'enrollment_a3', 'nontuition_a1', 'nontuition_a2', 'nontuition_a3',
                  'training_a1', 'training_a2', 'training_a3', 'equipmentlearn_a1', 'equipmentlearn_a2', 'equipmentlearn_a3',
                  'othera1_a1', 'othera2_a2', 'othera3_a3', 'total_a1', 'total_a2', 'total_a3', 'total_quarter']


# In[83]:


print(len(data_categories))


# In[ ]:





# In[ ]:





# In[7]:


from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO


# In[12]:


resource_manager = PDFResourceManager()
fake_file_handle = StringIO()
converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
page_interpreter = PDFPageInterpreter(resource_manager, converter)

with open(pdfstring, 'rb') as fh:

    for page in PDFPage.get_pages(fh,
                                  caching=True,
                                  check_extractable=True):
        page_interpreter.process_page(page)

    text = fake_file_handle.getvalue()

# close open handles
converter.close()
fake_file_handle.close()

print(text)


# In[ ]:





# In[ ]:





# In[24]:


from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import HTMLConverter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import re
import csv


# In[29]:


def convert_pdf_to_html(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = HTMLConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0 #is for all
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str


# In[30]:


print(convert_pdf_to_html(pdfstring))


# In[ ]:




