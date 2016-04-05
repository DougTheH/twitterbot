#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import tweepy, time, requests, random, json
 
#enter the corresponding information from your Twitter application:
CONSUMER_KEY = 'dt4zPpEy0dGjW9BTIZbUdykgu'
CONSUMER_SECRET = 'dbhXzbYyI7jThh9yYFrdy6Ojeyg3wA5MjENEnuKJCPAzIWZbVq'
ACCESS_KEY = '4928395696-eC87rM0lAKxoXyWywCwUrxyOALniJgnDDOYEAHn'
ACCESS_SECRET = 'HwVERue2Kju10LEvauGBoO497TKESeOgpWJdC9dVXJmgb'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

#setup and configure wordnik
from wordnik import *
apiUrl = 'http://api.wordnik.com/v4'
apiKey = 'e0132253b500d86f2770a0fa17503574624031335fc30f360'
client = swagger.ApiClient(apiKey, apiUrl)
wordApi = WordApi.WordApi(client)



while(True):
    hashtag = None
    #generate Instagram API request to get image.
    url = 'http://api.instagram.com/v1/media/search'
    latitude = random.uniform(24,50)
    longitude = random.uniform(66, 125)
    distance = 500
    
    #test with known working coordinates for downtown Austin, TX
    #latitude = 30.25
    #longitude = 97.75
    
    #test with working coordinates for downtown San Francisco, CA
    #latitude = 37.77
    #longitude = 122.41
    
    #test with working coordinates for downtown Times Square, Manhatten, NY
    #latitude = 40.758
    #longitude = 73.985
    
    #test with working coordinates for downtown Chicago, IL
    #latitude = 41.88
    #longitude = 87.62
    
    #test with coordinates returning no pictures
    #latitude = 55.87
    #longitude = 104.26
    
    payload = {'access_token' : '2957131468.1fb234f.aba3af5c2b3a452390a0246da404895f', 'lat' : latitude, 'lng' : longitude, 'distance' : distance}
    response = requests.get(url, params = payload)
    
    #check for errors
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        #print('unable to connect to instagram server at this time', e.message)
        continue
    #Load JSON data into a Python variable.
    
    #try to select the first picture in imagesData array, along with first hashtag
    try:
        imagesData = json.loads(response.text)
        imageKey = imagesData['data'][1]
        imageKeyLink = imageKey['link']
        #print(imageKeyLink)
        
        #get first hashtag
        hashtag = (imageKey['tags'][0])
        #print ('hashtag is %s', hashtag)
        
        #Unable to figure out why I can't use get() to iterate through all the hashtags    
        #if imagesData.get('tags'[0]) is not None:
            #for i in imagesData.get('tags'):
                #if imagesData.get('tags'[i]) is not None:
                    #imageKeyTags.append(imagesData.get('tags'[i]))
        #else:
            #print('No Tags')    
            #continue
    
        #print('in the try block')
    except (IndexError):
        #handle this
        #print('in the index exception handler')
        continue
    
    
    
    #use wordnik to generate comment from hashtag
    #test a nonvalid word as hashtag
    #hashtag = 'atx'
    
    if hashtag is not None:
        synonym = wordApi.getRelatedWords(hashtag, relationshipTypes = 'synonym', useCanonical = 'true',  limitPerRelationshipType = 1)
    else:
        synonym = None
        continue
    
    if synonym is not None:
        #print (synonym[0].words)
        definitions = wordApi.getDefinitions(synonym[0].words, partOfSpeech='noun/verb', sourceDictionaries='wordnet', limit = 1)
        #print(definitions[0].word)
        #print(definitions[0].text)
        
        #generate tweet
        tweet = definitions[0].text + ' '
        tweet += imageKeyLink
        #print(tweet)
        
        if len(tweet) < 140:
            api.update_status(tweet)
            time.sleep(900)#Tweet every 15 minutes
            #print('tweeting')
        else:
            #print('tweet too long')
            continue
        
        
    else:
        #print('synonym was None')
        time.sleep(300)#Reattempt every 5 minutes
        continue

