from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import webdriver_conf
import argparse
import colorama
import csv
import os


class Connection:

    def __init__(self, browser_driver, search_query):
        self.browser_driver = browser_driver
        for query in search_query:
            self.query = query

    def conn(self):
        url = 'https://youtube.com/results?search_query='
        Get_Links(self.browser_driver, url + '+'.join(self.query.split())).scrape()


class Get_Links:

    def __init__(self, driver, link):
        self.driver = driver
        self.link = link

    def dl_videos(self, video_links):
        folder_name = 'videos'
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        
        for dl_link in video_links:
            if dl_link == None:
                pass
            else:
                os.system(f'youtube-dl {dl_link}')

    def scrape(self):
        self.driver.get(self.link)
        try:
            with open('search_results.csv', 'w', encoding='utf-8') as f:
                headers = ['Title', 'URL/Link']
                writer = csv.writer(f, dialect='excel')
                writer.writerow(headers)

                container = WebDriverWait(self.driver, 0).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="contents"]/ytd-item-section-renderer'))
                )

                titles, links = [], []
                for link in container.find_elements_by_xpath('//*[@id="video-title"]'):
                    writer.writerows([[link.text, link.get_attribute('href')]])
                    titles.append(link.text)
                    links.append(link.get_attribute('href'))
                    print(colorama.Fore.YELLOW,f'[!] {link.text}',
                            colorama.Style.RESET_ALL, link.get_attribute('href'))

                print(colorama.Fore.GREEN,
                        f'[*] {len(titles)} results.', colorama.Style.RESET_ALL)
                
                auth = input('Do you want to download these videos?[y/n] ')
                if auth.casefold() == 'y' or auth.casefold() == 'yes':
                    Get_Links(self.driver, self.link).dl_videos(links)
                else:
                    print('Abort!')
        except WebDriverException as err:
            print(colorama.Fore.RED,
              '[!!] WebDriver Failed To Function!', err, colorama.Style.RESET_ALL)
            Get_Links(self.driver, self.link).scrape()
        finally:
            self.driver.quit()


if __name__ == '__main__':
    colorama.init()
    parser = argparse.ArgumentParser(description='Scrapes links of top related videos.')

    parser.add_argument('-s', '--search',
                        nargs=1, metavar='SEARCH',
                        action='store',
                        help='Searches for top related videos based on input.')

    args = parser.parse_args()
    if args.search:
        try:
            options = webdriver_conf.get_driver_options('Chrome')
            webdriver_conf.get_all_options('Chrome', options)
            browser = webdriver_conf.get_driver('Chrome', options)

            Connection(browser, [x for x in args.search]).conn()
        except WebDriverException as err:
            print(colorama.Fore.RED,
                f'No WebDriver Found For Chrome!', err, colorama.Style.RESET_ALL)
