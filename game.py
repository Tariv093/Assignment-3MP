import random
import socket
import time
from _thread import *
import threading
from datetime import datetime
import json
import requests
import sys

urlUpdate = "https://hdo928xxa4.execute-api.us-east-2.amazonaws.com/default/UpdatePlayers"
urlGetPlayers = "https://hizvu7kzba.execute-api.us-east-2.amazonaws.com/default/GetPlayer"
queryParams = {'user_id': 'player' , 'rating' : 'r'}



numGames = input("How many games do you want to play")
f = open('multiplayerLog', 'w')
sys.stdout = f

response = requests.get(urlGetPlayers)
responseBody = json.loads(response.content)

items = responseBody['Items']


for x in range(0,int(numGames)):
    player1 = random.randrange(0,len(items))
    player2 = random.randrange(0,len(items))
    while(player2 == player1):
        player2 = random.randrange(0,len(items))
    player3 = random.randrange(0,len(items))
    while(player3 == player2 or player3 == player1):
        player3 = random.randrange(0,len(items))
    print(items[player1]['user_id'] + ' ' + items[player1]['rating'])
    print(items[player2]['user_id'] + ' ' + items[player2]['rating'])
    print(items[player3]['user_id'] + ' ' + items[player3]['rating'])

    tempNum = 0
    for y in range(0,(len(items))):
        tempNum += float(items[y]['rating'])
     
    averageRating =  tempNum/len(items)
    
    if(items[player1]['rating'] < items[player2]['rating'] and items[player1]['rating'] < items[player3]['rating']):
        winner = player1
        loser = player2
        loser2 = player3
    elif (items[player2]['rating'] < items[player1]['rating'] and items[player2]['rating'] < items[player3]['rating']):
        winner = player2
        loser = player1
        loser2 = player3
    else:
        winner = player3
        loser = player1
        loser2 = player2

    winnerRating = float(items[winner]['rating']) + 25 *(1+averageRating/400)
    loserRating1 = float(items[loser]['rating']) - 25 *(0+averageRating/400)
    loserRating2 = float(items[loser2]['rating']) - 25 *(0+averageRating/400)
newReq = urlUpdate + '?user_id='+items[winner]['user_id']+'&rating='+str(winnerRating)
response = requests.put(newReq)
    #responseBody = json.loads(response.content)
newReq = urlUpdate + '?user_id='+items[loser]['user_id']+'&rating='+str(loserRating1)
response = requests.put(newReq)
newReq = urlUpdate + '?user_id='+items[loser2]['user_id']+'&rating='+str(loserRating2)
response = requests.put(newReq)
f.close()

