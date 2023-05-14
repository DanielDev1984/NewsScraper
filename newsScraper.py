import os
from bs4 import BeautifulSoup
import requests

os.system('color')
os.system("Cls") #clears screen

# simple web scraper for retrieving the  teaser of the latest news from rheinfelden.de using BeautifulSoup
# the ID of the latest found article is persisted on the file system to set a highlight on the last read article
# only if really a new entry is available
# logo idea taken / forked from https://github.com/sairash/spotify-1975

page_to_scrape = requests.get("https://www.rheinfelden.de/de/aktuell/Staedtische-Nachrichten")
soup = BeautifulSoup(page_to_scrape.text, "html.parser")
# date of the articles
dates = soup.findAll("div", attrs={"class":"cNews_rowDate"})
# title of the articles
headers = soup.findAll("div", attrs={"class":"cNews_rowTitle"})
# preview / teaser of the articles
teasers = soup.findAll("div", attrs={"class":"cNews_rowTeaser"})
# links to the referenced articles -> needed for extracting the articleID to allow for determining whether there are new articles available
links = soup.findAll("a", attrs={"class":"cNews_rowLink"})

# really simple / volatile way of determining which articles already have been read / displayed by the scraper
# read ID of last read entry from previous session
f = open("lastID.txt", "r")
lastID = int(f.read())
f.close()

# safe ID of most recent entry of the current fetch / get
mostRecetID = int(links[0]['href'].split('&id=')[1])
# always persist most recent entry
f = open("lastID.txt", "w")
f.write(str(mostRecetID))
f.close()   

# determine wether there has been a new article pusblished since the last time the script has been executed
updateAvailable = (mostRecetID > lastID) 


with open('logo.txt', 'r') as f:
    for line in f:
        print(line.rstrip())


# helper index to iterate over all fetched arrays
# todo: isnt there an easier way to iterate over all of the relevant data?
i=0
for header in headers:
    print("\n")
    # last read entry, only highlighted when an update is available
    if updateAvailable and (lastID == int(links[i]['href'].split('&id=')[1])):
        print( dates[i].text + '\33[101m' + header.text + '\033[0m')
    else:
        # entry newer than last read, visual indication
        if lastID < int(links[i]['href'].split('&id=')[1]):
            print( dates[i].text + '\33[100m' + header.text + '\033[0m')
        # entry older than last read, headers are visually taken out of the readers focus
        else:
            print( dates[i].text + '\33[90m' + header.text + '\033[0m')
    print(teasers[i].text)
    i = i + 1