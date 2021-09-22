# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 09:32:02 2021

@author: amiller
"""
#%% 
""" ------------ pdf_2_txt by client ------------ """

import sys
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import resolve1
import pandas as pd

# In[14]:


#filename = "./test_files/HEERF-Quarterly-Report-Jan-March%20PDF.pdf"
#filename = "HEERF Quarterly Budget and Expenditure Reporting - V1_3_1.pdf"
#filename = "HEERF_Quarterly_Budget_and_Expenditure_Public_Posting_FINAL_accessible.pdf"
filename = "0621%20HEERF_Quarterly_Budget_and_Expenditure_Public-Avalon.pdf"
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
# """ ------------ pdf_2_txt by AIR ------------ """

# import tika
# from tika import parser

# # Start running the tika service
# tika.initVM()

# import os


# #%%

# root_dir = '.'
# draft_dir = os.path.join(root_dir, 'test_files')

# draft_files = [file for file in os.listdir(draft_dir) if not file.startswith('~')]

# #draft_files = [filename]

# for draft_file in draft_files:
#     # Parse data from file
#     file_data = parser.from_file(os.path.join(draft_dir, draft_file))
#     # Get files text content
#     text = file_data['content']
#     cleaned_text = str(text).strip()
    
#     # Save converted files
#     with open(os.path.join(root_dir, 'text_versions', "{}.txt".format(draft_file.split('.')[0])), "w") as text_file:
#         text_file.write(cleaned_text)

#%%

import pandas as pd

df = pd.DataFrame(columns=['line'], dtype='string')

#txt_file_path = "./text_versions/HEERF Quarterly Budget and Expenditure Reporting - V1_3_1.txt"
#txt_file_path = "./text_versions/HEERF_Quarterly_Budget_and_Expenditure_Public_Posting_FINAL_accessible.txt"
txt_file_path = "./text_versions/062120HEERFQuarterlyBudgetandExpenditurePublicAvalon.txt"

#%%
def extractLines(txtfile):    
    #lines_to_read = range(163,232)
    fp = open(txtfile, 'r', encoding='UTF-8')
    lines = fp.readlines()
    idx_list = []
    for item in lines:
        if ("Institution Name:" in item):
            start_idx = lines.index(item)
    for item in lines:
        if (lines.index(item) >= start_idx):
            idx = lines.index(item)
            df.loc[idx,'line']=item
            df.loc[idx,'line2']=item.strip()
    fp.close()

#%%
extractLines(txt_file_path)
df.index = pd.RangeIndex(len(df.index))

for item in df['line2']:
    idx = list(df['line2']).index(item)
    splitList = item.split(':')
    ans = splitList[-1].strip()
    #question = splitList[0].strip()+":"+splitList[1].strip
    question = item.replace(ans,'').strip()
    question = question[:-1]
    df.loc[idx,'question'] = question
    df.loc[idx,'answer'] = ans
    
#%%
compdf1 = pd.DataFrame()
compdf1['questions'] = str_df['names']
compdf1['answers']=str_df['values']

compdf2 = pd.DataFrame()
compdf2['questions'] = df['question']
compdf2['answers']=df['answer']

compared = pd.DataFrame()
compared = compdf1.compare(compdf2, keep_shape=False, keep_equal=False)

#%%
# 
# def(pdfile)
# #filename = "./test_files/HEERF-Quarterly-Report-Jan-March%20PDF.pdf"
# #filename = "HEERF Quarterly Budget and Expenditure Reporting - V1_3_1.pdf"
# filename = "HEERF_Quarterly_Budget_and_Expenditure_Public_Posting_FINAL_accessible.pdf"
# fp = open("./test_files/"+filename, 'rb')

# parser = PDFParser(fp)
# doc = PDFDocument(parser)
# res = resolve1(doc.catalog)

# if 'AcroForm' not in res:
#     raise ValueError("No AcroForm Found")
    
# fields = resolve1(doc.catalog['AcroForm'])['Fields'] ## this line requires that there are acroform spaces

# #df = pd.DataFrame()

# form = {}
# names = []
# values =[]
# for i in fields:
#     field = resolve1(i)
#     name, value = field.get('T'), field.get('V')
#     form[name] = value
#     names.append(name)
#     values.append(value)

#%%
obj_df = pd.DataFrame()
#df = pd.DataFrame.from_dict(form, )
obj_df['names']=names
obj_df['values']=values
str_df = obj_df.stack().str.decode('utf-8').unstack()

