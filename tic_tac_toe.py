import random

def print_board(board):
    print()
    for i in range(3):
        row = board[i*3:(i+1)*3]
        print(" " + " | ".join(row))
        if i < 2:
            print("---+---+---")
    print()

def check_winner(board, player):
    win_conditions = [
        [0,1,2], [3,4,5], [6,7,8],  # rows
        [0,3,6], [1,4,7], [2,5,8],  # columns
        [0,4,8], [2,4,6]            # diagonals
    ]
    for condition in win_conditions:
        if all(board[i] == player for i in condition):
            return True
    return False

def check_tie(board):
    return all(space != ' ' for space in board)

def get_user_move(board):
    while True:
        move = input("Enter your move (1-9): ")
        if not move.isdigit():
            print("Invalid input. Please enter a number between 1 and 9.")
            continue
        move = int(move)
        if move < 1 or move > 9:
            print("Invalid move. Please enter a number between 1 and 9.")
            continue
        if board[move-1] != ' ':
            print("That square is already occupied. Choose another one.")
            continue
        return move-1

def get_computer_move(board):
    available = [i for i, spot in enumerate(board) if spot == ' ']
    return random.choice(available)

def main():
    board = [' '] * 9
    # Computer starts with 'X' in the middle
    board[4] = 'X'
    print("Welcome to Tic-Tac-Toe!")
    print("You are 'O'. The computer is 'X'.")
    print("Squares are numbered 1 to 9, row-wise.")
    print_board(board)

    while True:
        # User move
        user_move = get_user_move(board)
        board[user_move] = 'O'
        print_board(board)
        if check_winner(board, 'O'):
            print("You win!")
            break
        if check_tie(board):
            print("It's a tie!")
            break

        # Computer move
        comp_move = get_computer_move(board)
        board[comp_move] = 'X'
        print("Computer moves to square", comp_move+1)
        print_board(board)
        if check_winner(board, 'X'):
            print("Computer wins!")
            break
        if check_tie(board):
            print("It's a tie!")
            break

if __name__ == "__main__":
    main()
