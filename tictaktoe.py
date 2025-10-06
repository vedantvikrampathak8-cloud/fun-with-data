import math
def print_board(b):
    print(f"\n {b[0]} | {b[1]} | {b[2]}")
    print("---+---+---")
    print(f" {b[3]} | {b[4]} | {b[5]}")
    print("---+---+---")
    print(f" {b[6]} | {b[7]} | {b[8]}\n")
win_lines = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
def check_winner(board):
    for a,b,c in win_lines:
        if board[a] == board[b] == board[c] and board[a] != " ":
            return board[a]
    if all(s != " " for s in board):
        return "Draw"
    return None
def minimax(board, depth, is_max, ai, human):
    winner = check_winner(board)
    if winner == ai:return 10-depth
    if winner == human: return depth - 10
    if winner == "Draw": return 0
    if is_max:
        best = -math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = ai
                val = minimax(board, depth+1,False ,ai ,human)
                board[i] = " "
                best = max(best ,val)
        return best
    else:
        best = math.inf
        for i in range(9):
            if board[i] == " ":
                board[i]=human
                val = minimax(board ,depth+1 ,True,ai ,human)
                board[i] = " "
                best = min(best, val)
        return best
def best_move(board, ai, human):
    best_val = -math.inf
    move=None
    for i in range(9):
        if board[i] == " ":
            board[i] = ai
            val =minimax(board, 0, False, ai, human)
            board[i] = " "
            if val > best_val:
                best_val = val
                move= i
    return move
def human_move(board):
    while True:
        try:
            p = int(input("Enter cell (1-9): ")) - 1
            if 0 <= p < 9 and board[p] == " ":
                return p
        except:
            pass
        print("Invalid.Try again ")
def main():
    board = [" "]*9
    print("You are X, AI is O.")
    first = input("Play first? (y/n): ").lower().startswith("y")
    human, ai = ("X","O") if first else ("O","X")
    turn = "human" if first else "ai"
    while True:
        print_board(board)
        winner = check_winner(board)
        if winner:
            if winner == "Draw":
                print("Draw!")
            else:
                print(f"{winner} wins!")
            break
        if turn == "human":
            pos = human_move(board)
            board[pos] = human
            turn = "ai"
        else:
            pos = best_move(board, ai, human)
            board[pos] = ai
            print(f"AI plays {pos+1}")
            turn = "human"
if __name__ == "__main__":
    main()
