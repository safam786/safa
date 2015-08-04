#to make request to the website
import requests
#to scrape using BeautifulSoup
import bs4
#to use regex
import re 
#to use JSON
import json

response = requests.get('http://www.islamawareness.net/Dua/rabbana.html')
soup = bs4.BeautifulSoup(response.text)

#grab everything in a 'td' element
links = [a for a in soup.select('td')]

#get rid of html tags; regex only works on Strings; first and last 'td's are POO
links = [re.sub('<[^<]+?>','',str(links[i])) for i in range(0,len(links)) if i != 0 and i != len(links)-1]

#iterator to zip
#http://stackoverflow.com/questions/23286254/convert-list-to-a-list-of-tuples-python
it = iter(links) 
links = zip(it,it,it,it)

#create set of tuples in form (number, translation, transliteration, arabic)
#use regex to extract verse number from translation
#   remove verse number and punctuation except !- and space from translation
#   remove verse number from arabic
"""
links = [(re.findall(r'\[[^\[]+?\]',j)[0],re.sub('(\[[^\[]+?\])|([^a-zA-Z!\- ])','',j),k,re.sub('\[[^\[]+?\]','',l)) for (i,j,k,l) in links]
"""

#same as above but without transliteration
links = [(re.findall(r'\[[^\[]+?\]',j)[0],re.sub('(\[[^\[]+?\])|([^a-zA-Z!\- ])','',j),re.sub('\[[^\[]+?\]','',l)) for (i,j,k,l) in links]

labels = ("number", "translation", "transliteration", "arabic")
labelsNoTransliteration = ("number", "translation", "arabic")

#match created labels above to corresponding data from 'links'
links = [dict(zip(labelsNoTransliteration,a)) for a in links]

#test
'''
print(links[0]["arabic"])
print(links[0]["number"])
print(links[0]["translation"])
'''

#make JSON
links = {"40 Rabbanas":links}

#output to file
with open('output.json','w') as outfile: 
    json.dump(links,outfile)
