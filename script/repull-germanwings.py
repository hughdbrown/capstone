from __future__ import absolute_import, print_function

# System libraries
import os
import os.path
import random

# Third party libraries
from selenium import webdriver

from bs4 import BeautifulSoup

import requests

from script.utils.clean_data import clean


PHANTOM_PATH = '/usr/local/bin/phantomjs'


def main():
    all_files = os.listdir("raw")
    random.shuffle(all_files)
    for i, filename in enumerate(all_files, start=1):
        rawfile, cleanfile = tuple(os.path.join(p, filename) for p in ("raw", "clean2"))
        print("{0}: {1} / {2}".format(filename, i, len(all_files)))
        if os.path.isfile(rawfile) and not os.path.exists(cleanfile):
            url = "http://bit.ly/{0}".format(filename)
            try:
                cap = webdriver.DesiredCapabilities.PHANTOMJS
                cap["phantomjs.page.settings.resourceTimeout"] = 1000
                cap["phantomjs.page.settings.loadImages"] = False
                cap["phantomjs.page.settings.userAgent"] = "faking it"
                driver = webdriver.PhantomJS(desired_capabilities=cap, executable_path=PHANTOM_PATH)
                driver.implicitly_wait(10)
                driver.set_page_load_timeout(10)
                r = requests.head(url, allow_redirects=True)
                final_url = r.url
                driver.get(final_url)
                data = clean(driver.page_source)
                soup = BeautifulSoup(data, "lxml")
                clean_data = soup.get_text(strip=True)
                with open(cleanfile, "w") as f:
                    f.write(clean_data.encode("ascii", "ignore"))
            except Exception as exc:
                print("{0}: {1}".format(filename, exc))
            finally:
                driver.close()


if __name__ == '__main__':
    main()
