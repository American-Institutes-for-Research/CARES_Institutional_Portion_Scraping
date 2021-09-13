"""
   +===================+========-========*========-========+===================+
   ||                               pdf_txt_2_df.py$                          ||
   ||                      by Abigail Miller (8/30/2021)                      ||
   ||                       American Institutes for Research                  ||
   ||                          CARES_Web_Scraping                             ||
   ||                                                                         ||
   || Description:                                                            ||
   || Takes in output from pdf_2_txt.py and copies information to dataframe   ||
   ||                                                                         ||
   ||                                                                         ||
   || Language:  Python 3.8.8                                                 ||
   || Graphics:  None                                                         ||
   || Downloads: None                                                         ||
   || Run time:  Approx. XX seconds                                           ||
   +===========================================================================+
   +===============+==========-==========*==========-==========+===============+
                                   CHANGE LOGS
                          DATA || CHANGE || SECTION || USER
    [1] (8/30/2021) Initial construction of script by A. Miller
   +===============+==========-==========*==========-==========+===============+
"""

#%%

""" Set up """

import pandas as pd

df = pd.DataFrame(columns=['line'], dtype='string')

#txt_file_path = "./text_versions/HEERF Quarterly Budget and Expenditure Reporting - V1_3_1.txt"
txt_file_path = "./text_versions/HEERF_Quarterly_Budget_and_Expenditure_Public_Posting_FINAL_accessible.txt"

#%%

""" find the line where 'Institution Name:' exists """
fp = open(txt_file_path, 'r', encoding='UTF-8')
lines = fp.readlines()
for item in lines: 
    if ("Institution Name:" in item):
        idx = lines.index(item)

#%%
def extractLines(txtfile):    
    #lines_to_read = range(163,232)
    fp = open(txtfile, 'r', encoding='UTF-8')
    lines = fp.readlines()
    for item in lines:
        if ((not (u"\u00A0" in item)) & (":" in item) & (not("http" in item))):
            idx = lines.index(item)
            #df_idx = idx - 163
            df.loc[idx,'line']=item
            df.loc[idx,'line2']=item.strip()
    #df.reset_index()
    fp.close()

df2 = pd.DataFrame(columns=['line'], dtype='string')

def extractLines2(txtfile):    
    #lines_to_read = range(163,232)
    fp = open(txtfile, 'r', encoding='UTF-8')
    lines = fp.readlines()
#    idx_list = []
    for item in lines:
        if ("Institution Name:" in item):
            start_idx = lines.index(item)
    for item in lines:
        if (lines.index(item) >= start_idx):
            idx = lines.index(item)
            df2.loc[idx,'line']=item
            df2.loc[idx,'line2']=item.strip()
    fp.close()

extractLines(txt_file_path)
extractLines2(txt_file_path)

df.index = pd.RangeIndex(len(df.index))
df2.index=pd.RangeIndex(len(df2.index))

#%%
for item in df['line2']:
    idx = list(df['line2']).index(item)
    splitList = item.split(':')
    ans = splitList[-1].strip()
    #question = splitList[0].strip()+":"+splitList[1].strip
    question = item.replace(ans,'')
    df.loc[idx,'question'] = question
    df.loc[idx,'answer'] = ans

#%%
import os
import glob
import pandas as pd

df = pd.DataFrame(columns=['line'], dtype='string')

# for filename in os.listdir(os.getcwd()):
#     with open(os.path.join(os.getcwd(), filename), 'r') as f: #open in readonly mode
#         print(filename)

root_dir = '.'
text_files_dir = os.path.join(root_dir, 'text_versions/text_versions')
#%%
# def get_start_idx(file_path):
#     fp = open(file_path, 'r', encoding='UTF-8')
#     lines = fp.readlines()
#     for item in lines:
#         if ("Institution Name:" in item):
#             idx = lines.index(item)
#             return idx

#%%
def extractLines(txtfile):    
    #lines_to_read = range(163,232)
    fp = open(txtfile, 'r', encoding='UTF-8')
    lines = fp.readlines()
    idx_list = []
    # for item in lines:
    #     if ("Institution Name:" in item):
    #         global start_idx
    #         start_idx = lines.index(item)
    for item in lines:
        if ((not (u"\u00A0" in item)) & (":" in item) & (not("http" in item))):
            idx = lines.index(item)
            df.loc[idx,'line']=item
            df.loc[idx,'line2']=item.strip()
    #df.reset_index()
    fp.close()

#%%
for folder in os.listdir(text_files_dir):
    #print(folder)
    if folder.startswith('.'):
        print("Skipping folder {}".format(folder))
        continue
    for file in os.listdir(os.path.join(text_files_dir,folder)):
        filename = "{}".format(file)
        file_path = os.path.join(os.path.join(text_files_dir,folder),filename)
        extractLines(file_path)
        df.index = pd.RangeIndex(len(df.index))
        for item in df['line2']:
            idx = list(df['line2']).index(item)
            df.loc[idx,'school'] = folder
            df.loc[idx,'file'] = file
            splitList = item.split(':')