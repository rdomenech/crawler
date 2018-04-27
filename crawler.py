import json
import random
import re
import requests
from urllib.parse import urljoin, urlparse


class EmptyKeywords(Exception):
    def __init___(self):
        Exception.__init__(self, "Keywords must be provided!")


class NoQueryTypeProvided(Exception):
    def __init___(self):
        Exception.__init__(self, "Query type must be provided")


class Crawler():

    class CrawlerType():

        REPOSITORIES = 'Repositories'
        ISSUES = 'Issues'
        WIKIS = 'Wikis'
        TYPES = ['Repositories', 'Issues', 'Wikis']

    BASE_URL = 'https://github.com/'

    def __init__(self):
        """
        Crawler constructor.
        """

        self.keywords = []
        self.proxies = []
        self.type = ''

    def query(self, query_params):
        """
        Main crawler method of Github. It validates the json sent and its
        params, makes the main request to github and parses the response.

        Ex.:
        cr = Crawler()
        cr.query('{
            "keywords": ["openstack", "nova", "css"],
            "proxies": ["194.126.37.94:8080","13.78.125.167:8080"],
            "type": "Repositories"}')

        Response ex.:
        '[{
            "url": "https://github.com/atuldjadhav/DropBox-Cloud-Storage",
            "extra": {
                "owner": "atuldjadhav",
                "language_stats": {
                    "CSS": 52.0,
                    "JavaScript": 47.2,
                    "HTML": 0.8}}}]'

        :param query_params: json with the query params.
        :return: json with the response.
        """

        self._validate_params(query_params)
        response = requests.get(self._get_query_url(),
                                proxies=self._get_proxies())
        return self._parse_response(response)

    def _validate_params(self, query):
        """
        It validates the received params from the json and store it in the
        Crawler object or raises and exception.
        :param query: json query received.
        """

        query_data = json.loads(query)
        if 'keywords' not in query_data:
            raise KeyError
        elif not isinstance(query_data.get('keywords'), list):
            raise TypeError
        elif len(query_data.get('keywords')) == 0:
            raise EmptyKeywords

        self.keywords = [keyword for keyword in query_data.get('keywords')]

        if 'proxies' not in query_data:
            raise KeyError
        elif not isinstance(query_data.get('proxies'), list):
            raise TypeError

        self.proxies = [proxy for proxy in query_data.get('proxies')]

        if 'type' not in query_data:
            raise KeyError
        elif not isinstance(query_data.get('type'), str):
            raise TypeError
        elif query_data.get('type') not in Crawler.CrawlerType.TYPES:
            raise NoQueryTypeProvided

        self.type = query_data.get('type')

    def _get_query_url(self):
        """
        It builds the query url.
        :return: the query url.
        """

        query_type = ''
        if self.type != Crawler.CrawlerType.REPOSITORIES:
            query_type = self.type

        return '{}search?q={}&type={}'.format(
            Crawler.BASE_URL, '+'.join(self.keywords), query_type)

    def _get_proxies(self):
        """
        It builds a proxis dictionary for the request by choosing one of the
        proxies received randomly.
        :return: proxies dictionary.
        """
        return dict(http=random.choice(self.proxies))

    def _parse_response(self, response):
        """
        It parses the response from the github query and builds the json
        response.
        :param response: response from github query.
        :return: json response.
        """

        regex = '<a.*data-hydro-click.*\\s+(?:[^>]*?\\s+)?href=([\"\'])(.*?)' \
                '\\1'
        links = re.findall(regex, response.text)

        repo_links = []
        for link in links:
            url = urljoin(Crawler.BASE_URL, link[1])

            repo_data = dict(url=url)

            if self.type == Crawler.CrawlerType.REPOSITORIES:
                repo_data['extra'] = self._get_extra_data(url)

            repo_links.append(repo_data)

        return json.dumps(repo_links)

    def _get_extra_data(self, url):
        """
        It gets the extra data for a repos query and builds the dictionary
        with it for the response.
        :param url: url of the repo.
        :return: extra data dictionary.
        """
        owner = urlparse(url).path.split('/')[1]
        response = requests.get(url, proxies=self._get_proxies())

        regex = '<span class=\"language-color\" aria-label=\"(.*?)\"'
        languages = re.findall(regex, response.text)

        language_stats = dict()
        for el in languages:
            name, percentage = el.replace('%', '').split()
            language_stats[name] = self._convert_to_number(percentage)

        return dict(owner=owner, language_stats=language_stats)

    def _convert_to_number(self, number):
        """
        It converts the string language percentage to integer or float.
        :param number: string language percentage.
        :return: an integer or float.
        """

        try:
            return int(number)
        except ValueError:
            return round(float(number), 2)
