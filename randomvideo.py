import json
import urllib.request
import string
import random
from tkinter import *
from tkinter.messagebox import showinfo
import webbrowser

#ui counters 
clickCounterYear = 0

#search function toggles
searchYear = 0
durationSearch = 0 

#duration
durationUse = None

#counts attempts to search
YTCounter = 0

initialize = Tk()
initialize.geometry('350x250')
initialize['background'] = '#ffffff'
initialize.title('YouTube Randomizer')
initialize.resizable(False, False)

titleLabel = Label(initialize, text = 'YouTube Randomizer!', font = ('bold', 24), background = '#ffffff')
titleLabel.pack()

face = Label(initialize, text = '( ◡‿◡ )', font = ('bold', 30), background = '#ffffff')
face.place(x= 108, y = 180)


#years dropdown menu
years = [2022,2021,2020,2019,2018,2017,2016,2015,2014,2013,2012,2011,2010,2009,2008,2007,2006]

yearChoice = StringVar(initialize)
yearChoice.set(years[0])

yearMenu = OptionMenu(initialize, yearChoice, *years)
yearMenu.place(x = 220, y = 120)
yearMenu.configure(state="disabled")

def buttonPressYear():
  global clickCounterYear
  clickCounterYear = clickCounterYear + 1
  if clickCounterYear == 1:
      yearMenu.configure(state="active")
  else:
    yearMenu.configure(state="disabled")
    clickCounterYear = 0

c1 = Checkbutton(initialize, text='Before', onvalue=1, offvalue=0,  command = buttonPressYear)
c1.place(x = 50, y = 120)

#duration dropdown menu
duration = ['any', 'long', 'medium', 'short']

durationChoice = StringVar(initialize)
durationChoice.set(duration[0])

durationMenu = OptionMenu(initialize, durationChoice, *duration)
durationMenu.place(x = 220, y = 80)

def youtube():
  global searchYear
  global year
  global durationUse
  global YTCounter
  global face

  faceToggle = 0

  try: 
    while True:
      count = 1 #if it goes beyond one, the program outputs videos with similar titles. so its set to 1
      API_KEY = 'AIzaSyBHXQJ1KWqwCluldKjz9cYSiwCPX37Ijbg'

      #make range random for more random results
      numTry = random.randint(3,5)

      find = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(numTry))

      urlData = "https://www.googleapis.com/youtube/v3/search?videoDuration={}&key={}&maxResults={}&part=snippet&type=video&q={}".format(durationUse, API_KEY,count,find)
      #url changes based on options selected

      if searchYear == 1:
        urlData = urlData + "&publishedBefore={}-01-01T00:00:00.0Z".format(year)

      webURL = urllib.request.urlopen(urlData)
      data = webURL.read()
      encoding = webURL.info().get_content_charset('utf-8')
      results = json.loads(data.decode(encoding))

      if len(results['items']) == 0:
        YTCounter += 1
        if YTCounter == 4:
          YTCounter = 0
          faceToggle = 1
          raise Exception('No results found.') 
        else:
          continue
      else:
        YTCounter = 0
        break

    #make face happy again if it changed
    face = Label(initialize, text = '( ◡‿◡ )', font = ('bold', 30), background = '#ffffff')
    face.place(x= 108, y = 180)

    for data in results['items']:
        videoId = (data['id']['videoId'])
        webbrowser.open('https://www.youtube.com/watch?v=' + str(videoId))
  except:
    if faceToggle == 1:
        face.config(text = '(●︿●)', font = ('bold', 30)) 
        face.place(x= 108, y = 180)
        raise Exception
    else:
        face.config(text = '(X_X)', font = ('bold', 30)) 
        face.place(x= 108, y = 180)
        raise Exception

def search():
  #global variables
  global clickCounterYear
  global searchYear
  global year
  global durationUse

  #variables for search
  searchYear = 0

  if clickCounterYear == 1:
      year = yearChoice.get()
      searchYear = 1
    
  durationUse = durationChoice.get() 
  
  youtube()

searchButton  = Button(initialize, text = 'Search', height = 1, width = 10, command = search)
searchButton.place(x = 127, y = 50)


initialize.mainloop()


