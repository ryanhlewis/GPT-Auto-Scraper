#
#   ChatGPT Selenium Implementation
#   Author: eric88525
#   Edited lightly..
#

from selenium.webdriver.remote.webdriver import By
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
import pyperclip

class gptParser:
    def __init__(self,
                 driver,
                 gpt_url: str = 'https://chat.openai.com/'):
        """ ChatGPT parser
        Args:
            driver_path (str, optional): The path of the chromedriver.
            gpt_url (str, optional): The url of ChatGPT.
        """
        # Start a webdriver instance and open ChatGPT
        self.driver = driver
        self.driver.get(gpt_url)

    @staticmethod
    def get_driver(driver_path: str = None,):
        options = uc.ChromeOptions()
        options.binary_location = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
        return uc.Chrome(options) if driver_path is None else uc.Chrome(driver_path)

    def __call__(self, query: str):
        # Find the input field and send a question
        input_field = self.driver.find_element(
            By.TAG_NAME, 'textarea')
        pyperclip.copy(query)
        input_field.send_keys(Keys.CONTROL, 'v')
        input_field.send_keys(Keys.RETURN)

    def read_respond(self):
        try:
            # Get the last "code" tag element
            response = self.driver.find_elements(By.TAG_NAME, 'code')[-1].text
            return response
        except:
            return None

    def new_chat(self):
        """Open a new chat"""
        # Check if Clear Chat exists, otherwise open a new chat
        try:
            self.driver.find_element(By.XPATH, '//a[text()="Clear chat"]').click()
        except:
            self.driver.find_element(By.XPATH, '//a[text()="New chat"]').click()

    def close(self):
        # Save cookies and close the driver
        self.driver.quit()


#
#   Server implementation for GPT-3.5 API
#   Author: rhl
#

import time
import urllib.parse
import http.server
import socketserver

driver = gptParser.get_driver()
gpt = gptParser(driver=driver)

input('After you login, press enter to continue.')

port = 8000

Handler = http.server.SimpleHTTPRequestHandler

# Post a request with the following parameters:
#   q: query
#   t: time to wait before responding
#   newchat: if true, open a new chat

# Return code on POST requests
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        content_length = int(self.headers['Content-Length'])
        post_data = urllib.parse.parse_qs(self.rfile.read(content_length).decode('utf-8'))
        query = post_data['q'][0]
        seconds = int(post_data['t'][0])
        # If newchat is true, open a new chat, or clear existing chat
        if 'newchat' in post_data:
            gpt.new_chat()
        gpt(query)
        time.sleep(seconds)
        response = gpt.read_respond()
        self.wfile.write(bytes(response, 'utf-8'))

with socketserver.TCPServer(("", port), MyHandler) as httpd:
    print(f"serving at port {port}")
    httpd.serve_forever()