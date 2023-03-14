""" To work with html pages """
from bs4 import BeautifulSoup


class MyBeautifulSoup():
    """ Crawler for shodan """
    all_results = []
    total_results = False
    results = False
    pagination = False
    next_page_num = False


    def __init__(self, html_doc):
        """ Auto crawler for any page """
        self.soup = BeautifulSoup(html_doc, 'html.parser')

    async def page_results(self):
        """ Gets the number of results """
        try:
            total_results = self.soup.find('h4').get_text()
            self.total_results = {'total_results': f'Total Results: {total_results}'}
            self.results = self.soup.find_all('div', class_="result")
        except AttributeError:
            pass

    async def general_information(self):
        """ Crawler for main page """
        for result in self.results:
            hostname = result.find_all('li', class_="hostnames text-secondary")
            hostname = [i.get_text() for i in hostname ]
            country = result.find_all('a', class_="filter-link text-dark")
            country = ', '.join([i.get_text() for i in country])
            detail = result.find('a', class_="title text-dark")
            status = result.find_all('div', class_="columns")[-1].find('pre')
            components = result.find('li', class_="components")
            if components is not None:
                components = components.find_all('a')
                components = [i['aria-label'] for i in components]
            else:
                components = ''
            hostname = {
                'title': detail.get_text(),
                'detail': detail.get('href'),
                'hostname': hostname,
                'location': country,
                'status': status.get_text().replace('\n', '')[0:15],
                'components': components
                }
            self.all_results.append(hostname)

    async def only_hosts(self):
        """ Crawler urls for detail info """
        for result in self.results:
            detail_url = result.find('a', class_="title text-dark").get('href')
            self.all_results.append(detail_url)

    async def detail_info(self, hostname):
        """ Crawler info for each host """
        gen_information = self.soup.find(
            'div', class_="card card-yellow card-padding").find_all('td')
        gen_information = [i.get_text().strip() for i in gen_information]
        gen_information_key = gen_information[::2]
        gen_information_val = gen_information[1::2]
        gen_information = dict(zip(gen_information_key, gen_information_val))

        try:
            web_techn = self.soup.find('ul', id="http-components").find_all('a')
            web_techn = [i.get_text().strip() for i in web_techn]
        except AttributeError:
            web_techn = 'None'

        try:
            ports_num = self.soup.find_all('div', class_="six columns")[1].find_all('h6')
            ports_info = self.soup.find_all('div', class_="six columns")[1].find_all(
                'div', class_="card card-padding banner")
            ports_num = [i.get_text().strip() for i in ports_num]
            ports_info = [i.get_text().strip() for i in ports_info]
            ports = dict(zip(ports_num, ports_info))
        except AttributeError:
            ports = 'None'

        try:
            vulners = self.soup.find(id="vulnerabilities")
            vulners_num = [i.get_text().strip() for i in vulners.find_all('th')]
            vulners_info = [i.get_text().strip() for i in vulners.find_all('td')]
            vulners = dict(zip(vulners_num, vulners_info))
        except AttributeError:
            vulners = 'None'

        host_info = {
            'hostname': hostname,
            'General Information': gen_information,
            'ports': ports,
            'components': web_techn,
            'vuln': vulners,
        }
        return host_info

    async def pagination_url(self):
        """ Return next url if there """
        try:
            next_page = self.soup.find('div', class_="pagination").find_all('a')
            if len(next_page) == 1:
                self.pagination = next_page[0].get('href')
            else:
                self.pagination = next_page[1].get('href')
            self.next_page_num = int(self.pagination.split('page=')[-1])
        except AttributeError:
            pass
