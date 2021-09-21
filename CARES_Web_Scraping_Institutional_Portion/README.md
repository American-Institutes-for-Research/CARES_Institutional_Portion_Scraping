# CARES_Institutional_Portion_Scraping

## Anaconda Requirements

beautifulsoup4==4.9.3
certifi==2021.5.30
chardet==4.0.0
et-xmlfile==1.1.0
google==3.0.0
googlesearch-python==1.0.1
greenlet==1.1.1
idna==2.10
importlib-metadata==4.7.1
numpy==1.21.2
openpyxl==3.0.7
pandas==1.3.2
progressbar==2.5
python-dateutil==2.8.2
pytz==2021.1
requests==2.25.1
six==1.16.0
soupsieve==2.2.1
SQLAlchemy==1.4.23
tqdm==4.62.2
typing-extensions==3.10.0.0
urllib3==1.26.6
wget==3.2
zipp==3.5.0
beautifulsoup4==4.9.3
certifi==2021.5.30
chardet==4.0.0
et-xmlfile==1.1.0
google==3.0.0
googlesearch-python==1.0.1
greenlet==1.1.1
idna==2.10
importlib-metadata==4.7.1
numpy==1.21.2
openpyxl==3.0.7
pandas==1.3.2
progressbar==2.5
python-dateutil==2.8.2
pytz==2021.1
requests==2.25.1
six==1.16.0
soupsieve==2.2.1
SQLAlchemy==1.4.23
tika==1.24
tqdm==4.62.2
typing-extensions==3.10.0.0
urllib3==1.26.6
wget==3.2
zipp==3.5.0
beautifulsoup4==4.9.3
certifi==2021.5.30
chardet==4.0.0
et-xmlfile==1.1.0
google==3.0.0
googlesearch-python==1.0.1
greenlet==1.1.1
idna==2.10
importlib-metadata==4.7.1
numpy==1.21.2
openpyxl==3.0.7
pandas==1.3.2
progressbar==2.5
python-dateutil==2.8.2
pytz==2021.1
requests==2.25.1
six==1.16.0
soupsieve==2.2.1
SQLAlchemy==1.4.23
tika==1.24
tqdm==4.62.2
typing-extensions==3.10.0.0
urllib3==1.26.6
wget==3.2
zipp==3.5.0

## Required files:

`all 5000 statuses.csv` (provided by OCDO)
`IHE Student URLS January.xlsm` (provided by OCDO)


## Steps to run code:

 1. Install all packages in Anaconda using `pip install -r requirements.txt`
 2. Run the `web-scraper.py` script 
 3. Run the PDF to txt conversion script which converts PDF files to txt files using Apache Tika.
 4. Run the `pdf_txt_to_df.py` script which extracts information from the txt file to produce results in the form of a Dataframe.


