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
    lines_to_read = range(163,232)
    fp = open(txtfile, 'r', encoding='UTF-8')
    lines = fp.readlines()

    for item in lines:
        idx = lines.index(item)
        df_idx = idx - 163
        if idx in lines_to_read:
            df.loc[df_idx,'line']=item
            df.loc[df_idx,'trim']=item.strip()
    fp.close()

for item in df['trim']:
    idx = list(df['trim']).index(item)
    splitList = item.split(':')
    question = splitList[0].strip()
    ans = splitList[1].strip()
   # df['split'] = splitList
    df.loc[idx,'question'] = question
    df.loc[idx,'answer'] = ans
        