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
player_names = ["Drew","Jacob"]

(nV, nC) = testUtility.get_n_cards(player_names)

box = testUtility.get_boxes(nV)

# generate supply order
supply_order = testUtility.get_supply_order()

#Pick 10 cards from box to be in the supply.
supply = testUtility.pick_supply(box, [])

# since supply is a list -> therefore a reference, does not
# need to return anything!

# this is where the bug is located in this test scenario -
# we "accidentally" pass in box instead of supply to the 
# function. The game doesn't crash, but it immediately ends.
# this is because we don't add any of these required cards
# into the actual supply, and then there is zero victory cards
# in at least one of the piles by the game rules (really zero
# in all of them), so it immediately ends. But it does not crash.
testUtility.add_base_cards(box, player_names, nV, nC)

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
