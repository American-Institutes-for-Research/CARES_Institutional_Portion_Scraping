# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 09:32:02 2021

@author: amiller
"""

import sys
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import resolve1
import pandas as pd

# In[14]:


#filename = "./test_files/HEERF-Quarterly-Report-Jan-March%20PDF.pdf"
filename = "HEERF Quarterly Budget and Expenditure Reporting - V1_3_1.pdf"
fp = open("./test_files/"+filename, 'rb')

parser = PDFParser(fp)
doc = PDFDocument(parser)
res = resolve1(doc.catalog)

if 'AcroForm' not in res:
    raise ValueError("No AcroForm Found")
    
fields = resolve1(doc.catalog['AcroForm'])['Fields'] ## this line requires that there are acroform spaces

#df = pd.DataFrame()

form = {}
names = []
values =[]
for i in fields:
    field = resolve1(i)
    name, value = field.get('T'), field.get('V')
    form[name] = value
    names.append(name)
    values.append(value)

#%%
obj_df = pd.DataFrame()
#df = pd.DataFrame.from_dict(form, )
obj_df['names']=names
obj_df['values']=values
str_df = obj_df.stack().str.decode('utf-8').unstack()

#%%
import tika
from tika import parser

# Start running the tika service
tika.initVM()

import os


#%%

root_dir = '.'
draft_dir = os.path.join(root_dir, 'test_files')

draft_files = [file for file in os.listdir(draft_dir) if not file.startswith('~')]

#draft_files = [filename]

for draft_file in draft_files:
    # Parse data from file
    file_data = parser.from_file(os.path.join(draft_dir, draft_file))
    # Get files text content
    text = file_data['content']
    cleaned_text = str(text).strip()
    
    # Save converted files
    with open(os.path.join(root_dir, 'text_versions', "{}.txt".format(draft_file.split('.')[0])), "w") as text_file:
        text_file.write(cleaned_text)

#%%

import pandas as pd

df = pd.DataFrame(columns=['line'], dtype='string')

txt_file_path = "./text_versions/HEERF Quarterly Budget and Expenditure Reporting - V1_3_1.txt"

def extractLines(txtfile):    
    #lines_to_read = range(163,232)
    fp = open(txtfile, 'r', encoding='UTF-8')
    lines = fp.readlines()
    for item in lines:
        if ((not (u"\u00A0" in item)) & (":" in item)):
            idx = lines.index(item)
            #df_idx = idx - 163
            df.loc[idx,'line']=item
            df.loc[idx,'line2']=item.strip()
    #df.reset_index()
    fp.close()

extractLines(txt_file_path)
df.index = pd.RangeIndex(len(df.index))

for item in df['line2']:
    idx = list(df['line2']).index(item)
    splitList = item.split(':')
    question = splitList[0].strip()
    ans = splitList[1].strip()
    df.loc[idx,'question'] = question
    df.loc[idx,'answer'] = ans