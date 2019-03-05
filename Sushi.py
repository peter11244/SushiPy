# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 00:34:17 2017
@title: Sushi Go in Py
@author: psach
"""

#Cardset Currently Fixed
#number of players needs to affect rules/cards

import random
import math
from itertools import groupby as g

class SushiPy:
  #Defines a game of SushiGo
  
  def __init__ (self,players,cardset):
    # Games are defined by number of players and the cardset
    # At present only My First Meal is supported
    
    print("New Game")
    
    self.box = []
    self.players = []
    self.cardset = cardset
    
    
    for i in range(players):
      #TODO: add support for Real (Named) vs AI
      #Value Checking on player count
      self.players.append(Player(i))
    
    print("Using Cardset:", end = "")
    print(self.cardset)
    
    
       
    try:
        #This smells bad. Try a rewrite in order to get it looking better
        #self.newround(round = 1, direction = "Left", desserts = 3)
        self.makeDeck(self.cardset)
        self.newround(1,"Left",5)
        self.newround(2,"Right",3)
        self.newround(3,"Left",2)
        self.endGame()
    except ValueError:
        print("Terminating SushiPy")
  
    
    
  def newround(self, roundno , direction, desserts):
    print(f"Round {str(roundno)}")
      
    #Collect all cards (play areas should be clear of desserts)
    for i in self.players:
      self.box.extend(i.playArea)
      i.playArea = []
      
    # Add Desserts
    for i in range(desserts):
      self.box.append(SushiCard("Green Tea Ice Cream"))
    
    #Shuffle
    random.shuffle(self.box) 
    print("Dealing...")
    self.deal()
    
    for i in range(9):
      self.turn()
      self.passCards(direction)
  
    self.endRound()  
      
      
    
  def endGame(self):
    # Deals with Game Finish
    # Scores desserts, announces a winner
    # TODO: replay    
    print("GAME OVER!")
    
    # Score Ice Cream
    #TODO: Add other desserts
    for i in self.players:
        i.addPoints( math.floor(len(i.dessertStore)/4) * 12 ) 
        
    #Printout Scores
    results = []
    for i in self.players:
        results.append( (i.playerNo, i.points) )
    results.sort()
    for i in results:
        print(i)
    
    
  
  def makeDeck(self,cardset):
    #Creates the deck of cards for use in the game
    self.box = []
    if cardset == "My First Meal":
        for i in range(3):
          self.box.append(SushiCard("Squid Nigiri"))
          self.box.append(SushiCard("Maki Rolls", makival= 3))
          self.box.append(SushiCard("Wasabi"))
          self.box.append(SushiCard("Tea"))
          
        
        for i in range(4):
          self.box.append(SushiCard("Egg Nigiri"))
          self.box.append(SushiCard("Maki Rolls", makival= 1))
        
        
        for i in range(5):
          self.box.append(SushiCard("Salmon Nigiri"))
          self.box.append(SushiCard("Maki Rolls", makival= 2))
            
        for i in range(8):
          self.box.append(SushiCard("Tempura"))
          self.box.append(SushiCard("Sashimi"))
          self.box.append(SushiCard("Miso Soup"))
    else:
        print("I'm Sorry Your Cardset isn't currently supported, please select My First Meal")
        raise ValueError()


  def turn(self):
    
    print("Your Hand...")
    for i, j in enumerate(self.players[0].hand):
      print(i,": ",j)
    
    #Move all user input handling to other function?
    while True:
      try:
        answer = input("What card would you like to play?\n")
        #Valid Answer
        choice1 = int(answer)
        self.players[0].playCard(choice1)
      except:
        if answer.lower() == "quit":
            raise ValueError()
        print("Try Again or type Quit to exit")
        continue
      else:
        break
    
    for i in self.players:
      if i.playerNo != 0:
        i.playCard(0)
    
    
    
    #Miso Soup Check:
    misoCount = 0
    for i in self.players:
      #print(i.playArea[-1:])
      if list(i.playArea[-1:])[0].sushiName == "Miso Soup":
        misoCount += 1
    #print(misoCount)
    if misoCount > 1:
      print("Too Much Miso Soup! All who played Miso Soup lose their Cards")
      for i in self.players:
        if list(i.playArea[-1:])[0].sushiName== "Miso Soup":
          i.playArea.pop()
    
    
    print("Your Board...")
    print(self.players[0].playArea,"\n")
  
  def globalScore(self):
    #Scores Maki Rolls
    high = 0
    secondhigh = 0
    
    for i in self.players:
      a = i.playAreaMakiVal()
      if a > high:
        secondhigh = high
        high = a
      elif a > secondhigh and a != high:
        secondhigh = a
    #print("high=",high," secondhigh=",secondhigh)
    for i in self.players:
      if high > 0 and i.playAreaMakiVal() == high:
        i.addPoints(6)
      if secondhigh > 0 and i.playAreaMakiVal() == secondhigh:
        i.addPoints(3)
    

  def endRound(self):
    #Score Points
    
  
    #Move Desserts
    for i in self.players:
      i.scorePlayArea()
      
    self.globalScore()
    
    
    for i in self.players:
      print("Player ",i.playerNo, " is on ",i.points," points.")
      print(i.storeDesserts())
      print(i.playArea, i.dessertStore)
      
    
  
    


  def passCards(self,direction):
    if direction == "Left":
      bhand = self.players[0].hand
      for i in self.players[::-1]:
        ahand = i.hand
        i.hand = bhand
        bhand = ahand
    if direction == "Right":
      bhand = self.players[len(self.players)-1].hand
      for i in self.players:
        ahand = i.hand
        i.hand = bhand
        bhand = ahand
  
  
  def deal(self):
    for i in self.players:
      for j in range(9):
        i.addHand(self.box.pop(0))
        
      
    

class Player:
  #A player consists of a seat number, points, a hand, a play area and a dessert store
  
  
  def __init__(self,number):
    self.playerNo = number
    self.hand = []
    self.points = 0
    self.playArea = []
    self.dessertStore = []
    
  def addPoints(self, number):
    self.points += number
  
  def scorePlayArea(self):
    # Scores a round of SushiGo
    # Does not clear the play area
    
    points = 0
    tempuraCount = 0
    sashimiCount =0
    
    #All Nigiri, Tempura and Sashimi
    for i in self.playArea:
      if i.isCard("Egg Nigiri"):
        points+=1
      elif i.isCard("Salmon Nigiri"):
        points+=2
      elif i.isCard("Squid Nigiri"):
        points+=3
      elif i.isCard("Miso Soup"):
        points+=3
      elif i.isCard("Tempura"):
        tempuraCount+=1
      elif i.isCard("Sashimi"):
        sashimiCount+=1
      
    #Tempura and Sashimi points rely on sets
    points += math.floor(tempuraCount/2)*5
    points += math.floor(sashimiCount/3)*10
    
    
    #Wasabi uses card order
    wasabiCount = 0
    for i in self.playArea:
      if i.sushiName == "Wasabi":
        wasabiCount += 1
      if wasabiCount > 0 and i.sushiType == "Nigiri":
        if i.sushiName == "Egg Nigiri":
          points+=2
          wasabiCount-=1
        elif i.sushiName == "Salmon Nigiri":
          points+=4
          wasabiCount-=1
        elif i.sushiName == "Squid Nigiri":
          points+=6
          wasabiCount-=1
    
    
    #Tea relys on card colours, these are all different except nigiri/wasabi
    #teaList is the playArea but made with colours
    teaList = []
    
    for i in self.playArea:
      if i.sushiType == "Nigiri" or i.sushiName == "Wasabi":
        teaList.append('Yellow')
      else:
        teaList.append(i.sushiName)
    
    #Function found online to group the list
    teaScore = 0
    for a,b in g(sorted(teaList)):
      x = sum(1 for _ in b)
      if x > teaScore:
        teaScore = x
        #print(teaScore)
    for i in self.playArea:
      if i.sushiName == "Tea":
        points+=teaScore
    
       
    #Maki Rolls are scored at a global level
    

    #Points total is added to players score    
    self.addPoints(points)
    
  def playAreaMakiVal(self):
    #Function used by global scoring to assess Maki roll values
    makiSum = 0
    for i in self.playArea:
      if i.sushiName == "Maki Rolls":
        makiSum += i.sushiVal 
    return makiSum
    
    
  def playCard(self,cardNo):
    #When a player plays a card it is moved from their hand into their play area
    self.playArea.append(self.hand.pop(int(cardNo)))
  
  def storeDesserts(self):
    #Desserts persist through rounds, so we need to make sure to keep them to one side
    #We return the count of desserts stored
    dessertCount = 0
    loop = reversed(list(enumerate(self.playArea)))
    for n,i in loop:
      if i.sushiType == "Desserts":
        self.dessertStore.append(self.playArea.pop(n))
        dessertCount +=1
    return dessertCount
   
  def addHand(self,card):
    #Adds a card to hand, when dealing
    self.hand.append(card)    
        
  def __repr__(self):
    #Printing a player gives their score
    return ("Player "+str(self.playerNo)+": "+str(self.points)+" points")







class SushiCard:
#Defines a single SushiGo Card
#A card is defined by its name, and in the case of Maki its value

  def __init__(self,cname,makival=0):
    self.sushiName = cname
    self.sushiVal = makival

    if self.sushiName in ("Squid Nigiri","Egg Nigiri","Salmon Nigiri"):
      self.sushiType = "Nigiri"  
    elif self.sushiName in ("Maki Rolls","Temaki","Uramaki"):
      self.sushiType = "Maki Rolls"
    elif self.sushiName in ("Tempura","Sashimi","Dumpling","Eel","Tofu","Onigiri","Edemame","Miso Soup"):
      self.sushiType = "Appetizers"
    elif self.sushiName in ("Chopsticks","Soy Sauce", "Tea", "Menu", "Spoon", "Special Order", "Takeout Box", "Wasabi"):
      self.sushiType = "Specials"
    elif self.sushiName in ("Pudding", "Green Tea Ice Cream", "Fruit"):
      self.sushiType = "Desserts"
    else:
      self.sushiType = "Unknown"

  def isCard(self,name):
    #Checks if an instance of a card matches a name
    if self.sushiName == name:
      return True
    else:
      return False
    
    
  
  def __repr__(self):
    #Print method, usually card name
    if self.sushiVal>0:
      return self.sushiName+" ("+str(self.sushiVal)+")"
    return self.sushiName
    
  

    
    





def main():
  SushiPy(4,"My First Meal")
  
  
if __name__  ==  "__main__":
  main()
  











