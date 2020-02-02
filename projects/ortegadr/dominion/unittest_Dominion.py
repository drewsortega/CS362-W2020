from unittest import TestCase
import Dominion
import testUtility


class TestAction_card(TestCase):
    def setUp(self):
        # Get player names
        self.player_names = ["Aryn", *"Bob", "*Courtney"]

        # ignore the correct way to get the number of
        # curse and victory cards
        (self.nV, self.nC) = testUtility.get_n_cards(self.player_names)

        self.box = testUtility.get_boxes(self.nV)

        # generate supply order
        self.supply_order = testUtility.get_supply_order()

        # Pick 10 cards from box to be in the supply.
        self.supply = testUtility.pick_supply(self.box, [])

        # since supply is a list -> therefore a reference, does not
        # need to return anything!
        testUtility.add_base_cards(
            self.supply, self.player_names, self.nV, self.nC)

        # initialize the trash
        self.trash = []

        # initialize players and hands
        self.players = testUtility.init_players(self.player_names)

    def test_init(self):
        self.setUp()

        # manually create the Laboratory class
        name = "Laboratory"
        cost = 5
        actions = 1
        cards = 2
        buys = 0
        coins = 0
        manual_card = Dominion.Action_card(
            name, cost, actions, cards, buys, coins)
        lab_card = Dominion.Laboratory()

        # verify that a locally initialized card is the same as a generated one
        self.assertEqual(manual_card.name, lab_card.name)
        self.assertEqual(manual_card.category, lab_card.category)
        self.assertEqual(manual_card.cost, lab_card.cost)
        self.assertEqual(manual_card.buypower, lab_card.buypower)
        self.assertEqual(manual_card.vpoints, lab_card.vpoints)
        self.assertEqual(manual_card.actions, lab_card.actions)
        self.assertEqual(manual_card.cards, lab_card.cards)
        self.assertEqual(manual_card.buys, lab_card.buys)
        self.assertEqual(manual_card.coins, lab_card.coins)

    def test_use(self):
        self.setUp()
        # generate an Action Card that could be played
        lab_card = Dominion.Laboratory()
        # get the first player from the list
        player = self.players[0]
        # add our lab card to their hand
        player.hand.append(lab_card)
        # use the lab card in the players hand
        lab_card.use(player, self.trash)
        # check to see if the lab card is now in their played hands, at the end of the list
        self.assertEqual(lab_card, player.played[-1])

    def test_augment(self):
        self.setUp()

        # use the first player
        player = self.players[0]

        # init player turn as if taking a turn
        player.actions = 1
        player.buys = 1
        player.purse = 0

        # store the old values
        old_actions = player.actions
        old_buys = player.buys
        old_purse = player.purse
        old_n_cards = len(player.hand)

        # the number everything should be incremented by
        inc_amount = 4

        # create a fake card that will augment everything by inc_amount
        card = Dominion.Action_card("fake_card", 1, inc_amount,
                                    inc_amount, inc_amount, inc_amount)

        # run augment
        card.augment(player)

        # check to see if actions correctly incremented
        self.assertEqual(player.actions, old_actions+inc_amount)

        # check to see if buys correctly incremented
        self.assertEqual(player.buys, old_buys+inc_amount)

        # check to see if the player purse is correctly incremented
        self.assertEqual(player.purse, old_purse+inc_amount)

        # check to see if the player drew the correct number of cards
        self.assertEqual(len(player.hand)-old_n_cards, inc_amount)


class TestPlayer(TestCase):
    def setUp(self):
        # Get player names
        self.player_names = ["Aryn", *"Bob", "*Courtney"]

        # ignore the correct way to get the number of
        # curse and victory cards
        (self.nV, self.nC) = testUtility.get_n_cards(self.player_names)

        self.box = testUtility.get_boxes(self.nV)

        # generate supply order
        self.supply_order = testUtility.get_supply_order()

        # Pick 10 cards from box to be in the supply.
        self.supply = testUtility.pick_supply(self.box, [])

        # since supply is a list -> therefore a reference, does not
        # need to return anything!
        testUtility.add_base_cards(
            self.supply, self.player_names, self.nV, self.nC)

        # initialize the trash
        self.trash = []

        # initialize players and hands
        self.players = testUtility.init_players(self.player_names)

    def test_action_balance(self):
        # set up
        self.setUp()
        player = self.players[0]
        print(len(player.stack()))
        # since there are no possible action cards, the total should be zero
        self.assertEqual(0, player.action_balance())
        # remove two cards from the hand
        player.hand = player.hand[2:]

        # add two real action cards
        player.hand.append(Dominion.Laboratory())
        player.hand.append(Dominion.Village())

        # hand-calculated value, compared
        self.assertEqual(7, player.action_balance())

    def test_calcpoints(self):
        # set up
        self.setUp()

        # get the first player
        player = self.players[0]

        # we start with 3 estate cards.
        self.assertEqual(player.calcpoints(), 3)

        # add an estate with 1 vic points
        player.hand.append(Dominion.Estate())
        
        self.assertEqual(player.calcpoints(), 4)

        # add a Duchy with 3 vic points
        player.hand.append(Dominion.Duchy())

        self.assertEqual(player.calcpoints(), 7)

        # add two garden. This is the 6th through 10th victory cards.
        # so we add (10/10)*5=5 to the total
        player.hand.append(Dominion.Gardens())
        player.hand.append(Dominion.Gardens())
        player.hand.append(Dominion.Gardens())
        player.hand.append(Dominion.Gardens())
        player.hand.append(Dominion.Gardens())

        self.assertEqual(player.calcpoints(), 12)

    def test_draw(self):
        # set up
        self.setUp()

        # get a player
        player = self.players[0]

        # store hand size
        old_size = len(player.hand)

        # draw a card
        player.draw()

        # check to see if we have another card in the hand
        self.assertEqual(len(player.hand), old_size+1)

        d_size = len(player.deck)
        # discard the entire deck
        player.discard = player.deck[:]
        player.deck = []

        # ensure the deck is empty
        self.assertEqual(len(player.deck), 0)

        # shuffles discard into deck
        player.draw()

        # check to see we drew card and deck was restored
        self.assertEqual(len(player.hand), old_size+2)
        self.assertEqual(len(player.deck), d_size-1)


        

    def test_cardsummary(self):
        # set up
        self.setUp()

        # just use the first player
        player = self.players[0]


        summary = player.cardsummary()

        self.assertEqual(summary["Estate"], 3)
        self.assertEqual(summary["Copper"],7)
        self.assertEqual(summary["VICTORY POINTS"], 3)
        self.assertNotIn("Duchy", summary)

        # add an extra estate
        player.hand.append(Dominion.Estate())

        # also add a Duchy
        player.hand.append(Dominion.Duchy())

        summary = player.cardsummary()

        # should have more victory points
        self.assertEqual(summary["Estate"], 4)
        self.assertEqual(summary["Copper"],7)
        self.assertEqual(summary["Duchy"],1)
        self.assertEqual(summary["VICTORY POINTS"], 7)


class TestGame(TestCase):
    def test_gameover(self):
        # Get player names
        self.player_names = ["Aryn", *"Bob", "*Courtney"]

        # ignore the correct way to get the number of
        # curse and victory cards
        (self.nV, self.nC) = testUtility.get_n_cards(self.player_names)

        self.box = testUtility.get_boxes(self.nV)

        # generate supply order
        self.supply_order = testUtility.get_supply_order()

        #Pick 10 cards from box to be in the supply.
        self.supply = testUtility.pick_supply(self.box, [
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
        testUtility.add_base_cards(
            self.supply, self.player_names, self.nV, self.nC)

        # initialize the trash
        self.trash = []

        # initialize players and hands
        self.players = testUtility.init_players(self.player_names)

        # game should not be over since full provinces
        self.assertFalse(Dominion.gameover(self.supply))

        # clear all provinces as could eventually happen in game
        self.supply["Province"]=[]

        self.assertTrue(Dominion.gameover(self.supply))

        # add back the provinces so we test on something else

        self.supply["Province"]=[Dominion.Province()]
        self.assertFalse(Dominion.gameover(self.supply))
        
        # 1 "out", so not game over
        self.supply["Cellar"]=[]
        self.assertFalse(Dominion.gameover(self.supply))
        # 2 "out", so not game over
        self.supply["Market"]=[]
        self.assertFalse(Dominion.gameover(self.supply))
        # 3 "out", so must be game over
        self.supply["Milita"]=[]
        self.assertTrue(Dominion.gameover(self.supply))
