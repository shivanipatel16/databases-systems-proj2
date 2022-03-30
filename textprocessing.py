import requests
from bs4 import BeautifulSoup


def get_content(url):
    print("\tFetching text from url...") # TODO: try finally block
    try:
        html_text = requests.get(url, timeout=20).text
        text = BeautifulSoup(html_text, features="html.parser").get_text()
        if len(text) > 20000:
            print("\tTrimming webpage context from {} to 20000 characters".format(len(text)))
            text = text[:20000]

        print("Webpage length (num characters): {}".format(len(text)))
        return text
    except Exception as e:
        print("\tsomething went wrong...")
