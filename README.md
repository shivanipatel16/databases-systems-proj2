# databases-systems-proj2
Aditi Dam (ad3707) and Shivani Patel (svp2128)

**A list of all the files that you are submitting**
 - README.md
 - requirements.txt 
 - download_finetuned.sh
 - project2.py
 - googleapi.py 
 - textprocessing.py
 - spacy_help_functions.py
 - spanbert.py


## Install Requirements
First, create a conda environment running Python 3.6:

```bash
conda create --name spacyspanbert python=3.6
conda activate spacyspanbert
```

Then, install requirements and download spacy's en_core_web_lg:
```bash
sudo apt-get update
sudo apt install python3-pip
pip3 install --upgrade google-api-python-client
pip3 install -U pip setuptools wheel
pip3 install -U spacy
python3 -m spacy download en_core_web_lg
pip3 install -r requirements.txt
```

## Download Pre-Trained SpanBERT (Fine-Tuned in TACRED)
SpanBERT has the same model configuration as [BERT](https://github.com/google-research/bert) but it differs in
both the masking scheme and the training objectives.

* Architecture: 24-layer, 1024-hidden, 16-heads, 340M parameters
* Fine-tuning Dataset: [TACRED](https://nlp.stanford.edu/projects/tacred/) ([42 relation types](https://github.com/gkaramanolakis/SpanBERT/blob/master/relations.txt))

To download the fine-tuned SpanBERT model run: 

```bash
bash ./download_finetuned.sh
```

## How to run the program:
```python3 retrieval.py {google api key} {google engine id} {relation} {confidence threshold} {initial query} {# of tuples}```

 {relation} is an integer from 1 to 4:
 - 1 is for Schools_Attended
 - 2 is for Work_For
 - 3 is for Live_In
 - 4 is for Top_Member_Employees
 
Example program arguments
```AIzaSyAGmypTtalCS9lLgosvQiBQBIJ3FbviylU e1418010197679c8b 3 0.7 "megan repinoe redding" 2```

## Description of the internal design:
In our project folder, we have a README, a googleapi.py, project2.py, spacy_help_functions.py, spanbert.py, and textprocessing.py. 

**googleapi.py** makes a call to the Google search engine api to find top 10 url results for given query and handles checking for valid input arguments and whether the connection to the Google search engine is valid.

**textprocessing.py** gets the content from the url and cleans the text by only retrieving alphanumeric values, taking out the style, script, noscript, sup, img, and cite tags. It also removes the multiple whitespaces and trims the text to 20,000 characters. 

**helper_functions.py** [Adapted from SpacySpanBERT](hhttps://github.com/gkaramanolakis/SpacySpanBERT/blob/master/spacy_help_functions.py) Modified extract_relations() to only process (subj, object) tuples that are of the correct entity for the desired relation; drastically lowers the runtime of spanbert.predict()

**spanbert.py** [from SpacySpanBERT](https://github.com/gkaramanolakis/SpacySpanBERT/blob/master/README.md)

**project2.py** main program that first loads the nlp model, matches the correct entities of interest with the correpsonding relation desired, and then extracts relations from searching the query until k tuples of the desired relation that meets the confidence threshold


## External libraries:
- requests --> makes a request to a web page in order to extract its content
- from bs4 import BeautifulSoup --> pulls data out of HTML files and supports removing certain HTML tags
- re --> provides regular expression matching operations, used to parse text file to remove nonalphanumeric characters
- spaCy --> to process and annotate text by splitting into sentences and detecting entities of the tokens
- from collections import defaultdict --> returns a dictionary like object where there is a default value type if key is not defined
- tabulate --> print tabular data, used to print the relations extracted at each iteration


## Description of Step 3:
1) Retrieving the URLS: 
 - To retrieve the URLs, we utilized our project 1 code. We created a set of urls to keep track of the urls we already have seen. We skipped already-seen URLs by checking if it was in the set already. We ignored any non-HTML websites.

2) Getting Content: 
- To extract the actual plain text, we had a function called get_content in textprocessing.py. In get_content, we first did a get request to get the raw content of the website with a timeout of 20 seconds. Then, we utilized the library BeautifulSoup and used a html parser as a feature. BeautifulSoup pulls data out of HTML files. To get more relevant content for our program, we iterated through the data we extracted from BeautifulSoup and took out some tags such the style, script, noscript, sup, img, and cite tags. Thus, we were essentially left with the body of the html page. We also only kept alphanumeric values and took out multiple whitespaces. Lastly, we truncated the text to 20,000 characters by slicing the cleaned text. 

3) Extracting Entities:
 - The spacy library was used to split the now cleaned text into sentences and extracted named entities. An entity of interest list was created which corresponded to the relation it represented. For example, if relation was 1, the list of entities of interest were "PERSON" and "ORGANIZATION". The desired relation for this relation was "per:schools_attended". We applied this logic with the remaining relations from relation 1 to 4. We utilized this to only keep the entity pairs that were of the desired relation. This way we can avoid processing tuples that were not of the correct entity time. 

4) Predicting Relations: 
- From this we used the sentences and named entity pairs as input to SpanBERT to predict the correct corresponding relations and extracted all instances of the specified relation. The tuples that had a confidence greater than the threshold were added to a set if the tuple was never seen before OR if the same tuple was seen prior was a lower confidence level. If the tuple had a lower confidence, then we ignored it. 
 
## Parameters:
- Google Custom Search Engine JSON API Key: key = "AIzaSyAGmypTtalCS9lLgosvQiBQBIJ3FbviylU"
- Engine ID: id = 'e1418010197679c8b'
