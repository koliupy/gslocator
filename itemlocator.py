from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from pathlib import Path
import sys
import os
import glob
import json
import time

# Set webdriver Options
options = Options()
options.headless = True

# Check for arguments
if(len(sys.argv) == 3):
    if (sys.argv[2] == '--headless-off' or sys.argv[2] == '-ho'):
        options.headless = False
elif (len(sys.argv) != 2):
    print('\nPlease enter the URL of the desired item as an argument.\n')
    print('USAGE: $python itemlocator.py <URL>\n')
    sys.exit()
else:
    if (sys.argv[1] == '--help' or sys.argv[1] == '-h'):
        print('\nOptions:\n')
        print('\tHeadless OFF: --headless-off | -ho\tBy default gslocator runs in headless mode.\n')
        print('\nUSAGE: $python itemlocator.py <URL> [options]\n')
        sys.exit()


# Open webdriver
profile_path = str(Path.home())  + '\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\'
profile_path = profile_path + glob.glob(profile_path + '*.default')[0].replace(profile_path, '')
profile = webdriver.FirefoxProfile(profile_path)
binary = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\Firefox.exe')

executable = os.getcwd() + '\\drivers\\geckodriver.exe'
log = os.getcwd() + '\\logs\\geckodriver.log'
driver = webdriver.Firefox(options=options, firefox_profile=profile, firefox_binary=binary, executable_path=executable, service_log_path=log)
driver.get(sys.argv[1])
title = driver.find_element_by_css_selector('#checkout > div > div.leftColumn.ats-productdetailcolumn > div > div.productDetails.ats-productdetails > h3 > a').text
time.sleep(8)

cities = json.load(open('resources\\o_cities.json', 'r'))['United States']
results = open('results\\' + title + '.txt', 'w')
found = []

if (options.headless):
    print('\ngslocator running in Headless Mode.')
print('\nSearch started for ' + title + '.\n')

try:
    for i, city in enumerate(cities):
        location = driver.find_element_by_css_selector('#puas_location')
        search = driver.find_element_by_css_selector('#puas_search')
        search.click()
        search.clear()
        search.send_keys(city)
        search.send_keys(Keys.ENTER)
        location.submit()
        time.sleep(8)
        store_names = driver.find_elements_by_css_selector('div.contactInfo > div.title.ats-storetitle')
        store_addresses = driver.find_elements_by_css_selector('div.contactInfo > div.address.ats-storeaddress')
        store_phones = driver.find_elements_by_css_selector('div.contactInfo > div.phoneNumber.ats-storephone')

        count = 0
        for j, store_name in enumerate(store_names):
            if (store_name.text not in found):
                found.append(store_name.text)
                results.write(store_name.text + '\n')
                results.write(store_addresses[j].text + '\n')
                results.write(store_phones[j].text + '\n')
                count = count + 1
        print('Searching... ' + str(i + 1) + '/' + str(len(cities)) + ' cities processed. Found ' + str(count) + ' units in ' + city + '. Total units found: ' + str(len(found)))

    print('\nSearch completed with ' + str(len(found)) + ' store results.')
finally:
    results.close()
    driver.quit()

results.close()
driver.quit()