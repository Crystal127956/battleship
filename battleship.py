from colorama import Fore, Style
import random, sys


def display_welcome():
    # Print the welcome screen.
    print(Fore.CYAN + """
    ==========================
        Welcome to Battleship!
    ==========================
    """ + Style.RESET_ALL)
    print("Try to sink all the computer's ships before it sinks yours!")
    print("Let's begin!")


def select_difficulty():
    # Allow the player to select a difficulty level.
    print("Select a difficulty level:")
    print("1. Easy (5x5 board, 3 ships)")
    print("2. Medium (7x7 board, 5 ships)")
    print("3. Hard (10x10 board, 8 ships)")
    while True:
        choice = input("Enter your choice (1/2/3): ")
        if choice == "1":
            return 5, 3
        elif choice == "2":
            return 7, 5
        elif choice == "3":
            return 10, 8
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
    
    
def create_board(size):
    # Create an empty game board.
    return [["~" for _ in range(size)] for _ in range(size)]


def print_board(board, hide_ships=False):
    # Print the game board using different colors.
    cell_symbols = {
        "~": Fore.BLUE + "." + Style.RESET_ALL,  # Water
        "S": Fore.GREEN + "S" + Style.RESET_ALL,  # Ship
        "X": Fore.RED + "X" + Style.RESET_ALL,  # Hit
        "O": Fore.YELLOW + "O" + Style.RESET_ALL,  # Miss
    }
       
    print("  " + " ".join(str(i) for i in range(len(board))))
    for i, row in enumerate(board):
        row_display = [
            cell_symbols[cell] if cell != "S" or not hide_ships else cell_symbols["~"]
            for cell in row
        ]
        print(f"{i} " + " ".join(row_display))


def place_ships(board, ship_count, ship_length=1):
    # Randomly place ships on the board.
    size = len(board)
    for _ in range(ship_count):
        while True:
            orientation = random.choice(["horizontal", "vertical"])
            if orientation == "horizontal":
                row = random.randint(0, size - 1)
                col = random.randint(0, size - ship_length)
                if all(board[row][col + i] == "~" for i in range(ship_length)):
                    for i in range(ship_length):
                        board[row][col + i] = "S"
                    break
            else:  # Vertical
                row = random.randint(0, size - ship_length)
                col = random.randint(0, size - 1)
                if all(board[row + i][col] == "~" for i in range(ship_length)):
                    for i in range(ship_length):
                        board[row + i][col] = "S"
                    break


def get_computer_guess(board, guessed_cells):
    # Generate a valid guess for the computer.
    size = len(board)
    while True:
        row, col = random.randint(0, size - 1), random.randint(0, size - 1)
        if (row, col) not in guessed_cells:
            guessed_cells.add((row, col))
            return row, col
        

def get_player_guess(board):
    # Get a valid guess from the player.
    size = len(board)
    while True:
        try:
            guess = input("Enter your guess (row and column, e.g., 1 2): ").split()
            if len(guess) != 2:
                raise ValueError("Please enter two numbers separated by a space.")
            row, col = map(int, guess)
            if 0 <= row < size and 0 <= col < size and board[row][col] not in ["X", "O"]:
                return row, col
            print("Invalid guess. The cell is either out of range or already guessed. Try again.")
        except ValueError:
            print("Invalid input. Please enter two numbers separated by a space.")


def take_turn(board, is_player=True, guessed_cells=None):
    # Handles a turn for the player or computer.
    if is_player:
        row, col = get_player_guess(board)
    else:
        row, col = get_computer_guess(board, guessed_cells)
    hit = check_hit(board, row, col)
    if is_player:
        print("You hit a ship!" if hit else "You missed!")
    else:
        print(f"The computer hit your ship at ({row}, {col})!" if hit else f"The computer missed at ({row}, {col}).")
    return hit
    


def check_hit(board, row, col):
    # Check if the guess is a hit or a miss.
    board[row][col] = "X" if board[row][col] == "S" else "O"
    return board[row][col] == "X"


def count_remaining_ships(board):
    # Count the remaining ships on the board.
    return sum(row.count("S") for row in board)


def display_turn_summary(player_hits, computer_hits):
    # Display a summary of the current turn.
    print(Fore.CYAN + "\nTurn Summary:" + Style.RESET_ALL)
    print(f"Your hits: {player_hits}")
    print(f"Computer's hits: {computer_hits}")


def display_game_over(winner):
    # Display the game over screen.
    print(Fore.MAGENTA + "\n==========================" + Style.RESET_ALL)
    if winner == "player":
        print(Fore.GREEN + """
    ____    ____  ______    __    __     ____    __    ____  __  .__   __. 
    \   \  /   / /  __  \  |  |  |  |    \   \  /  \  /   / |  | |  \ |  | 
     \   \/   / |  |  |  | |  |  |  |     \   \/    \/   /  |  | |   \|  | 
      \_    _/  |  |  |  | |  |  |  |      \            /   |  | |  . `  | 
        |  |    |  `--'  | |  `--'  |       \    /\    /    |  | |  |\   | 
        |__|     \______/   \______/         \__/  \__/     |__| |__| \__| 
                                                                       """ + Style.RESET_ALL)
    else:
        print(Fore.RED + "Game over! The computer won!" + Style.RESET_ALL)
    print(Fore.MAGENTA + "==========================" + Style.RESET_ALL)


def battleship():
    while True:
        # Main function to play the Battleship game.
        display_welcome()
        size, ship_count = select_difficulty()
        print(f"Board size: {size}x{size}, Ships: {ship_count}")
    
        # Create boards
        player_board = create_board(size)
        computer_board = create_board(size)

        # Place ships
        place_ships(player_board, ship_count)
        place_ships(computer_board, ship_count)

        # Initialize hit counters.
        player_hits = 0
        computer_hits = 0

        # Initialize guessed cells for the computer
        computer_guessed_cells = set()

        # Computer's turn
        computer_hits += take_turn(player_board, is_player=False, guessed_cells=computer_guessed_cells)

        # Game loop
        while True:
            print("\nYour Board:")
            print_board(player_board)
            print("\nComputer's Board:")
            print_board(computer_board, hide_ships=True)
            
            # Player's turn
            player_hits += take_turn(computer_board, is_player=True)

            # Check if player wins
            if count_remaining_ships(computer_board) == 0:
                display_game_over("player")
                break

            # Check if computer wins
            if count_remaining_ships(player_board) == 0:
                display_game_over("computer")
                break

            # Display turn summary
            display_turn_summary(player_hits, computer_hits)

        # Ask to restart
        restart = input("Do you want to play again? (y/n): ").lower()
        if restart != "y":
            print("Thanks for playing! Goodbye!")
            sys.exit()


if __name__ == "__main__":
    battleship()
