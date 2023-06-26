# GPT Auto Scraper
GPT Auto Scraper is a project that leverages AI capabilities to carry out web scraping tasks. It offers a solution for pulling out information from HTML data sources according to the specifications set by the user. It not only creates the necessary scraping code in Python but also runs it to fetch the data of interest.

## Free?

Yes. As scraping HTML pages uses thousands of tokens, it is not possible to use the API version of GPT-3.5. Instead, we use the free version of ChatGPT via browser automation tool Selenium.

### Step 1
Download [Chrome](https://www.google.com/chrome/). I strongly recommend that you update to the latest version of Chrome.

**No Chrome?**
We need something Chromium based for *undetected_chromedriver* to remain undetected. You can download [Microsoft Edge](https://www.microsoft.com/en-us/edge) or [Chromium](https://chromium.com/) and change Line 28 in *server.py* to the path of the browser you downloaded.

### Step 2
Install the required packages [Selenium](https://github.com/SeleniumHQ/selenium) and [undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver)
```
pip install -r requirements.txt
```

### Step 3
Run the ChatGPT browser server as a mock API. Do ```python server.py``` in the terminal, and login to your OpenAI account. Then, press ```Enter``` in the terminal to start the server.

### Step 4
Now, run ```python scraper.py``` in the terminal. Make sure to open ```scraper.py``` and switch out the needed data format in the prompt,
as well as the URL of the website you want to scrape.

## Future
- [ ] Add websites.txt, list of websites to scrape
- [ ] Add settings.json, settings for the scraper

### Credits
- [OpenAI](https://openai.com/)
- [Selenium](https://github.com/SeleniumHQ/selenium)
- [GPT-Parser](https://github.com/eric88525/Gpt-Selenium)
- [Undetected-Chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver)