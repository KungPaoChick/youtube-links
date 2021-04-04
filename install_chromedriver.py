import requests
import wget
import zipfile
import os
import sys
import platform
import colorama


class Identify_sys:

    def system(self):
        op_systems = {'Linux': f'chromedriver_linux{Identify_sys().system_bit()}',
                      'Darwin': f'chromedriver_mac{Identify_sys().system_bit()}',
                      'Windows': f'chromedriver_win{Identify_sys().system_bit()}'}
        if platform.system() in op_systems:
            return op_systems[platform.system()]
        else:
            print(colorama.Fore.RED,
                    '[!!] Not Supported.', colorama.Style.RESET_ALL)

    def system_bit(self):
        return 64 if sys.maxsize > 2**32 else 32


class Get_chromedriver:

    def __init__(self, zip_name):
        self.zip_name = zip_name

    def latest_version(self):
        try:
            with requests.get('https://chromedriver.storage.googleapis.com/LATEST_RELEASE') as response:
                response.raise_for_status()

            return Get_chromedriver(self.zip_name).install(response.text)
        except requests.HTTPError as err:
            print(colorama.Fore.RED,
                    f'Something went wrong! {err}', colorama.Style.RESET_ALL)

    def install(self, version):
        download_url = f'https://chromedriver.storage.googleapis.com/{version}/{self.zip_name}.zip'
        driver_zip = wget.download(download_url, 'chromedriver.zip')
        with zipfile.ZipFile(driver_zip) as zip_ref:
            zip_ref.extractall()
        
        os.remove(driver_zip)
        if not 'chromedriver' in [content.split()[0] for content in os.listdir()]:
            print(colorama.Fore.RED,
                    '\n[!!] chromedriver failed to install.',
                    colorama.Style.RESET_ALL)
        else:
            if platform.system() == 'Linux':
                os.system('chmod 755 chromedriver')
            print(colorama.Fore.GREEN,
                    f'\n[*] chromedriver v{version} successfully installed.',
                    colorama.Style.RESET_ALL)


if __name__ == '__main__':
    colorama.init()
    Get_chromedriver(Identify_sys().system()).latest_version()