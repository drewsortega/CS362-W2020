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
    def test_action_balance(self):
        self.fail()

    def test_calcpoints(self):
        self.fail()

    def test_draw(self):
        self.fail()

    def test_cardsummary(self):
        self.fail()


class TestGame(TestCase):
    def test_gameover(self):
        self.fail()
