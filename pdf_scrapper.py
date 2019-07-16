from helper_modules import CrawlHelper
from time import time as timer
import argparse


if __name__ == '__main__':  

    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="url that needs to be searched for pdf files")
    args = parser.parse_args()
    url = args.url
    
    try:
        cw = CrawlHelper()  
        links = cw.get_pdf_links(url)        
        print("Total download links found "+ str(len(links)))
        #start = timer()
        for link in links:
            if link is not None:
                cw.download_pdf(link)
        #print(f"Elapsed Time: {timer() - start}")    
            
    except KeyboardInterrupt:
        print("application stopped")
    except Exception:
        cw.logger.error("Exception occurred", exc_info=True)  
        print("Exception occured")
        
