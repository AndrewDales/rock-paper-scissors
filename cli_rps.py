from game_objects import Game, PlayerObject, ComputerPlayer


# Command Line Interface - gives prompts to run the game from the Command line
class ClInterface:
    def __init__(self):
        self.game = Game()
        # Convert to plain Rock, Paper, Scissors by uncommenting next 3 lines
        # ToDo Give the user an option to choose this
        # allowable_objects = ('rock', 'paper', 'scissors')
        # win_dict = {'rock': ['scissors'], 'scissors': ['paper'], 'paper': ['rock']}
        # self.game = Game(allowable_objects, win_dict)

    def set_up(self):
        objects = PlayerObject.allowable_objects
        wel_string = f"Welcome to the {', '.join([obj.title() for obj in objects])} Game"
        print(wel_string)
        print("-" * len(wel_string))

        for i in range(2):
            player_type_chosen = False
            while not player_type_chosen:
                player_type = input(f"\nWill player {i} be a human (h) or the computer (c): ")
                if player_type[0].lower() == "h":
                    name = input("\nEnter Player's name: ")
                    self.game.add_human_player(name)
                    player_type_chosen = True
                elif player_type[0].lower() == "c":
                    self.game.add_computer_player()
                    player_type_chosen = True
                else:
                    print("Error - please enter 'h' or 'c'")
        self.input_max_rounds()

    def input_max_rounds(self):
        self.game.set_max_rounds(int(input("How many rounds will you play: ")))

    def get_choices(self):
        for player in self.game.players:
            while player.current_object is None:
                try:
                    if isinstance(player, ComputerPlayer):
                        player.choose_object()
                    else:
                        object_list = [f"'{obj}'" for obj in PlayerObject.allowable_objects]
                        choice = input(f"{player.name} please choose "
                                       f"{', '.join(object_list[:-1])} or {object_list[-1]}: ")
                        player.choose_object(choice)
                except ValueError as e:
                    print(e)

    def run_game(self):

        while not self.game.is_finished():
            self.game.next_round()
            self.get_choices()
            self.game.find_winner()
            print()
            print(self.game.report_round())
            print()
            print(self.game.report_score())
            print()

        print("Final Results")
        print("-" * 13)
        print(self.game.report_score())
        print()
        print(self.game.report_winner())

    def run_sequence(self):
        self.set_up()
        cont_seq = True
        while cont_seq:
            self.run_game()
            print("Would you like to play again (y/n)? ")
            play_again = input()
            if play_again[0].lower() == "y":
                self.input_max_rounds()
                self.game.reset()
            else:
                cont_seq = False
        print("Goodbye!")


if __name__ == "__main__":
    cli = ClInterface()
    cli.run_sequence()
