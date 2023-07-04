#needed to start a browser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

#needed for command line arguments
import argparse

#parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument('-s','--search_for', help='what are you looking for')

args = parser.parse_args()

#check if arguments are available, ask for user input if not
if(args.search_for):
   search_for = args.search_for
else:   
   search_for = input("What are you looking for? ")

#start the browser with options
browser = webdriver.Chrome(ChromeDriverManager().install())
opts = Options()
opts.headless=True
browser.get('https://duckduckgo.com')

search_form = browser.find_element_by_class_name('js-search-input.search__input--adv')
search_form.send_keys(search_for)
search_form.submit()

browser.close
