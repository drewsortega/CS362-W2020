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
player_names = ["Aryn","*Bob","*Courtney"]

# ignore the correct way to get the number of 
# curse and victory cards
#(nV, nC) = testUtility.get_n_cards(player_names)
# set the number of curse and victory cards manually:
nV = 1
nC = 400


box = testUtility.get_boxes(nV)

# generate supply order
supply_order = testUtility.get_supply_order()

#Pick 10 cards from box to be in the supply.
supply = testUtility.pick_supply(box, [
    "Cellar",
    "Market",
    "Militia",
    "Mine",
    "Moat",
    "Remodel",
    "Smithy",
    "Village",
    "Woodcutter",
    "Workshop"
    ])

# since supply is a list -> therefore a reference, does not
# need to return anything!
testUtility.add_base_cards(supply, player_names, nV, nC)

#initialize the trash
trash = []

# initialize players and hands
players = testUtility.init_players(player_names)

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
