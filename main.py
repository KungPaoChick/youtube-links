from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import youtube_dl as yd
import webdriver_conf
import argparse
import colorama
import json
import os


class Connection:

    def __init__(self, browser_driver, search_query):
        self.browser_driver = browser_driver
        for query in search_query:
            self.query = query

    def conn(self):
        url = 'https://youtube.com/results?search_query='
        Get_Links(self.browser_driver, url + '+'.join(self.query.split())).scrape(self.query)


class Get_Links:

    def __init__(self, driver, link):
        self.driver = driver
        self.link = link

    def scrape(self, search_query):
        self.driver.get(self.link)
        try:
            with open('search_results.json', 'w', encoding='utf-8') as f:
                container = WebDriverWait(self.driver, 0).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="contents"]/ytd-item-section-renderer'))
                )

                results = {}
                results['contents'] = [{}]
                titles, links = [], []
                for link in container.find_elements_by_xpath('//*[@id="video-title"]'):
                    if link.get_attribute('href') == None:
                        pass
                    else:
                        titles.append(link.text)
                        links.append(link.get_attribute('href'))
                        print(colorama.Fore.YELLOW,f'[!] {link.text}',
                                colorama.Style.RESET_ALL, f"- {link.get_attribute('href')}")

                        for element in results['contents']:
                            element[link.text] = link.get_attribute('href')

                results['info'] = {'results': len(titles)}
                json.dump(results, f, indent=2)
                print(colorama.Fore.GREEN,
                        f'[*] {len(titles)} results.', colorama.Style.RESET_ALL)

        except WebDriverException as err:
            print(colorama.Fore.RED,
              '[!!] WebDriver Failed To Function!', err, colorama.Style.RESET_ALL)
            Get_Links(self.driver, self.link).scrape(search_query)
        finally:
            self.driver.quit()


def dl_videos():
    folder_name = 'videos'
    origin = os.getcwd()
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    with open('search_results.json', 'r', encoding='utf-8') as j_source:
        source = json.load(j_source)

    ydl_opts = {}
    for dict in source['contents']:
        if args.download:
            os.chdir(os.path.join(origin, folder_name))
            for video_title in args.download:
                if not video_title in dict:
                    print(colorama.Fore.RED,
                            f'[!!] {video_title} does not exist',
                            colorama.Style.RESET_ALL)
                else:
                    with yd.YoutubeDL(ydl_opts) as get:
                        if not get.download([dict[video_title]]) == 0:
                            print(colorama.Fore.RED,
                                    f'[!!] {video_title} failed to download',
                                    colorama.Style.RESET_ALL)
                        else:
                            print(colorama.Fore.GREEN,
                                    f'[*] {video_title} has been downloaded',
                                    colorama.Style.RESET_ALL)
            os.chdir(origin)

        if args.downloadall:
            os.chdir(os.path.join(origin, folder_name))
            for title in dict:
                with yd.YoutubeDL(ydl_opts) as get:
                    if not get.download([dict[title]]) == 0:
                        print(colorama.Fore.RED, f'[!!] {title} failed to download',
                                colorama.Style.RESET_ALL)
                    else:
                        print(colorama.Fore.GREEN, f'[*] {title} has been downloaded',
                                colorama.Style.RESET_ALL)
            os.chdir(origin)


if __name__ == '__main__':
    colorama.init()
    parser = argparse.ArgumentParser(description='Scrapes links of top related videos.')

    parser.add_argument('-s', '--search',
                        nargs=1, metavar='SEARCH',
                        action='store',
                        help='Searches for top related videos based on input.')

    parser.add_argument('-d', '--download',
                        nargs='+', metavar='DOWNLOAD',
                        action='store',
                        help='Downloads the video/s from search_results.json.')

    parser.add_argument('-da', '--downloadall',
                        action='store_true',
                        help='Downloads all videos from search_results.json')

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

    if args.download:
        dl_videos()

    if args.downloadall:
        dl_videos()
