# Tic-Tac-Toe game with AI opponent using Minimax algorithm

def print_board(board):
    """Display the Tic-Tac-Toe board."""
    # Iterate through each row of the board
    for row in board:
        # Join cells in the row with ' | ' for visual separation
        print(" | ".join(row))
        # Print a horizontal line to separate rows
        print("-" * 9)

def check_winner(board, player):
    """Check if the specified player has won."""
    # Check rows for a win
    for row in board:
        if all(cell == player for cell in row):
            return True
    # Check columns for a win
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    # Check main diagonals (top-left to bottom-right)
    if all(board[i][i] == player for i in range(3)):
        return True
    # Check anti-diagonal (top-right to bottom-left)
    if all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_board_full(board):
    """Check if the board is full (tie game)."""
    # Checking for no empty cells 
    return all(cell != " " for row in board for cell in row)

def get_empty_cells(board):
    """Return a list of empty cell coordinates."""
    # It returns a list of (row,col) tuples for empty cells 
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]

def minimax(board, depth, is_maximizing):
    """Minimax algorithm to determine the best move for AI."""
    if check_winner(board, "O"):  # AI wins
        return 10 - depth 
    if check_winner(board, "X"):  # Human wins
        return depth - 10
    if is_board_full(board):  # Tie
        return 0

    if is_maximizing:
        # AI's turn to maximize score 
        best_score = -float("inf")
        # Try each empty cell
        for i, j in get_empty_cells(board):
            board[i][j] = "O" # Simulate AI move
            score = minimax(board, depth + 1, False)
            board[i][j] = " " # Undo move
            best_score = max(score, best_score) # Update best score 
        return best_score
    else:
        # Human's turn to minimize score 
        best_score = float("inf")
        # Try each emopty cell 
        for i, j in get_empty_cells(board):
            board[i][j] = "X" # Simulate human move 
            score = minimax(board, depth + 1, True)
            board[i][j] = " " # Undo move
            best_score = min(score, best_score) # Update best score 
        return best_score

def best_move(board):
    """Find the AI's best move using Minimax."""
    best_score = -float("inf") # Initialize best score 
    move = None # Initialize best move 
    # Evaluate each empty cell 
    for i, j in get_empty_cells(board):
        board[i][j] = "O" # Simulate AI move
        score = minimax(board, 0, False) # Get score from minimax
        board[i][j] = " " # Undo move
        if score > best_score:
            best_score = score # Update best score
            move = (i, j) # Update best move 
    return move

def main():
    """Main game loop."""
    # Initialize 3x3 board with empty spaceds
    board = [[" " for _ in range(3)] for _ in range(3)]
    print("Welcome to Tic-Tac-Toe! You are 'X', AI is 'O'.")
    print("Enter row (0-2) and column (0-2) for your move (e.g., '1 1').")

    while True:
        # Human player's turn
        print_board(board) # Display currrent board
        try:
            # Get human move input
            row, col = map(int, input("Your move (row col): ").split())
            # Validate move
            if 0 <= row <= 2 and 0 <= col <= 2 and board[row][col] == " ":
                board[row][col] = "X" # Place human's mark 
            else:
                print("Invalid move. Cell is taken or out of bounds. Try again.")
                continue
        except ValueError:
            print("Invalid input. Enter two numbers (0-2) separated by a space.")
            continue

        # Check if human wins
        if check_winner(board, "X"):
            print_board(board)
            print("Congratulations! You win!")
            break

        # Check for tie
        if is_board_full(board):
            print_board(board)
            print("It's a tie!")
            break

        # AI's turn
        print("AI is thinking...")
        move = best_move(board) # Get AI's best move 
        if move:
            board[move[0]][move[1]] = "O" # Place AI's mark 

        # Check if AI wins
        if check_winner(board, "O"):
            print_board(board)
            print("AI wins! Better luck next time.")
            break

        # Check for tie
        if is_board_full(board):
            print_board(board)
            print("It's a tie!")
            break

if __name__ == "__main__":
    main() # Start the game 