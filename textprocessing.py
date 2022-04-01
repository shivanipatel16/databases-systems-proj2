import requests
from bs4 import BeautifulSoup
import re

#gets the content of the html page and cleans the text so that we essentially get the body of the html page and the best context. 
def get_content(url):
    print("\tFetching text from url...")  # TODO: try finally block
    try:
        html_text = requests.get(url, timeout=20).text
        soup = BeautifulSoup(html_text, features="html.parser")

        for data in soup(['style', 'script', 'noscript', 'sup', 'img', 'cite']): 
            # Remove tags
            data.decompose()

        text = soup.get_text(separator="\n", strip=False)



        cleaned_text = " ".join(text.split()) #removes multiple white spaces
        cleaned_text = re.sub(r'[^\x00-\x7F\xA9]+', '', cleaned_text) #gets alphanumeric values only


        print("Webpage length (num characters): {}".format(len(text)))
        if len(cleaned_text) > 20000:
            print("\tTrimming webpage context from {} to 20000 characters".format(len(cleaned_text)))
            cleaned_text = cleaned_text[:20000] #slices the text to 20,000 characters

        return cleaned_text
    except Exception as e:
        print("\tsomething went wrong...") #error message that displays
        print(e)
        return ""
