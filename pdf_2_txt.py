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
    [1] Commentary on entire script || A Miller
   +===============+==========-==========*==========-==========+===============+
"""

from tika import parser
import os
import re
from urllib.request import url2pathname

# Set the root directory (the file that you are currently working out of)
root_dir = '.'
# Set the path for the folder where the downloaded PDFs are 
downloaded_files_dir = os.path.join(root_dir, 'Downloaded_PDFs')
# Set the path for the folder where the text files will be saved
target_dir = os.path.join(root_dir, 'text_versions')

#%%

# Iterate through each Institution Folder in the Dowloaded_PDfs folder
for folder in os.listdir(downloaded_files_dir):
    
    # Skip over folders that start with a period.
    # These are more common on MACs. Unlikely to see folders like this with Windows
    if folder.startswith('.'):
        print("Skipping folder {}".format(folder))
        continue
    
    # Create a folder in the text file folder of the institution name.
    # Punctuation and special characters are removed from the name.
    # Folders should match in the Downloaded_PDFs folder and text_versions folder
    os.makedirs(os.path.join(target_dir, re.sub('[^a-zA-Z0-9 \n\.]', '_', folder)), exist_ok=True)
    
    # Iterate through each File in the Institution Folder
    for file in os.listdir(os.path.join(downloaded_files_dir, folder)):
        
        # Check if file is a working file saved by MS Word
        # This shouldn't occur, but if it does, this is the check to skip over the file
        if file.startswith('~'):
            print("Skipping file {}".format(file))
            continue
        
        else:
            # Run the pdf file through the text parser
            file_data = parser.from_file(os.path.join(downloaded_files_dir, folder, file))
            # Get files text content
            text = file_data['content']
            # Remove all white spaces on the ends of the text
            cleaned_text = str(text).strip()
    
            # Save converted files to the folder of the institution
            with open(os.path.join(target_dir, re.sub('[^a-zA-Z0-9 \n\.]', '_', folder), "{}.txt".format(re.sub('[^a-zA-Z0-9 \n\.]', '_', file.split('.')[0]))), "w") as text_file:
                ext_file.write(cleaned_text)

            