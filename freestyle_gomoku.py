# In this problem, you will implement two-player Freestyle Gomoku with the following specifications:
# a. The game must be implemented using only the Python standard library.
# b. The game must be able to be run from the command line/terminal. No frontend.
# c. The game must show the state and progression through ASCII graphics.
# d. Players must be able to keep playing without restarting the script.
# e. Players must be able to quit or give-up at any time.

# Use Flake8 to understand PEP 8
# Python Standard Library - https://docs.python.org/3.8/library/
# Ø

# rcmd on Windows search
# C:\Users\Mat T\Downloads\EnvAI Solutions Files\software_engineer_assignment\assignment_one
# idle freestyle_gomoku.py


# ********************************** FREESTYLE_GOMOKU **********************************#
from typing import Optional, List, Tuple, Dict, Union


class Board:
    def __init__(self):
        self.rules: str = "\nThis is freestyle gomoku! Place your coloured tiles " \
                          "at assigned coordinates on the game board.\nWinner " \
                          "is declared when a player is able to align five of " \
                          "their coloured tiles in a straight line - horizontal, " \
                          "vertical, or diagonal.\nPress R to give-up current " \
                          "game. Press Q to quit and shut down program.\n"

        self.available_coordinates: List[List[int]] = [[i, j] for i in range(15) for j in range(15)]
        self.player_coordinates: Dict[int, List[Optional[List[int]]]] = {1: [], 2: []}
        self.column_headers: List[str] = ["   0", "  1", "  2", "  3", "  4", "  5", "  6", "  7", "  8",
                                          "  9", "  10", " 11", " 12", " 13", " 14  "]

    def __repr__(self) -> str:
        return self.rules

    def display_board(self):
        """
        Draws 15x15 game board. Each column/row separated by three blank spaces.
        """

        # print column headers
        for header in self.column_headers:
            print(header, end="")
        print("")

        # iterate through all rows and row spaces of the board (vertically, top to bottom)
        for y_axis in range(30):
            # even numbers are where spaces and column lines are drawn
            if y_axis == 0 or y_axis % 2 == 0:
                for grid_space in range(49):
                    if grid_space % 3 == 0:
                        print("|", end="")
                    else:
                        print(" ", end="")
                print("")

            # odd numbers are where row headers, row lines, and coordinate indicators are drawn
            else:
                for x_axis in range(49):
                    # current coordinate will be checked against player coordinates so that appropriate symbol is drawn
                    current_coordinate: List[int] = [int(x_axis / 3) - 1, int(y_axis / 2)]

                    if x_axis == 0:
                        print(int(y_axis / 2), end="")

                    elif x_axis % 3 == 0:
                        if current_coordinate in self.player_coordinates[1]:
                            print("O", end="")
                        elif current_coordinate in self.player_coordinates[2]:
                            print("X", end="")
                        else:
                            print("+", end="")
                    else:
                        # for spacing of row lines after 10th row
                        if y_axis > 20 and x_axis == 1:
                            continue
                        else:
                            print("-", end="")
                print("")

    def update_available_coordinates(self) -> List[List[int]]:
        """
        Lists coordinates available on the board.
    
        :return: updated list of available board spaces
        """

        if self.player_coordinates[1]:
            for i in self.player_coordinates[1]:
                if i in self.available_coordinates:
                    self.available_coordinates.remove(i)

        if self.player_coordinates[2]:
            for j in self.player_coordinates[2]:
                if j in self.available_coordinates:
                    self.available_coordinates.remove(j)

        return self.available_coordinates

    def check_gomoku_winner(self, player: int) -> Optional[Tuple[bool, int]]:
        """
        Indicates player with five in a row.

        :param player: the player whose tiles will be examined
        :return: boolean that indicates whether a winner has been found and, if True, who that winner is.
        """

        if self.player_coordinates[player]:
            for tile in self.player_coordinates[player]:
                # check vertical, horizontal, diagonal down-right and diagonal up-right 5 in a row
                try:
                    if ([tile[0], tile[1] + 1] in self.player_coordinates[player] and [tile[0], tile[1] + 2] in
                        self.player_coordinates[player] and [tile[0], tile[1] + 3] in self.player_coordinates[player]
                        and [tile[0], tile[1] + 4] in self.player_coordinates[player]) or (
                            [tile[0] + 1, tile[1]] in self.player_coordinates[player] and [tile[0] + 2, tile[1]] in
                            self.player_coordinates[player] and [tile[0] + 3, tile[1]] in self.player_coordinates[
                            player] and [tile[0] + 4, tile[1]] in self.player_coordinates[player]) or (
                            [tile[0] + 1, tile[1] + 1] in self.player_coordinates[player] and [tile[0] + 2, tile[1] + 2]
                            in self.player_coordinates[player] and [tile[0] + 3, tile[1] + 3] in
                            self.player_coordinates[player] and [tile[0] + 4, tile[1] + 4] in
                            self.player_coordinates[player]) or (
                            [tile[0] - 1, tile[1] + 1] in self.player_coordinates[player] and [tile[0] - 2, tile[1] + 2]
                            in self.player_coordinates[player] and [tile[0] - 3, tile[1] + 3] in
                            self.player_coordinates[player] and [tile[0] - 4, tile[1] + 4] in
                            self.player_coordinates[player]):
                        return True, player
                except IndexError:
                    continue

    def restart(self) -> bool:
        """
        Prompts player if they want restart the game."
        """

        while True:
            replay = input("\nWould you like to play again: 'Y' for yes, 'N' for no. ")
            if replay == "y" or replay == "Y":
                self.available_coordinates.extend(self.player_coordinates[1])
                self.available_coordinates.extend(self.player_coordinates[2])
                self.player_coordinates[1].clear()
                self.player_coordinates[2].clear()

                return True
            elif replay == "n" or replay == "N":
                return False
            else:
                print("\nTry again...")

    def play_gomoku(self):
        """
        Uses board to start a game of 2-Player Freestyle Gomoku.
        """
        # establish players and turn number
        player_1: Player = Player(1)
        player_2: Player = Player(2)
        turn: int = 1
        p: Player
        game_quit: bool = False

        while True:
            while True:
                # display board
                self.display_board()

                # state rules at start of game
                if turn == 1:
                    # state rules of game
                    print(self.rules)

                # cycles between players depending on turn number; odd turns - Player 1, even turns - Player 2
                if turn % 2 != 0:
                    p = player_1
                else:
                    p = player_2
                print(p)

                # player gives input
                choice = p.choose_space(self.available_coordinates)

                # confirm outcome based on player's input (restart, quit, or place a tile)
                if choice == "R":
                    print(f"\nPlayer {p.turn_player} has given up. Your opponent wins!!! ")
                    break
                elif choice == "Q":
                    game_quit = True
                    break
                else:
                    self.player_coordinates[p.turn_player].append(choice)

                # check for winner when a player has minimum 5 tiles on the board
                if turn > 8:
                    winner = self.check_gomoku_winner(p.turn_player)
                    if winner:
                        self.display_board()
                        print(f"\nPlayer {p.turn_player} wins!!!\n")
                        break

                # update available spaces on board and turn number
                self.available_coordinates = self.update_available_coordinates()
                turn += 1

                # Exits if there are no board spaces available
                if not self.available_coordinates:
                    print("\nNo more spaces available!\n")
                    break

            # current game has finished; prompts for a new game of Gomoku
            if not game_quit:
                if self.restart():
                    turn = 1
                    continue

            # shuts down game when player quits
            print("\nThank you for playing freestyle gomoku!\n")
            break


class Player:
    def __init__(self, turn_player: int):
        self.turn_player = turn_player

    def __repr__(self):
        return f"Player {self.turn_player}'s turn.\n"

    def choose_space(self, spaces: List[List[int]]) -> Union[str, List[int]]:
        """
        Prompts turn player for board coordinates onto which their tile will be placed.

        :param spaces: coordinates on the board that don't have a tile on them
        :return: player's choice of coordinate
        """
        while True:
            choice_str: str = input("\nSelect column and row, separated by space: ")

            # confirms give up or quit prompt
            if choice_str == "R" or choice_str == "Q":
                if self.confirm_giveup_or_quit(choice_str):
                    return choice_str
                else:
                    continue

            # other prompt edge cases
            choice_str_list: List[str] = choice_str.split()
            try:
                choice: List[int] = [int(i) for i in choice_str_list]

                if len(choice) != 2:
                    print("\nYou must specify two coordinates.")
                elif choice[0] not in range(15) or choice[1] not in range(15):
                    print("\nIntegers must be between 0-14 inclusive.")
                elif choice not in spaces:
                    print("\nSpace already has a tile. Try again!")
                else:
                    return choice
            except ValueError:
                print("\nCoordinates must be integers between 0-14.")


    def confirm_giveup_or_quit(self, choice: str) -> bool:
        """
        Player confirms their choice of giving-up or quitting

        :param choice: player input that raises give-up or quit prompt
        :return: bool that confirms whether player has given up current game or has quit playing Gomoku
        """

        # Check for give-up and quit input
        if choice == "R":
            give_up: str = input("\nAre you sure you want to give up current game? Y for yes, any other key for No.")
            if give_up == "Y" or give_up == "y":
                return True
            else:
                return False

        if choice == "Q":
            game_quit: str = input("\nAre you sure you want to quit Gomoku? Y for yes, any other key for No.")
            if game_quit == "Y" or game_quit == "y":
                return True
            else:
                return False


def main():
    my_board = Board()
    my_board.play_gomoku()

if __name__ == '__main__':
    main()



