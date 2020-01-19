# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 15:42:42 2015

@author: tfleck
"""

import Dominion
import random
import testUtility
from collections import defaultdict

#Get player names
player_names = ["Annie","*Ben","*Carla"]

(nV, nC) = testUtility.get_n_cards(player_names)

box = testUtility.get_boxes(nV)

supply_order = testUtility.get_supply_order()

#Pick 10 cards from box to be in the supply.
supply = testUtility.pick_supply(box)


#The supply always has these cards
supply["Copper"]=[Dominion.Copper()]*(60-len(player_names)*7)
supply["Silver"]=[Dominion.Silver()]*40
supply["Gold"]=[Dominion.Gold()]*30
supply["Estate"]=[Dominion.Estate()]*nV
supply["Duchy"]=[Dominion.Duchy()]*nV
supply["Province"]=[Dominion.Province()]*nV
supply["Curse"]=[Dominion.Curse()]*nC

#initialize the trash
trash = []

#Costruct the Player objects
players = []
for name in player_names:
    if name[0]=="*":
        players.append(Dominion.ComputerPlayer(name[1:]))
    elif name[0]=="^":
        players.append(Dominion.TablePlayer(name[1:]))
    else:
        players.append(Dominion.Player(name))

#Play the game
turn  = 0
while not Dominion.gameover(supply):
    turn += 1    
    print("\r")    
    for value in supply_order:
        print (value)
        for stack in supply_order[value]:
            if stack in supply:
                print (stack, len(supply[stack]))
    print("\r")
    for player in players:
        print (player.name,player.calcpoints())
    print ("\rStart of turn " + str(turn))    
    for player in players:
        if not Dominion.gameover(supply):
            print("\r")
            player.turn(players,supply,trash)
            

#Final score
dcs=Dominion.cardsummaries(players)
vp=dcs.loc['VICTORY POINTS']
vpmax=vp.max()
winners=[]
for i in vp.index:
    if vp.loc[i]==vpmax:
        winners.append(i)
if len(winners)>1:
    winstring= ' and '.join(winners) + ' win!'
else:
    winstring = ' '.join([winners[0],'wins!'])

print("\nGAME OVER!!!\n"+winstring+"\n")
print(dcs)
