from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
opts = Options()
opts.set_headless()
assert opts.headless  # Operating in headless mode
browser = Chrome(options=opts)
browser.get('https://duckduckgo.com')

search_form = browser.find_element_by_class_name('js-search-input.search__input--adv')
search_form.send_keys('real python')
search_form.submit()

results = browser.find_elements_by_class_name('result')
print(results[0].text)
print(len(results))

for i in range(len(results)):
  print(results[i].text)

browser.close
