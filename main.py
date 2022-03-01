"""
CREATED: 25-FEB-2022
LAST EDIT: 01-MAR-2022
AUTHOR: DUANE RINEHART (drinehart@ucsd.edu)
FUNCTION: TEST FRONT-END FUNCTIONALITY OF ACTIVEBRAINATLAS.UCSD.EDU
"""

import os
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pathlib import Path

BASEURL = 'https://activebrainatlas.ucsd.edu'
BROWSER_DRIVER_PATH = os.path.join("/", 'data', "selenium", "browsers")

class Log:
    _LOGFILE = 'auto_test_' + datetime.today().strftime('%Y-%m-%d') + '.log'
    _LOGFILE_PATH = os.path.join('/', 'mnt', 'webdev', _LOGFILE)

    def __init__(self):
        """
        -CHECK FOR PRESENCE OF LOG FILE (RW PERMISSION)
        -SET CONFIG FOR LOGGING
        """

        try:
            with open(self._LOGFILE_PATH, 'a') as f:
                pass
        except FileNotFoundError:
            Path(self._LOGFILE_PATH).touch()

        logging.basicConfig(
            filename=self._LOGFILE_PATH,
            level=logging.INFO,
            format="%(message)s",
            force=True
        )

    def event(self, msg):
        timestamp = datetime.today().strftime('%H:%M:%S')
        logging.info(f"{timestamp} - {msg}")


def main():
    log = Log()
    log.event('INIT APP')

    # LOAD [CHROME] BROWSER
    ser = Service(os.path.join(BROWSER_DRIVER_PATH, 'chromedriver'))
    op = webdriver.ChromeOptions()

    # OPTIONS '--no-sandbox' AND '--disable-dev-shm-usage' ARE REQUIRED FOR CRON JOB
    op.add_argument('--no-sandbox')
    op.add_argument('--disable-dev-shm-usage')

    #op.add_experimental_option("detach", True) #LEAVE BROWSER OPEN AFTER SCRIPT ENDS (TESTING)
    driver = webdriver.Chrome(service=ser, options=op)

    driver.get(BASEURL)
    if "Active Atlas Viewer" not in driver.title:
        log.event(f'BASE URL ({BASEURL}) PAGE NOT LOADED')
    else:
        #FOUND BASE URL PAGE; CONTINUE
        elem = driver.find_element(By.XPATH, '//button[text()="View Brain DK39"]/parent::*')
        href = elem.get_attribute("href") #CAPTURE HREF FOR; DO NOT CLICK ON ELEMENT
        driver.get(href) #LOAD HREF ELEMENT

        if "neuroglancer" not in driver.title:
            current_url = driver.current_url
            log.event(f'NEUROGLANCER ({current_url}) PAGE NOT LOADED')
        else:
            #FOUND NEUROGLANCER PAGE; CONTINUE
            log.event(f'MAIN SITE + NEUROGLANCER (DK39) LOADED SUCCESSFULLY')

    driver.close()
    log.event('END APP')

    #APACHE INDEX OF FOLDER (Options +Indexes)


if __name__ == '__main__':
    main()
