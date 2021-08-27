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

root_dir = '.'
draft_dir = os.path.join(root_dir, 'test_files')

draft_files = [file for file in os.listdir(draft_dir) if not file.startswith('~')]

for draft_file in draft_files:
    # Parse data from file
    file_data = parser.from_file(os.path.join(draft_dir, draft_file))
    # Get files text content
    text = file_data['content']
    cleaned_text = str(text).strip()
    
    # Save converted files
    with open(os.path.join(root_dir, 'text_versions', "{}.txt".format(draft_file.split('.')[0])), "w") as text_file:
        text_file.write(cleaned_text)