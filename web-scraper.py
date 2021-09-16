"""
   +===================+========-========*========-========+===================+
   ||                               web-scraper.py                                ||
   ||                      by Karthik Jallawaram on (8/24/21)               ||
   ||                       American Institutes for Research                  ||
   ||                      CARES_Institutional_Portion_Scraping                                ||
   ||                                                                         ||
   || Description:                                                            ||
   ||                                                                         ||
   ||                                                                         ||
   ||                                                                         ||
   || Language:  Python 3.7.3                                                 ||
   || Graphics:  None                                                         ||
   || Downloads: None                                                         ||
   || Run time:  Approx. XX seconds                                           ||
   +===========================================================================+
   +===============+==========-==========*==========-==========+===============+
                                   CHANGE LOGS
                          DATA || CHANGE || SECTION || USER
    [1] 
   +===============+==========-==========*==========-==========+===============+
"""
#%%

from bs4 import BeautifulSoup
import os
import requests
import sqlalchemy as db
from datetime import datetime
from tqdm import tqdm
import pytz
import time
import json
from hashlib import sha256
import re
import wget
import requests
import csv
from bs4 import BeautifulSoup
from googlesearch import search
# from urllib.request import urlopen
# from urllib.parse import urljoin
import urllib.request
import urllib
import pathlib
from time import sleep
import pandas as pd
import progressbar
import os
import random
import requests
import re

#%%
# SQL Alchemy
engine = db.create_engine('sqlite:///institutional_quarterly_report_metadata.sqlite')
connection = engine.connect()
metadata = db.MetaData()

google_search_table = db.Table('google_search_tracking', metadata,
                        db.Column('ID', db.String(64), primary_key=True),
                        db.Column('OPE_ID', db.String(20)),
                        db.Column('Applicant_Name', db.String(250)),
                        db.Column('Applicant_State', db.String(5)),
                        db.Column('Applicant_Domain', db.String(250)),
                        db.Column('Query', db.String(100)),
                        db.Column('Num_Search_Results', db.Integer),
                        db.Column('PDF_URL', db.String(150))
                        )

metadata.create_all(engine)

#%%
# Import list of schools
school_status_data = pd.read_csv('./all 5000 statuses.csv', usecols=['school_name'])  # , names=columnNames)

# Extract general school website from URL file and add to data frame
# Read in provided URLS
url_data = pd.read_excel('./IHE Student URLS January.xlsm')
# raw_url = file['URL']
df = school_status_data.join(url_data)

# Extract primary component of URL
df['shortURL'] = df.URL.str.split("/", expand=True)[2]

# Remove preceding "www." if present
df['Site'] = [str(x).replace('www.', '') for x in df['shortURL']]

df_filtered = df.loc[:,['Applicant Name','Applicant State', 'OPE ID', 'Site']]


df_filtered['Applicant Name'] = df_filtered['Applicant Name'].apply(lambda x: re.sub('[^a-zA-Z0-9 \n\.]','',x))

                                                                     
#%%
def google_search(siteStr):
    results = []
    query = "\"Institutional Portion\" HEERF filetype:pdf site:" + siteStr
    df['Google Queried'] = 'Y'
    # for j in search(query, tld="co.in", num=10, stop = None, pause = 4):
    for j in search(query = query, num = 10, start = 0, pause = 10):
        results.append(j)

    return results

#%%
for applicant_no in tqdm(range(3000, len(df_filtered['Applicant Name'])), desc="Google Search status"):
    google_query = "\"Institutional Portion\" HEERF filetype:pdf site:" + df_filtered['Site'][applicant_no]

    search_results = google_search(df_filtered['Site'][applicant_no])
    num_search_results = len(search_results)
    for pdf_url in search_results:
        value_list = [{'OPE_ID': df_filtered['OPE ID'][applicant_no],
                       'Applicant_Name': df_filtered['Applicant Name'][applicant_no],
                       'Applicant_State': df_filtered['Applicant State'][applicant_no],
                       'Applicant_Domain': df_filtered['Site'][applicant_no],
                       'Query': google_query,
                       'Num_Search_Results': num_search_results,
                       'PDF_URL': pdf_url}]
    
        ID = sha256(json.dumps(value_list[0], default=str, sort_keys=True).encode()).hexdigest()
    
        #query = db.select([google_search_table]).filter(google_search_table.columns.ID == ID)
        query = connection.execute(db.select(google_search_table.columns.ID).filter(google_search_table.columns.ID == ID))
        result = len(query.scalars().all())
    
        if result == 1:
            print("Already in database")
            continue

        os.makedirs(os.path.join(".", "Downloaded_PDFs", df_filtered['Applicant Name'][applicant_no]), exist_ok=True)
        
        value_list[0]['ID'] = ID
        query = db.insert(google_search_table)
        ResultProxy = connection.execute(query, value_list)

        pdf_title = re.sub('[^a-zA-Z0-9 \n\.]', '_', pdf_url.split('/')[-1])
        
        
        if pdf_title in os.listdir(os.path.join(".", "Downloaded_PDFs", df_filtered['Applicant Name'][applicant_no])):
            print("PDF already downloaded, Skipping : {}".format(pdf_title))
            continue
    
        try:
            print("Downloading book {}".format(pdf_title))
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
            }
            r = requests.get(pdf_url, headers=headers)
            with open(os.path.join(".", "Downloaded_PDFs", df_filtered['Applicant Name'][applicant_no], pdf_title), 'wb') as f:
                f.write(r.content)
        except:
            print("Error occured at school: {}, on pdf :{},  pdf_url :{}".format(df_filtered['Applicant Name'][applicant_no],
                                                                                                  pdf_title,
                                                                                                  pdf_url))
            continue
    
#temp = pd.read_sql("SELECT * from google_search_tracking", con = engine)