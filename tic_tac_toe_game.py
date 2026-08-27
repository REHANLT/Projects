def print_board(board):
    """Displays the 3x3 Tic Tac Toe board."""
    print("\n")
    for row in range(3):
        print(f" {board[row][0]} | {board[row][1]} | {board[row][2]} ")
        if row < 2:
            print("---|---|---")
    print("\n")


def check_win(board, player):
    """Checks rows, columns, and diagonals for a win."""
    # Check rows and columns
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or \
           all(board[j][i] == player for j in range(3)):
            return True

    # Check diagonals
    if (board[0][0] == player and board[1][1] == player and board[2][2] == player) or \
       (board[0][2] == player and board[1][1] == player and board[2][0] == player):
        return True

    return False


def check_tie(board):
    """Checks if the board is completely full (tie game)."""
    for row in board:
        if " " in row:
            return False
    return True


def play_game():
    """Main function to control turns and game loop."""
    while True:
        # Step 1: Initialize 3x3 grid
        board = [[" " for _ in range(3)] for _ in range(3)]
        current_player = "X"
        game_over = False

        print("--- Welcome to Tic Tac Toe ---")
        print("Positions are specified by Row (1-3) and Column (1-3).")

        while not game_over:
            # Step 2: Display board
            print_board(board)

            # Step 3: Player input
            print(f"Player {current_player}'s turn.")
            try:
                row = int(input("Enter row (1-3): ")) - 1
                col = int(input("Enter column (1-3): ")) - 1

                # Validate position range
                if row not in range(3) or col not in range(3):
                    print("Invalid position! Row and column must be between 1 and 3.")
                    continue

                # Check if spot is open
                if board[row][col] != " ":
                    print("That space is already taken! Try again.")
                    continue

            except ValueError:
                print("Invalid input! Please enter numbers (1-3).")
                continue

            # Mark board
            board[row][col] = current_player

            # Step 4: Check win or tie
            if check_win(board, current_player):
                print_board(board)
                print(f"🎉 Player {current_player} wins!")
                game_over = True
            elif check_tie(board):
                print_board(board)
                print("🤝 It's a tie!")
                game_over = True
            else:
                # Switch player turn
                current_player = "O" if current_player == "X" else "X"

        # Step 5: Ask to play again
        replay = input("Do you want to play again? (yes/no): ").strip().lower()
        if replay not in ("yes", "y"):
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    play_game()
