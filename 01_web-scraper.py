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
    [1] Adding comments throughout entire script || Abigail Miller
   +===============+==========-==========*==========-==========+===============+
"""
#%%

from bs4 import BeautifulSoup
import os
import requests
import sqlalchemy as db
from datetime import datetime
from tqdm import tqdm, trange
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
"""
This section is to establish the SQL engine and database that we will use to store the search results
We chose to use SQL to provide a table environment and to handle the potentially large volume of results 
"""

# Initialize the SQL engine
# SQL Alchemy
engine = db.create_engine('sqlite:///institutional_quarterly_report_metadata_6_to_8.sqlite')
connection = engine.connect()
metadata = db.MetaData()

# Initialize the SQL table defined with the columns listed below and their data type
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

# Create the table
metadata.create_all(engine)

#%%
""" This section imports and processes the school information
"""
# Extract general school website from URL file and add to data frame (df)
# Import list of schools
school_status_data = pd.read_csv('./all 5000 statuses.csv', usecols=['school_name'])  # , names=columnNames)
# Read in provided URLS
url_data = pd.read_excel('./IHE Student URLS January.xlsm')
# Create a dataframe with each school as a row and their corresponding URL
df = school_status_data.join(url_data)

# Extract primary component of URL
df['shortURL'] = df.URL.str.split("/", expand=True)[2]

# Remove preceding "www." if present
df['Site'] = [str(x).replace('www.', '') for x in df['shortURL']]

# Filter dataframe to only the columns listed below (name, state, ID, school webpage)
df_filtered = df.loc[:,['Applicant Name','Applicant State', 'OPE ID', 'Site']]

# Remove all special characters and punctuation from the names of the schools
df_filtered['Applicant Name'] = df_filtered['Applicant Name'].apply(lambda x: re.sub('[^a-zA-Z0-9 \n\.]','',x.strip()))

                                                                     
#%%
""" 
Here, we define a function that takes the search query as an input and performs a Google search.
Each result found from the query is saved in a list.
This list is returned by the function.
"""
# siteStr is the website you want to search
def google_search(query):
    # Initialize the list that will contains the results as an empty list
    results = []
    
    # Depending on the machine you are using or the version of packages you are using,
    # you may have better luck using either of the lines below:
    # Option 1: for j in search(query, tld="co.in", num=10, stop = None, pause = 45):
    # Option 2:
    for j in search(query = query, num = 10, start = 0, pause = 50):
        results.append(j)
    
    return results

n = 500  #chunk row size
df_filtered_splits = [df_filtered[i:i+n].reset_index(drop = True) for i in range(0,df_filtered.shape[0], n)]

#%%
""" This section completes the "heavy lifting" of the algorithm.
    Here, we are iterating through rows of the dataframe (df_filtered_splits)
"""
# This for loop iterates through applicants in the Applicant Name column 
# with a row index contained in range(start,end)
# In the example here, we are searching the entire column as the range goes from index 0 (first possible row)
# to the last record (length of the column)
for chunk_id in trange(6, 8):#len(df_filtered_splits)):
    for applicant_no in tqdm(range(92, len(df_filtered_splits[chunk_id]['Applicant Name'])), desc="Google Search status"):
    
        # This query is what we would type into the search bar on Google.com
        # This query pulls pdf files from the school website
        google_query = "\"Institutional Portion\" HEERF filetype:pdf site:" + df_filtered_splits[chunk_id]['Site'][applicant_no]
    
        # Perform the search by calling the function
        search_results = google_search(google_query)
    
        # Count the number of results for each search
        num_search_results = len(search_results)
    
        # Iterate through each of the found PDFs in the search results
        for pdf_url in search_results:
            # Assign metadata about the PDF to the table
            value_list = [{'OPE_ID': df_filtered_splits[chunk_id]['OPE ID'][applicant_no],
                           'Applicant_Name': df_filtered_splits[chunk_id]['Applicant Name'][applicant_no],
                           'Applicant_State': df_filtered_splits[chunk_id]['Applicant State'][applicant_no],
                           'Applicant_Domain': df_filtered_splits[chunk_id]['Site'][applicant_no],
                           'Query': google_query,
                           'Num_Search_Results': num_search_results,
                           'PDF_URL': pdf_url}]
            
            # Create a unique ID for each PDF found
            ID = sha256(json.dumps(value_list[0], default=str, sort_keys=True).encode()).hexdigest()
        
            # with the unique ID made for each PDF, check and see if the ID already shows up in the table
            #query = db.select([google_search_table]).filter(google_search_table.columns.ID == ID)
            query = connection.execute(db.select(google_search_table.columns.ID).filter(google_search_table.columns.ID == ID))
            result = len(query.scalars().all())
        
            # if the ID is already in the table, then we know the PDF has already been entered into the SQL database
            # result should either be zero (if the PDF needs to be added to the database)
            # or result could be one (if the PDF has already been added)
            if result == 1:
                print("Already in database")
                # continue to next PDF in search results
                continue
    
            # Make a folder in the Downloaded_PDFs folder with the Applicant Name (./Downloaded_PDFs/Applicant Name)
            os.makedirs(os.path.join(".", "Downloaded_PDFs", df_filtered_splits[chunk_id]['Applicant Name'][applicant_no]), exist_ok=True)
            
            # Import information from Python to SQL under the specific PDF ID
            value_list[0]['ID'] = ID
            query = db.insert(google_search_table)
            ResultProxy = connection.execute(query, value_list)
            
            # Select the PDF title from the URL string and
            # Remove special characters and punctionation from the PDF title
            pdf_title = re.sub('[^a-zA-Z0-9 \n\.]', '_', pdf_url.split('/')[-1])
            
            # Check if the title is already downloaded in the school folder
            if pdf_title in os.listdir(os.path.join(".", "Downloaded_PDFs", df_filtered_splits[chunk_id]['Applicant Name'][applicant_no])):
                # If yes, print message and move on to next file
                print("PDF already downloaded, Skipping : {}".format(pdf_title))
                
            # if no, download the PDF report and save in the file ./Downloaded_PDFs/Applicant Name
            try:
                print("Downloading PDF {}".format(pdf_title))
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
                }
                r = requests.get(pdf_url, headers=headers)
                with open(os.path.join(".", "Downloaded_PDFs", df_filtered_splits[chunk_id]['Applicant Name'][applicant_no], pdf_title), 'wb') as f:
                    f.write(r.content)
            # unless an error occurs, then print the message below and move onto the next file
            except:
                print("Error occured at school: {}, on pdf :{},  pdf_url :{}".format(df_filtered_splits[chunk_id]['Applicant Name'][applicant_no],
                                                                                                      pdf_title,
                                                                                                      pdf_url))
                continue
    
# If you would like to convert the completed SQL database back into a dataframe, 
# You may run the code below and view temp in the Variable Explorer.
#temp = pd.read_sql("SELECT * from google_search_tracking", con = engine)