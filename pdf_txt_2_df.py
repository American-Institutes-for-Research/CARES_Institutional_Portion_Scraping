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

""" Set up """

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
