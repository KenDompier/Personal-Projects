import csv
from csv import *
import shutil
import requests
import tweepy
from random import *
import os

#TWITTER DETAILS
auth = tweepy.OAuthHandler("key here")
auth.set_access_token("token here")
API = tweepy.API(auth)

#randomly chooses publisher
pubSearch = choice(['"Mcgraw+Hill"','"Pearson+Education"', '"Houghton+Mifflin"'])

#DICTIONARY OF BOOKS
bookDict = {}
fieldNames = ['Title', 'Author']

#TWITTER CAPTION
tweetDetails = []

#PIC FILE SIZE
size = []

#IS OR ISNT IN CSV FILE
csvToggle = [0]

#FINDS RANDOM BOOK
def getBook(search): 
    url = 'http://openlibrary.org/search.json?author=' + search
    resp = requests.get(url)
    json = resp.json()

    pageCount = round(json['num_found'] / 100)
    
    resultCount = len(json['docs']) #counts amount of results
    #if there is more than 1 page of results

    #randomize page number
    counterPage = 0 #shuffle
    while counterPage < 100:
        pageNum = randint(0, pageCount)
        counterPage += 1

    url = 'http://openlibrary.org/search.json?author=' + search + '&page=' + str(pageNum)
    #if there is an error because there is no cover, randomize again until result has a cover
    while True:
        try: 
            counter = 0 #shuffles
            while counter < 100:
                book = randint(0, resultCount - 1)
                counter += 1
            id = json['docs'][book]['cover_i']
            title = json['docs'][book]['title']
            author = json['docs'][book]['author_name'][0]                
        except: 
            continue
        else:
            coverLink = ('https://covers.openlibrary.org/b/id/' + str(id) + '-L.jpg')

            #adds title with author into book dictionary 
            bookDict['Title'] = title
            bookDict['Author'] = author
            
            #puts in twitter details list for later
            tweetDetails.append(title)
            tweetDetails.append(author)

            #downloads book cover
            downloadCover(coverLink, id)

            break


#DOWNLOADS BOOK COVER TO COMPUTER
def downloadCover(coverLink, id):
    fileName = str(id) + '.jpg'

    r = requests.get(coverLink, stream = True)
    #check if the image was retrieved successfully
    if r.status_code == 200:
        #set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True
        #Open a local file with wb permission.
        with open(fileName,'wb') as f:
            shutil.copyfileobj(r.raw, f)
        print('Image sucessfully Downloaded: ',fileName)

    else:
        print('Image Couldn\'t be retreived')

    path = 'C:/Users/Admin/Coding/attempt1/new/' + fileName 
    imgSize = os.path.getsize(path)
    size.append(imgSize)
    #adds to tweet details list
    tweetDetails.append(fileName)

#SEARCHES FOR BOOK TITLE + AUTHOR IN CSV FILE TO PREVENT POSTING SAME BOOK TWICE
def search():
    with open('bookDict.csv', 'rt') as f:
        reader = csv.reader(f, delimiter=',') 
        for row in reader:
            if bookDict['Title'] and bookDict['Author'] in row:
                csvToggle[0] = 1
                break

#PART THAT POSTS IT TO TWITTER
def postTweet():
    # Create a tweet
    caption = "Title: " + tweetDetails[0] + '\nAuthor/Publisher: ' + tweetDetails[1]
    API.update_status_with_media(filename = tweetDetails[2], status = caption)


#running process
while True:
    getBook(pubSearch)
    search()
    #if size of image file less than 4 mb, find another textbook to post
    if size[0] <= 4096:
        #remove info in dictionary for new book
        bookDict.clear()
        csvToggle[0] = 0
        continue
    elif csvToggle[0] == 1:
        #remove info in dictionary for new book
        bookDict.clear()
        csvToggle[0] = 0
        continue
    else:
        #if over 4 mb, post to twitter
        postTweet()
        #creates file with book dictionary
        with open('bookDict.csv', 'a') as f_object:
            dictwriter_object = DictWriter(f_object, fieldnames=fieldNames)
            dictwriter_object.writerow(bookDict)
            f_object.close()
        break
        
