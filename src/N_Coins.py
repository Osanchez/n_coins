import random as rand


class CoinGame:
    def __init__(self, coins_state, turn, personal_score, evil_score, parent):
        self.parent_state = parent
        self.coins = coins_state
        self.isYourTurn = turn
        self.personal_score = personal_score
        self.evil_score = evil_score

    def get_game(self):
        return self.coins

    def get_parent(self):
        return self.parent_state

    def get_personal_score(self):
        return self.personal_score

    def get_evil_score(self):
        return self.evil_score

    def check_winner(self):
        if len(self.coins) == 0 and self.personal_score > self.evil_score:
            return True, 1
        elif len(self.coins) == 0 and self.personal_score < self.evil_score:
            return True, -1
        elif len(self.coins) == 0 and self.personal_score == self.evil_score:
            return True, 0
        else:
            return False, 0

    def end_turn(self, points):
        if self.isYourTurn:
            self.personal_score += points
        else:
            self.evil_score += points

    def expand(self):
        if self.isYourTurn:
            left_copy = self.coins[:]
            right_copy = self.coins[:]

            left_choice = left_copy.pop(0)
            right_choice = right_copy.pop(len(self.coins) - 1)

            left = CoinGame(left_copy, self.isYourTurn, self.personal_score, self.evil_score, self)
            left.end_turn(left_choice)
            left.isYourTurn = not left.isYourTurn

            right = CoinGame(right_copy, self.isYourTurn, self.personal_score, self.evil_score, self)
            right.end_turn(right_choice)
            right.isYourTurn = not right.isYourTurn
            right.parent_state = self

            return [left, right]
        else:
            left_copy = self.coins[:]
            right_copy = self.coins[:]

            left_choice = left_copy.pop(0)
            right_choice = right_copy.pop(len(self.coins) - 1)

            if left_choice > right_choice:
                optimal = CoinGame(left_copy, self.isYourTurn, self.personal_score, self.evil_score, self)
                optimal.end_turn(left_choice)
                optimal.isYourTurn = not optimal.isYourTurn
            else:
                optimal = CoinGame(right_copy, self.isYourTurn, self.personal_score, self.evil_score, self)
                optimal.end_turn(right_choice)
                optimal.isYourTurn = not optimal.isYourTurn

            return [optimal]

    @staticmethod
    def print_optimal_moves(winning_board):
        print()
        optimal_moves = []
        current_board = winning_board
        while current_board.get_parent() is not None:
            current_board = current_board.get_parent()
            optimal_moves.append(str(current_board.get_game()) + " = " + str(current_board.get_personal_score()))

        optimal_moves.reverse()

        for move in optimal_moves:
            print(move)

    @staticmethod
    def get_max_game(winning_games):
        max_game = None
        score = 0
        for winning_game in winning_games:
            win_score = winning_game.get_personal_score()
            if win_score > score:
                max_game = winning_game
                score = win_score

        return max_game

    def maximize_score(self):
        initial = self.expand()
        winning_list = []
        open_list = []

        for node in initial:
            open_list.append(node)

        closed_list = []

        while len(open_list) > 0:
            current_child = open_list.pop(0)
            closed_list.append(current_child.get_game())
            if len(current_child.get_game()) > 0:
                expansion = current_child.expand()
                for child in expansion:
                    if child.check_winner()[0]:
                        if child.check_winner()[1] == 1:
                            winning_list.append(child)
                    else:
                        if child.get_game() not in closed_list:
                            open_list.append(child)

        maximum_score = self.get_max_game(winning_list)

        self.print_optimal_moves(maximum_score)


def main():
    number_turns = 2
    random_coin_state = []
    for x in range(2 * number_turns):
        random_number = rand.randint(0, 100)
        random_coin_state.append(random_number)

    game = CoinGame(random_coin_state, True, 0, 0, None)
    game.maximize_score()


if __name__ == "__main__":
    main()
