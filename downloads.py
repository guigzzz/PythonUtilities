from requests import get
from lxml import html
from multiprocessing.pool import Pool
from requests import get
from shutil import copyfileobj
from os.path import exists

SUFFIXES = ['html', '.com', '/']

class Downloader:
    """
    Mass/parallel downloading utility
    Constructor:
        - url: URL of page to scrape for file urls
        - blacklist: blacklist of url extensions
    """
    def __init__(self, url, blacklist = SUFFIXES):
        self.url = url
        self.blacklist = blacklist

    def __fetch_url(self):
        """
        Get page content from given url and searches the text for links
        This removes all links not starting with http and links with suffices present in the blacklist
        Returns a list of url strings
        """
        with get(self.url) as r:
            urls = html.fromstring(r.text).xpath("//a/@href")

        return [url for url in urls 
                if url.startswith('http') and not any(url.endswith(s) for s in self.blacklist) 
                    and not ':8' in url]

    def __select_urls(self, urls):
        """
        Ask the user for a selection of files to download given a list of urls
        """
        url_num = ""
        while not all(num.isnumeric() for num in url_num.split(' ')):
            url_num = input("> Input list of file numbers separated by spaces ")

        return [urls[int(num)] for num in url_num.split(' ')] 

    def download(self):
        """
        Main interface.
        Will fetch the links from the given page, filter them according to user preference,
        and finally download them in parallel
        """
        filtered = self.__fetch_url()
        if filtered:
            print('> Found following urls in page:')
            for i, url in enumerate(filtered): print('{} - {}'.format(i, url))
        else:
            print('> No URLs found in page')
            if(input("> Exit? [y/n]") == 'y'): exit()

        urls = []
        for url in self.__select_urls(filtered):
            local_filename = url.split('/')[-1]
            if exists(local_filename):
                if(input('> File {} already exists, download anyways? [y/n] '.format(local_filename)) == 'y'):
                    urls.append(url)
    
        with Pool() as p:
            p.map(self.__download_file, urls)

    def __download_file(self, url):
        """
        Worker function for the download threads
        """
        print('> Downloading: {}'.format(url))

        local_filename = url.split('/')[-1]
        
        with get(url, stream=True) as r:
            with open(local_filename, 'wb') as f:
                copyfileobj(r.raw, f)
        
        print('> Saved {} to: {}'.format(url, local_filename))
        return local_filename




if __name__ == '__main__':
    import sys
    url = sys.argv[1]

    d = Downloader(url)
    d.download()
