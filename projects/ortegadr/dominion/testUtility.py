import Dominion
import random
from collections import defaultdict

# calculates number of cards based on the number of players
def get_n_cards(player_names):

    #number of curses and victory cards

    # nV = number of victory cards
    # nC = number of curse cards

    if len(player_names)>2:
        nV=12
    else:
        nV=8
    nC = -10 + 10 * len(player_names)
    return (nV, nC)

# gets the set of all cards
def get_boxes(nV):
    #define box
    box = {}
    box["Woodcutter"]=[Dominion.Woodcutter()]*10
    box["Smithy"]=[Dominion.Smithy()]*10
    box["Laboratory"]=[Dominion.Laboratory()]*10
    box["Village"]=[Dominion.Village()]*10
    box["Festival"]=[Dominion.Festival()]*10
    box["Market"]=[Dominion.Market()]*10
    box["Chancellor"]=[Dominion.Chancellor()]*10
    box["Workshop"]=[Dominion.Workshop()]*10
    box["Moneylender"]=[Dominion.Moneylender()]*10
    box["Chapel"]=[Dominion.Chapel()]*10
    box["Cellar"]=[Dominion.Cellar()]*10
    box["Remodel"]=[Dominion.Remodel()]*10
    box["Adventurer"]=[Dominion.Adventurer()]*10
    box["Feast"]=[Dominion.Feast()]*10
    box["Mine"]=[Dominion.Mine()]*10
    box["Library"]=[Dominion.Library()]*10
    box["Gardens"]=[Dominion.Gardens()]*nV
    box["Moat"]=[Dominion.Moat()]*10
    box["Council Room"]=[Dominion.Council_Room()]*10
    box["Witch"]=[Dominion.Witch()]*10
    box["Bureaucrat"]=[Dominion.Bureaucrat()]*10
    box["Militia"]=[Dominion.Militia()]*10
    box["Spy"]=[Dominion.Spy()]*10
    box["Thief"]=[Dominion.Thief()]*10
    box["Throne Room"]=[Dominion.Throne_Room()]*10

    return box

# defines the order of prices
def get_supply_order():
    supply_order = {0:['Curse','Copper'],
                    2:['Estate','Cellar','Chapel','Moat'],
                    3:['Silver','Chancellor','Village','Woodcutter','Workshop'],
                    4:['Gardens','Bureaucrat','Feast','Militia','Moneylender',
                        'Remodel','Smithy','Spy','Thief','Throne Room'],
                    5:['Duchy','Market','Council Room','Festival',
                        'Laboratory','Library','Mine','Witch'],
                    6:['Gold','Adventurer'],
                    8:['Province']}
    return supply_order

# picks from the cards to be in the list
def pick_supply(box, override):
    boxlist = [k for k in box]
    if override:
        supply = defaultdict(list,[(c,box[c]) for c in override])

        return supply
    else:
        #Pick 10 cards from box to be in the supply.
        random.shuffle(boxlist)
        random10 = boxlist[:10]
        supply = defaultdict(list,[(k,box[k]) for k in random10])

        return supply

# adds cards that must be used in every game
def add_base_cards(supply, player_names, nV, nC):
    #The supply always has these cards
    supply["Copper"]=[Dominion.Copper()]*(60-len(player_names)*7)
    supply["Silver"]=[Dominion.Silver()]*40
    supply["Gold"]=[Dominion.Gold()]*30
    supply["Estate"]=[Dominion.Estate()]*nV
    supply["Duchy"]=[Dominion.Duchy()]*nV
    supply["Province"]=[Dominion.Province()]*nV
    supply["Curse"]=[Dominion.Curse()]*nC

# initilizes player hands
def init_players(player_names):
    #Costruct the Player objects
    players = []
    for name in player_names:
        if name[0]=="*":
            players.append(Dominion.ComputerPlayer(name[1:]))
        elif name[0]=="^":
            players.append(Dominion.TablePlayer(name[1:]))
        else:
            players.append(Dominion.Player(name))

    return players
