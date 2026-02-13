import random
from enum import IntEnum


class GameAction(IntEnum):
    Rock = 0
    Paper = 1
    Scissors = 2
    Spock = 3
    Lizard = 4

    @classmethod
    def minus(cls, *actions):
        excluded = set(actions)
        return {a for a in cls if a not in excluded}


class GameResult(IntEnum):
    Victory = 0
    Defeat = 1
    Tie = 2


# user_action gana a estas  visto desde la posicion del usuarios
_WINS_AGAINST = {
    GameAction.Rock: {GameAction.Scissors, GameAction.Lizard},
    GameAction.Paper: {GameAction.Rock, GameAction.Spock},
    GameAction.Scissors: {GameAction.Paper, GameAction.Lizard},
    GameAction.Spock: {GameAction.Scissors, GameAction.Rock},
    GameAction.Lizard: {GameAction.Spock, GameAction.Paper},
}

# Mensajes (solo para consola) visto desde la posicion del usuarios
_WIN_MESSAGES = {
    (GameAction.Rock, GameAction.Scissors): "Rock crushes scissors.",
    (GameAction.Rock, GameAction.Lizard): "Rock crushes lizard.",
    (GameAction.Paper, GameAction.Rock): "Paper covers rock.",
    (GameAction.Paper, GameAction.Spock): "Paper disproves Spock.",
    (GameAction.Scissors, GameAction.Paper): "Scissors cuts paper.",
    (GameAction.Scissors, GameAction.Lizard): "Scissors decapitates lizard.",
    (GameAction.Spock, GameAction.Scissors): "Spock smashes scissors.",
    (GameAction.Spock, GameAction.Rock): "Spock vaporizes rock.",
    (GameAction.Lizard, GameAction.Spock): "Lizard poisons Spock.",
    (GameAction.Lizard, GameAction.Paper): "Lizard eats paper.",
}


class Game:
    def assess_game(self, user_action: GameAction, computer_action: GameAction) -> GameResult:
        if user_action == computer_action:
            return GameResult.Tie
        if computer_action in _WINS_AGAINST[user_action]:
            return GameResult.Victory
        return GameResult.Defeat

    def get_computer_action(self) -> GameAction:
        computer_action = random.choice(list(GameAction))
        print(f"Computer picked {computer_action.name}.")
        return computer_action

    def get_user_action(self) -> GameAction:
        choices = ", ".join(f"{a.name}[{a.value}]" for a in GameAction)
        raw = input(f"\nPick a choice ({choices}): ").strip()
        try: # evita romper valor no valido
            return GameAction(int(raw))
        except Exception:
            raise ValueError

    def play_another_round(self) -> bool:
        return input("\nAnother round? (y/n): ").strip().lower() == "y"

    def _print_console_result(self, user_action: GameAction, computer_action: GameAction, result: GameResult) -> None:
        if result == GameResult.Tie:
            print(f"User and computer picked {user_action.name}. Draw game!")
            return
        if result == GameResult.Victory:
            print(_WIN_MESSAGES[(user_action, computer_action)] + " You won!")
        else:
            print(_WIN_MESSAGES[(computer_action, user_action)] + " You lost!")

    def run_console(self) -> None:
        while True:
            try:
                user_action = self.get_user_action()
            except ValueError:
                print(f"Invalid selection. Pick a choice in range [0, {len(GameAction) - 1}]!")
                continue

            computer_action = self.get_computer_action()
            result = self.assess_game(user_action, computer_action)
            self._print_console_result(user_action, computer_action, result)

            if not self.play_another_round():
                break


def main():
    Game().run_console()


if __name__ == "__main__":
    main()