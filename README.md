# databases-systems-proj2
Aditi Dam (ad3707) and Shivani Patel (svp2128)

**A list of all the files that you are submitting**
Zip file with: 
- README.md 
- googleapi.py
- project2.py
- requirements.txt
- spacy_help_functions.py
- spanbert.py
- textprocessing.py
- download_finetuned.sh

**How to run the program:**
Commands to run: 
sudo apt update 
sudo apt install 
python3-pip 
pip3 install beautifulsoup4
pip3 install tabulate


**Description of the internal design:**


**External libraries:**
- requests
- from bs4 import BeautifulSoup
- re
- spacy 
- from spanbert import SpanBERT
- from collections import defaultdict
- sys
- tabulate


**Description of Step 3:**
1) Retrieving the URLS: 
 - To retrieve the URLs, we utilized our project 1 code. We created a set of urls to keep track of the urls we already have seen. We skipped already-seen URLs by checking if it was in the set already.

2) Getting Content: 
- To extract the actual plain text, we had a function called get_content in textprocessing.py. In get_content, we utilized the library BeautifulSoup and used a html parser as a feature. Beautiful soup pulls data out of HTML files. To get more relevant content for our program, we iterated through the data we extracted from Beautiful Soup and took out some tags such the style, script, noscript, sup, img, and cite tags. Thus, we were essentially left with the body of the html page. We also only kept alphanumeric values and took out multiple whitespaces. Lastly, we truncated the text to 20,000 characters by slicing the cleaned text. 

3) Extracting Entities:
 - The spacy library was used to split the now cleaned text into sentences and extracted named entities. An entity of interest list was created which corresponded to the relation it represented. For example, if relation was 1, the list of entities of interest were "PERSON" and "ORGANIZATION". The desired relation for this relation was "per:schools_attended". We applied this logic with the remaining relations from relation 1 to 4. 

4) Predicting Relations: 
- From this we used the sentences and named entity pairs as input to SpanBERT to predict the correct corresponding relations and extracted all instances of the specified relation. The tuples that had a confidence greater than the threshold were added to a set. 
 
**Parameters:**
Parameters Google Custom Search Engine JSON API Key: key = "AIzaSyAGmypTtalCS9lLgosvQiBQBIJ3FbviylU"

Engine ID: id = 'e1418010197679c8b'
