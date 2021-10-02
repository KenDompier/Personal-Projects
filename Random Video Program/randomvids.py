#finds random "short" videos on youtube from before 2013.
def youtube():
  import json
  import urllib.request
  import string
  import random
  count = 1 #if it goes beyond one, the program outputs videos with similar titles. so its set to 1
  API_KEY = #your key here
  random = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))

  urlData = "https://www.googleapis.com/youtube/v3/search?publishedBefore=2012-12-31T00:00:00.0Z&videoDuration=short&key={}&maxResults={}&part=snippet&type=video&q={}".format(API_KEY,count,random)
  webURL = urllib.request.urlopen(urlData)
  data = webURL.read()
  encoding = webURL.info().get_content_charset('utf-8')
  results = json.loads(data.decode(encoding))

  for data in results['items']:
      videoId = (data['id']['videoId'])
      print('https://www.youtube.com/watch?v=' + str(videoId))
      #store your ids

 #by doing this, the next videos the program outputs won't be related to each other via title.
counter = 0
while counter < 10:
  youtube()
  counter = counter + 1
