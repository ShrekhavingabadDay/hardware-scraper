import requests
import os
from bs4 import BeautifulSoup

sorting_payloads = [
    {
        "order":"time",
        "dir":"d"
    },
    {
        "order":"price",
        "dir":"a"
    },
    {
        "order":"price",
        "dir":"d"
    }
]

sorting_keywords = {
    "uj":1,
    "ar_nov":2,
    "ar_csokk":3
}

class HardverApro:

    def __init__(self, url, modosit_url, data_dir, link_dir, stext=None ):
        self.url = url
        self.modosit_url = modosit_url
        self.req_session = requests.Session()
        self.data_dir = data_dir
        self.link_dir = link_dir
        self.soup = None
        self.result_count = None
        self.ad_list = None

        if stext:
            self.set_search_term(stext)

    def jegelve(self, ad):
        if ad.find('p', {'class':'mt-1'}):
            return True
        return False
    
    def write_ids_to_file(self, array):
        try:
            with open(os.path.join(self.data_dir, self.stext), 'a') as f:
                f.writelines([item + '\n' for item in array])
        except FileNotFoundError:
            raise FileNotFoundError("Please make sure to run configure.sh before running the program!")

    def write_links_to_file(self, array):
        try:
            with open(os.path.join(self.link_dir, self.stext), 'a') as f:
                f.writelines([item + '\n' for item in array])
        except FileNotFoundError:
            raise FileNotFoundError("Please make sure to run configure.sh before running the program!")

    def get_ids_from_file(self):
        try:
            with open(os.path.join(self.data_dir, self.stext), 'r') as file:
                ad_ids = [line.strip() for line in file.readlines()]

            return ad_ids
        except FileNotFoundError:
            return []

    def set_url_search_term(self):
        self.url = self.url[:45] + self.stext + self.url[45:]

    def construate_modosit_url(self):
        self.modosit_url = self.modosit_url + self.url

    def set_search_term(self, search_term):
        self.stext = search_term
        self.set_url_search_term()
        self.construate_modosit_url()

    def reload(self):
        r = self.req_session.get(self.url)
        self.soup = BeautifulSoup(r.text, 'html.parser')

    def init_session(self, sorting_keyword):
        # initializing the session for obtaining the cookies
        self.req_session.get(self.url)

        # this request modifies the page on the server side given as response to match the required sorting
        self.req_session.post(self.modosit_url, sorting_payloads[sorting_keywords[sorting_keyword]])

        self.reload()
    def get_result_count(self):

        # this is where all the ads are found (and also the result count)
        self.ad_list = self.soup.find('div',{'class':'uad-list'}).find('ul',{'class':'list-unstyled'})

        full_text = self.ad_list.find('li',{'class':None}).text

        self.result_count = [int(s) for s in full_text.split() if s.isdigit()][0]

    def scrape_all_links(self):

        self.get_result_count()
        repeat_count = (self.result_count // 50) + 1
        current_offset = 50
        all_links = []
        all_uids = []
        ad_ids = self.get_ids_from_file()

        for i in range(repeat_count):

            if not self.ad_list:
                self.ad_list = self.soup.find('div',{'class':'uad-list'}).find('ul',{'class':'list-unstyled'})

            links = [one_ad.find('a')["href"] for one_ad in self.ad_list.find_all("li", {"class", "media"}) if (one_ad["data-uadid"] not in ad_ids)]

            all_links += links

            all_uids += [uad['data-uadid'] for uad in self.ad_list.find_all("li", {"class":"media"})]

            self.ad_list = None

            self.url = self.url + "&offset=" + str(current_offset)

            self.reload()

            current_offset += 50

        self.write_ids_to_file( all_uids )
        self.write_links_to_file( all_links )

        return all_links

hardverapro_scraper = HardverApro
