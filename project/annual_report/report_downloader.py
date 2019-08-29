import os
import time
import requests
from bs4 import BeautifulSoup
from configparser import ConfigParser, ExtendedInterpolation
import logging
from logging.config import fileConfig

config = ConfigParser(interpolation=ExtendedInterpolation())
config.read('../config.ini')
OUTPUT_DIR_PATH = config['AUTOMATION']['OUTPUT_DIR_PATH']
BASE_URL =  config['AUTOMATION']['BASE_URL']

fileConfig('logging_config.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class AnnualReportDownloader:

    def __init__(self, company):
        self.base_url = BASE_URL
        self.urls = []
        self.company = company

    def get_annual_report_urls(self):
        """ collect all of the urls for the numerous pdf annual reports
        of a specified company

        :param company: company name, used to search for annual reports
        :return urls: list of urls for the annual report pdfs for the company
        """

        # find all links to annual reports on the webpage
        company_url = r'{}/Company/{}'.format(self.base_url, self.company)
        r = requests.get(company_url)
        b = BeautifulSoup(r.text, 'lxml')
        annual_reports = b.find_all('ul', attrs={'class':'links'})

        for report in annual_reports:
            try:
                # create the report_url to download the pdf
                report_name = report.find('a')['href']
                report_url = ''.join([self.base_url, report_name])
                self.urls.append(report_url)
            except (TypeError, KeyError):
                # ignore expected errors for links on the page that are not for pdfs
                continue

    def download_annual_reports(self):
        """ Download all of the annual reports in self.urls """

        output_paths = self.create_output_paths()

        for url in self.urls:
            # get directory to store annual report
            filepath = output_paths[url]
            filename = filepath.split('\\')[-1]

            # skip files that have already been downloaded
            if filename in os.listdir(OUTPUT_DIR_PATH):
                logger.info('file already downloaded: {}'.format(url))
                continue

            # download pdf
            r = requests.get(url)
            logger.info('downloaded: {}'.format(url))

            # write pdf to local directory
            # 'wb' stands for write binary
            with open(filepath, 'wb') as f:
                f.write(r.content)

            # required delay, stated in the robots.txt
            time.sleep(5)  # five seconds

    def create_output_paths(self):
        """ create a mapping a file paths for the report_names and
        directory paths to store each annual report locally

        NOTE:annual_report/raw_data/[company_name]

        :return output_paths: dict with mapping - {'report name': 'directory_path'}
        """

        output_paths = {}
        for ind, url in enumerate(self.urls):
            # parse the year from the annual report report_name
            year = url.split('_')[-1].split('.')[0]

            # The first annual report on a page is stored in different html
            # and does not have the year in the report name
            # e.g. ('Click/[#]') instead of ('NYSE_ORCL_2015.pdf')
            # add a condition to identify the url with index 0 and
            # add one to the year of the next annual report (2nd most recent year)
            # you will need to convert a string to an int for the addition
            if ind == 0:
                previous_year = self.urls[1].split('_')[-1].split('.')[0]
                year = str(int(previous_year) + 1)

            # create a file path to identify how to name a file
            # and where to store it locally
            filename = '{}_annual_report_{}.pdf'.format(self.company, year)
            filepath = os.path.join(OUTPUT_DIR_PATH, filename)
            output_paths[url] = filepath

        return output_paths
