"""
   +===================+========-========*========-========+===================+
   ||                               pdf_2_txt.py$                             ||
   ||                      by Karthik Jallawaram on (12/6/2020)               ||
   ||                       American Institutes for Research                  ||
   ||                          CARES_Web_Scraping                             ||
   ||                                                                         ||
   || Description:                                                            ||
   ||                                                                         ||
   ||                                                                         ||
   ||                                                                         ||
   || Language:  Python 3.7.6                                                 ||
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

from tika import parser
import os
import re
from urllib.request import url2pathname
root_dir = '.'
downloaded_files_dir = os.path.join(root_dir, 'Downloaded_PDFs')
target_dir = os.path.join(root_dir, 'text_versions')

for folder in os.listdir(downloaded_files_dir):
    if folder.startswith('.'):
        print("Skipping folder {}".format(folder))
        continue
    os.makedirs(os.path.join(target_dir, re.sub('[^a-zA-Z0-9 \n\.]', '', folder)), exist_ok=True)
    for file in os.listdir(os.path.join(downloaded_files_dir, folder)):
        if file.startswith('~'):
            print("Skipping file {}".format(file))
            continue
        else:
            file_data = parser.from_file(os.path.join(downloaded_files_dir, folder, file))
            # Get files text content
            text = file_data['content']
            cleaned_text = str(text).strip()
    
            # Save converted files
            with open(os.path.join(target_dir, re.sub('[^a-zA-Z0-9 \n\.]', '', folder), "{}.txt".format(re.sub('[^a-zA-Z0-9 \n\.]', '', file.split('.')[0]))), "w") as text_file:
                text_file.write(cleaned_text)

            