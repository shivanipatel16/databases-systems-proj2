import requests
from bs4 import BeautifulSoup
import re

def get_content(url):
    print("\tFetching text from url...")  # TODO: try finally block
    try:
        html_text = requests.get(url, timeout=20).text
        soup = BeautifulSoup(html_text, features="html.parser")

        for data in soup(['style', 'script', 'noscript', 'sup', 'img', 'cite']):
            # Remove tags
            data.decompose()

        text = soup.get_text(separator="\n", strip=False)

        # maybe header tag
        # remove no script tag
        # alphanumeric is all we neeed -- ascii characters

        cleaned_text = " ".join(text.split())
        cleaned_text = re.sub(r'[^\x00-\x7F\xA9]+', '', cleaned_text)


        print("Webpage length (num characters): {}".format(len(text)))
        if len(cleaned_text) > 20000:
            print("\tTrimming webpage context from {} to 20000 characters".format(len(cleaned_text)))
            cleaned_text = cleaned_text[:20000]

        return cleaned_text
    except Exception as e:
        print("\tsomething went wrong...")
        print(e)
        return ""
