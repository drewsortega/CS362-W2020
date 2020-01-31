from unittest import TestCase
import Dominion
import testUtility


class TestAction_card(TestCase):
    def setUp(self):
        # Get player names
        player_names = ["Aryn", *"Bob", "*Courtney"]

        # ignore the correct way to get the number of
        # curse and victory cards
        (nV, nC) = testUtility.get_n_cards(player_names)

        # however, to introduce a bug, I override the number
        # of victory cards in play to 1.
        nV = 1

        box = testUtility.get_boxes(nV)

        # generate supply order
        supply_order = testUtility.get_supply_order()

        # Pick 10 cards from box to be in the supply.
        supply = testUtility.pick_supply(box, [])

        # since supply is a list -> therefore a reference, does not
        # need to return anything!
        testUtility.add_base_cards(supply, player_names, nV, nC)

        # initialize the trash
        trash = []

        # initialize players and hands
        players = testUtility.init_players(player_names)

    def test_init(self):
        self.setUp()
        name = "Laboratory"
        cost = 5
        actions = 1
        cards = 2
        buys = 0
        coins = 0
        manual_card = Dominion.Action_card(
            name, cost, actions, cards, buys, coins)
        lab_card = Dominion.Laboratory()

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
        self.fail()

    def test_augment(self):
        self.fail()


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
