import requests 
import spacy
from bs4 import BeautifulSoup

def LoopURL():
  #FOR LOOP TO GO THROUGH URLS
  r = requests.get(URL)
  getContent(r)
  

def getContent(r):
  URL = "https:..." 
  #LOOP through each of the urls 
  soup = BeautifulSoup(r.content, 'html5lib')
    

def spacyProcess: 
  
  
   
