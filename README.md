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

**How to run the program: **
Commands to run: 
sudo apt update 
sudo apt install 
python3-pip 
pip3 install beautifulsoup4
pip3 install tabulate


A clear description of the internal design of your project, explaining the general structure of your code (i.e., what its main high-level components are and what they do), as well as acknowledging and describing all external libraries that you use in your code


**External libraries: **


**Description of Step 3: **
To retrieve the URLs we utilized our project 1 code. 
We extracted the plain text from the webpage using the beautiful soup library in python. We truncated the plain text to 20,000 characters if it was longer than that. We then used the spacy library to split the tect into sentences and extract named entities.


For each URL from the previous step that you have not processed before (you should skip already-seen URLs, even if this involves processing fewer than 10 webpages in this iteration):
Retrieve the corresponding webpage; if you cannot retrieve the webpage (e.g., because of a timeout), just skip it and move on, even if this involves processing fewer than 10 webpages in this iteration.
Extract the actual plain text from the webpage using Beautiful Soup.
If the resulting plain text is longer than 20,000 characters, truncate the text to its first 20,000 characters (for efficiency) and discard the rest.
Use the spaCy library to split the text into sentences and extract named entities (e.g., PERSON, ORGANIZATION). See below for details on how to perform this step.
Use the sentences and named entity pairs as input to SpanBERT to predict the corresponding relations, and extract all instances of the relation specified by input parameter r. See below for details on how to perform this step.
Identify the tuples that have an associated extraction confidence of at least t and add them to set X.

Parameters Google Custom Search Engine JSON API Key: key = "AIzaSyAGmypTtalCS9lLgosvQiBQBIJ3FbviylU"

Engine ID: id = 'e1418010197679c8b'
