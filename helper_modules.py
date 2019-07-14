import requests
import logging
import re
import sys, os
from gdrive_downloader import Gdrive
try:
    from bs4 import BeautifulSoup as Soup
    from clint.textui import progress
except ImportError:
    print('''
    install beautifulsoup4 before proceed
    pip install beautifulsoup4
    pip install clint
    ''')
    logging.error("beautiful soup not found")

class CrawlHelper():
    def __init__(self):
        # Create the Logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
    
        # Create the Handler for logging data to a file
        logger_handler = logging.FileHandler('python_logging.log')
        logger_handler.setLevel(logging.INFO)
    
        # Create a Formatter for formatting the log messages
        logger_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    
        # Add the Formatter to the Handler
        logger_handler.setFormatter(logger_formatter)
    
        # Add the Handler to the Logger
        self.logger.addHandler(logger_handler)
        self.logger.info('Completed configuring logger()!')

        #request headers
        self.headers = requests.utils.default_headers()
        self.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        })

    #module to crawl url and extract pdf
    def get_pdf_links(self, url):
        self.links = []
        try:
            r = requests.get(url, self.headers)                
            soup = Soup(r.text, 'html.parser')
            links = soup.find_all('a')
            for link in links:                     
                url = link.get('href', None)                
                if url is None:
                    pass
                elif url.endswith('.pdf'):                    
                    self.logger.info(url)
                    self.links.append(url)                        
                elif 'drive.google' in url:                        
                    self.logger.info(url)
                    self.links.append(url)                            
            return self.links
        except KeyboardInterrupt:
            print("press control-c again to quit")
            self.logger.error("exiting application")
        except Exception:
            self.logger.error("Exception occurred", exc_info=True)            


    def download_pdf(self, url):
        #check whether it is google drive link
        #extract id from url
        if 'drive.google' in url:
            m = re.search(r"([A-Za-z0-9-_]{25,35})", url)        
            if m is not None:
                id = m.group()
                #call gdrive_downloader to download link
                dest = str(id)+".pdf"
                gd = Gdrive()
                print("downloading :"+url)
                gd.download_file_from_google_drive(id, dest)
        #if it is direct link
        else:
            try:                
                self.direct_download(url)
            except:
                print(url+" is not available! unable to download")
                self.logger.error("link not available", exc_info=True)

    #util to download with progress bar
    def direct_download(self, link):
        fname = link.split('/')[-1]
        r = requests.get(link, stream=True)
        print("Downloading :"+fname)
        with open(fname, "wb") as Pypdf:
            total_length = int(r.headers.get('content-length'))
            for ch in progress.bar(r.iter_content(chunk_size = 2391975), expected_size=(total_length/1024) + 1):
                if ch:
                    Pypdf.write(ch)
