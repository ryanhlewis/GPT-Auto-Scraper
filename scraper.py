import re
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests
from selenium.webdriver.common.by import By
import glob

url = 'https://www.google.com/search?q=hello+world&tbm=isch'

driver = webdriver.Chrome() # or webdriver.Chrome() or whichever browser driver you use
driver.get(url) 

time.sleep(5)

html = driver.page_source

# Clean up the HTML, remove all script and style tags, img tags, and comments 
soup = BeautifulSoup(html, 'html.parser')
for script in soup(["script", "style", "img", "comment","svg","meta","link","a","nav","input"]):
    script.extract()

# Remove everything except for the structure of the DOM.All style and class attributes are removed.
for tag in soup.findAll(True):
    # dO NOT REMOVE THE FOLLOWING TAGS
    # CLASS, ID
    for attr in tag.attrs.copy():
        if attr not in ['class', 'id']:
            del tag[attr]
    #tag.attrs = {}

# Remove all empty elements (no text)
for tag in soup.findAll(True):
    if len(tag.text.strip()) == 0:
        tag.extract()

# Remove any class or id that says footer or is displayed as a footer, or display:none
for tag in soup.findAll(True):
    if 'footer' in tag.get('class', []) or 'footer' in tag.get('id', []) or 'footer' in tag.get('style', []):
        tag.extract()

# Remove all classes except for the first one on each tag
for tag in soup.find_all():
    if tag.has_attr('class'):
        tag['class'] = tag['class'][0:1]

# Remove repetitive single child tags and keep the text
for tag in soup.find_all():
    if len(tag.contents) == 1 and tag.contents[0].name:
        if tag.contents[0].string:
            tag.string = tag.contents[0].string

html = str(soup)

# Remove blank lines
html = '\n'.join([line for line in str(soup).splitlines() if line.strip() != ''])

# Remove any html comments
html = re.sub(r'<!--.*?-->', '', html)

# Remove any empty divs
html = re.sub(r'<div\s*>\s*</div>', '', html)

# No empty lines
html = re.sub(r'\n\s*\n', '\n', html)

print(html)
driver.quit()


pythoncode = """from bs4 import BeautifulSoup
from selenium import webdriver
import json
import time
driver = webdriver.Chrome()
url = '{}'
driver.get(url)
time.sleep(5)
html = driver.page_source
driver.quit()
soup = BeautifulSoup(html, 'html.parser')""".format(url)

# A diffrent style of prompting that puts the HTML at the end
query = "Write Python code using BeautifulSoup to scrape picture information from their URL ({}) using Selenium Edge and save the JSON result to a root domain .json. \n\n\nExtend from here: \n\n\n{}\n\n\nHere is the HTML: \n\n{}...".format(url, pythoncode, html)

response = requests.post('http://localhost:8000', data={'q': query, 't': 20})#, 'newchat': True})
print(response.text)

# Execute the code, if it fails, pass the code and the error back to ChatGPT for up to 3 tries
code = response.text
for i in range(3):
    try:
        exec(code)
        files = glob.glob("*.json")
        for file in files:
            if len(file) > 2:
                print('Scraping completed. JSON data saved as "{}"'.format(file))
                break
            else:
                print('JSON data is empty. Trying again.')
                continue
        break
    except Exception as e:
        print(e)
        response = requests.post('http://localhost:8000', data={'q': f"{code}\n{e}", 't': 10})
        code = response.text

# Write the Python code to a file
with open('webscraper.py', 'w') as f:
    f.write(code)

