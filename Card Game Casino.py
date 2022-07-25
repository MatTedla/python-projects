from typing import Dict, List, Tuple, Union, Optional, Any
from random import choice, sample


class Blackjack:

    def __init__(self, deck: List):
        """
        :param deck: Deck of cards to play blackjack with
        """
        self.deck: List = deck
        self.rules: str = "\nWelcome to blackjack! You can choose to keep drawing cards until you either: reach 21 and " \
                          "win, go over 21 and lose, or chose to stay.\nIf you choose to stay and the next card is " \
                          "over 21, you win; if the next card is 21 or under 21, you lose.\n"
        self.value_list: List = []
        self.value_list_length: int = len(self.value_list)
        self.removed_cards_list: List = []

    def __repr__(self) -> str:
        return self.rules

    def draw_card(self):
        new_card: str = choice(self.deck)
        self.making_list_of_removed_cards(new_card)
        print(f"{new_card}")
        return new_card

    def making_list_of_removed_cards(self, removed_card: str):
        """
        :param removed_card: card that has been removed from deck
        """
        index: int = self.deck.index(removed_card)
        del self.deck[index]

        self.removed_cards_list.append(removed_card)

    def add_card_value_to_list(self):
        value_added: bool = False
        new_card: str = self.draw_card()
        for i in range(2, 10):
            if str(i) in new_card:
                self.value_list.append(i)
                value_added = True

        if value_added is False:
            if "Ace" in new_card:
                self.decide_ace_value()
            else:
                self.value_list.append(10)

    def decide_ace_value(self):
        decision: str = input("Do you want Ace to be worth 1 or 11? ")
        error_prompt: str = "Value must be 1 or 11"
        while True:
            try:
                if int(decision) == 1:
                    self.value_list.append(1)
                    break
                elif int(decision) == 11:
                    self.value_list.append(11)
                    break
                else:
                    print(error_prompt)
            except TypeError:
                print(error_prompt)

    def reset_class_variables(self):
        self.value_list.clear()
        self.value_list_length: int = len(self.value_list)
        self.removed_cards_list.clear()

    def play(self):
        while True:
            self.add_card_value_to_list()
            total: int = 0
            for item in self.value_list:
                total += item
            print(f"You're total is {total}.\n")

            if total > 21:
                print("You lose!")
                break
            elif total == 21:
                print("You win!")
                break
            else:
                hit: str

                while True:
                    hit = input("Would you like to hit? 'Y' for yes, 'N' for no. ")
                    if hit == 'Y' or hit == 'y' or hit == 'N' or hit == 'n':
                        break
                    else:
                        print("Input must be 'Y' or 'N")

                if hit == 'Y' or hit == 'y':
                    continue
                else:
                    self.add_card_value_to_list()
                    total += self.value_list[-1]
                    print(f"You're total is {total}.\n")

                    if total > 21:
                        print("You win!")
                        break
                    else:
                        print("You lose!")
                        break


class Poker:
    def __init__(self, deck: List):
        """
        :param deck: Deck of cards to play blackjack with
        """
        self.deck: List = deck
        self.rules: str = "Welcome to Poker! You can choose to between basic 5 card poker or Texas Holdem.\n\n"
        self.cards_in_play: List = []
        self.removed_cards_list: List = []
        self.suite_count: List[int, int, int, int] = [0, 0, 0, 0]
        self.straight: int = 0
        self.flush: bool = False
        # First cell is number of 2s in hand, last is number of Aces in hand
        self.num_count: List[int, int, int, int, int, int, int, int, int, int, int, int, int] = [0, 0, 0, 0, 0, 0, 0, 0,
                                                                                                 0, 0, 0, 0, 0]

    def __repr__(self):
        return self.rules

    def dealt_cards(self, num_dealt: int):
        """
        :param num_dealt: The number of cards to be drawn from the deck
        :return: A list of cards drawn from the deck
        """
        dealt_cards: List = sample(self.deck, num_dealt)
        self.making_list_of_removed_cards(dealt_cards)

        for card in dealt_cards:
            self.cards_in_play.append(card)
        self.display_cards(num_dealt)

    def making_list_of_removed_cards(self, removed_cards: List):
        """
        :param removed_cards: cards that have been removed from deck
        """
        for i in range(len(removed_cards)):
            if removed_cards[i] in self.deck:
                index: int = self.deck.index(removed_cards[i])
                del self.deck[index]
                self.removed_cards_list.append(removed_cards[i])

    def display_cards(self, num_dealt):
        if num_dealt == 1:
            if len(self.cards_in_play) == 6:
                print("\nTurn")
            else:
                print("\nRiver")
            print(self.cards_in_play[-1])
        elif num_dealt == 3:
            print("\nFlop")
            for card in self.cards_in_play[-3:]:
                print(card)
        else:
            for card in self.cards_in_play:
                print(card)

    def counting_suites_and_nums_from_hand(self):
        # Looks at each card in hand one at a time
        for card in self.cards_in_play:
            # Counting suites
            if 'Diamonds' in card:
                self.suite_count[0] += 1
            elif 'Hearts' in card:
                self.suite_count[1] += 1
            elif 'Spades' in card:
                self.suite_count[2] += 1
            else:
                self.suite_count[3] += 1

            # Counting faces and numbers
            if 'Jack' in card:
                self.num_count[-4] += 1
            elif 'Queen' in card:
                self.num_count[-3] += 1
            elif 'King' in card:
                self.num_count[-2] += 1
            elif 'Ace' in card:
                self.num_count[-1] += 1
            else:
                # Checks for each possible number a card could contain
                # If one found it will be added to count total, then break to look at next card
                for j in range(2, 11):
                    if str(j) in card:
                        # Range starts at 2, so subtract 2 from j to refer to corresponding index
                        self.num_count[j - 2] += 1
                        break
                    else:
                        continue

    def checking_straights_and_flushes(self):
        # Checking flush
        if 5 in self.suite_count or 6 in self.suite_count or 7 in self.suite_count:
            self.flush = True

        # For checking sequence / straights
        for k in range(13):
            # Counts 2 through Ace
            if self.num_count[k] > 0:
                self.straight += 1
            # Breaks only if a sequence of numbers not found (there must be at least three numbers found before
            # breaking), takes into account Texas Holdem since seven cards can be considered
            else:
                if self.straight > 2:
                    break
                elif self.straight > 1 and len(self.cards_in_play) == 6:
                    break
                elif self.straight > 0 and len(self.cards_in_play) == 5:
                    break
                else:
                    continue

    def returning_poker_rank(self) -> int:
        # Returning the grade
        if self.flush is True:
            if self.straight == 5 and len(self.cards_in_play) == 5 or self.straight == 6 and \
                    len(self.cards_in_play) == 6 or self.straight == 7 and len(self.cards_in_play) == 7:
                # Checking whether there's an Ace in a straight guarantees it's a Royal
                if self.num_count[-1] == 1:
                    return 1
                # Straight Flush
                else:
                    return 2

        # Sorts number from biggest to smallest
        self.num_count.sort(reverse=True)

        # Four of a Kind
        if self.num_count[0] == 4:
            return 3

        # Full House and Three of a Kind
        # Since this is 5 card hand, if first number 3, then second must be 2 for a full house
        elif self.num_count[0] == 3:
            if self.num_count[1] == 2:
                return 4
            # In the event of a Three of a Kind with a hand of same suits
            elif self.flush is True:
                return 5
            else:
                return 7

        # Flush
        elif self.flush is True:
            return 5
        # Straight
        elif self.straight == 5 and len(self.cards_in_play) == 5 or self.straight == 6 and \
                len(self.cards_in_play) == 6 or self.straight == 7 and len(self.cards_in_play) == 7:
            return 6
        # Two Pair and One Pair
        elif self.num_count[0] == 2:
            if self.num_count[1] == 2:
                return 8
            else:
                return 9
        else:
            # High Card
            return 10

    def reset_class_variables(self):
        self.cards_in_play.clear()
        self.removed_cards_list.clear()
        self.suite_count.clear()
        self.suite_count = [0, 0, 0, 0]
        self.straight = 0
        self.flush = False
        self.num_count.clear()
        self.num_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


# Make hands then apply the functions above, for texas holdem ask the user if they'll stay before implementing the
# functions for the next card in the river
class BasicPoker(Poker):
    def __init__(self, deck: List):
        super().__init__(deck)
        self.rules: str = "\nWelcome to classic poker! In this game the dealer gives the player 5 cards.\n" \
                          "A poker rank is generated based on the cards in the player's hand.\n"

    def play(self):
        self.dealt_cards(5)
        self.counting_suites_and_nums_from_hand()
        self.checking_straights_and_flushes()
        print(f"\nRank {self.returning_poker_rank()} hand")

        self.reset_class_variables()


class TexasHoldem(Poker):
    def __init__(self, deck: List):
        super().__init__(deck)
        self.rules: str = "\nWelcome to Texas Holdem. In this game the dealer gives the player 2 cards, and reveals 3 " \
                          "cards from the deck.\nThe player can choose to fold or stay; if they stay another card will " \
                          "be revealed from deck.\nUp to 2 additional cards can be revealed from the deck - the poker " \
                          "rank is generated based on the cards from deck, alongside the cards in the hand.\n"

    def ask_user_permission(self, message) -> str:
        """
        :param message: prints out appropriate input message for user
        """
        while True:
            decision = input(f"\n{message} 'Y' for yes, 'N' for no. ")
            if decision == 'Y' or decision == 'y' or decision == 'N' or decision == 'n':
                return decision
            else:
                print("Input must be 'Y' or 'N")

    def play(self):
        self.dealt_cards(2)
        self.dealt_cards(3)

        confirm_turn: str = self.ask_user_permission("Would you like to see the next card from the deck? ")
        if confirm_turn == 'Y' or confirm_turn == 'y':
            self.dealt_cards(1)
            confirm_river: str = self.ask_user_permission("Would you like to see one final card from the deck? ")
            if confirm_river == 'Y' or confirm_river == 'y':
                self.dealt_cards(1)

        self.counting_suites_and_nums_from_hand()
        self.checking_straights_and_flushes()
        print(f"\nRank {self.returning_poker_rank()} hand")

        self.reset_class_variables()


def make_deck() -> List:
    suits = ['Diamonds', 'Hearts', 'Spades', 'Clubs']
    numbers = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    return [f"{number} of {suit}" for number in numbers for suit in suits]


def open_casino(deck: List[int]):
    print("Greetings! Welcome to my casino. What card game would you like to play?\n")
    my_game: Optional[Blackjack, BasicPoker, TexasHoldem]
    select: Optional[None, str] = None
    replay: str
    change_game: str

    while True:
        if not select:
            select = input("Please select from the following options.\n\tPress 1 for Blackjack, 2 for Classic Poker, or "
                           "3 for Texas Holdem: ")
        
        if select == "1":
            my_game = Blackjack(my_deck)
        elif select == "2":
            my_game = BasicPoker(my_deck)
        elif select == "3":
            my_game = TexasHoldem(my_deck)
        else:
            print("Try again.\n")
            select = None
            continue

        print(my_game)
        my_game.play()

        while True:
            replay = input("Would you like to play again: 'Y' for yes, 'N' for no.")
            if replay == "y" or replay == "Y":
                break
            elif replay == "n" or replay == "N":
                select = None
                break
            else:
                print("Try again!\n")

        if replay == "n" or replay == "N":
            change_game = input("Would you like to choose a different game: 'N' for No, Any other key for yes.")
            if change_game == "N" or change_game == "n":
                break
            else:
                continue

    print("\nThanks for playing in my casino!")


# preparing deck, opening the casino
my_deck = make_deck()
open_casino(my_deck)




