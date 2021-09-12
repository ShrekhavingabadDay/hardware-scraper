# TODO: switch to using url_constructor class for setting the params for a bot

import requests
import os
from bs4 import BeautifulSoup
from library import url_constructor

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

scraper_config_object = {
    "name":None,
    "stext":None,
    "min_price":None,
    "max_price":None
}

sorting_keywords = {
    "uj":1,
    "ar_nov":2,
    "ar_csokk":3
}

class HardverApro:

    def __init__(self, url, modosit_url, data_dir, link_dir, config_object ):
        self.url = url
        self.modosit_url = modosit_url
        self.req_session = requests.Session()
        self.data_dir = data_dir
        self.link_dir = link_dir
        self.soup = None
        self.result_count = None
        self.ad_list = None
        self.url_constructor = url_constructor.url_constructor(url)
        self.modosit_url_constructor = url_constructor.url_constructor(modosit_url)
        self.config_object = config_object

        if not config_object["name"]:
            raise AttributeError("Please initialize the bot with a valid name!")

        if config_object:
            self.set_url_params()
        else:
            raise AttributeError("Invalid config object for scraper!")

    def modify_config_object(self, param_to_modify):
        for key in param_to_modify:
            try:
                self.config_object[key] = param_to_modify[key]
            except KeyError:
                return("Invalid configuration for " + self.config_object["name"])
        return "Configuration for " + self.config_object["name"] + " successful!"
    

    def jegelve(self, ad):
        if ad.find('p', {'class':'mt-1'}):
            return True
        return False
    
    def write_ids_to_file(self, array):
        try:
            with open(os.path.join(self.data_dir, self.config_object["stext"]), 'a') as f:
                f.writelines([item + '\n' for item in array])
        except FileNotFoundError:
            raise FileNotFoundError("Please make sure to run configure.sh before running the program!")

    def write_links_to_file(self, array):
        try:
            with open(os.path.join(self.link_dir, self.config_object["stext"]), 'a') as f:
                f.writelines([item + '\n' for item in array])
        except FileNotFoundError:
            raise FileNotFoundError("Please make sure to run configure.sh before running the program!")

    def get_ids_from_file(self):
        try:
            with open(os.path.join(self.data_dir, self.config_object["stext"]), 'r') as file:
                ad_ids = [line.strip() for line in file.readlines()]

            return ad_ids
        except FileNotFoundError:
            return []

    def set_url_params(self):
        
        try:
            self.url = self.url_constructor.set_param({"stext":self.config_object["stext"],
                                                   "minprice":self.config_object["min_price"],
                                                   "maxprice":self.config_object["max_price"]
                                                  })
        except KeyError:
            print("Incorrect config object...")

    def construate_modosit_url(self):

        self.modosit_url = self.modosit_url_constructor.set_param({"url":self.url})

    def set_search_term(self, search_term):
        self.config_object["stext"] = search_term
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

        try:
            full_text = self.ad_list.find('li',{'class':None}).text
        except AttributeError:
            return True

        self.result_count = [int(s) for s in full_text.split() if s.isdigit()][0]
        return False

    def set_url_offset(self, offset):
        for i in range(len(self.url)-1, 0, -1):
            if self.url[i] == "=":
                param_index = i+1
                break
        self.url = self.url[:param_index] + str(offset)

    def reset_db(self):
        try:
            with open(os.path.join(self.link_dir, self.config_object["stext"]), 'r+') as link_f:
                link_f.truncate(0)
            with open(os.path.join(self.data_dir, self.config_object["stext"]), 'r+') as id_f:
                id_f.truncate(0)
        except FileNotFoundError:
            raise FileNotFoundError("Please make sure to run configure.sh before running the program!")
        self.scrape_all_links()

    def scrape_all_links(self):

        if self.get_result_count():
            return None

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

            new_uids = [uad['data-uadid'] for uad in self.ad_list.find_all("li", {"class":"media"}) if uad['data-uadid'] not in ad_ids]

            all_uids += new_uids
            ad_ids += new_uids

            self.ad_list = None

            self.set_url_offset(current_offset)

            self.reload()

            current_offset += 50

        self.write_ids_to_file( all_uids )
        self.write_links_to_file( all_links )

        if len(all_links) == 0:
            return None

        return  (self.config_object["name"] + '\n'.join(all_links))

hardverapro_scraper = HardverApro
