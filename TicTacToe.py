from Board import *
import copy

def minimax(current_board:   Board, \
            is_maximizing:   bool, \
            original_player: Player, \
            debug:           bool = False) -> int:
    if current_board.isWin() or current_board.isDraw():
        return current_board.evaluate(original_player)

    if is_maximizing:
        best_result = float("-inf")
        for move in current_board.getLegalMoves():
            is_maximizing = False
            result = minimax(current_board.getNewBoardWithMove(move),
							is_maximizing, original_player)
                            #update best_result if appropriate
            if result > best_result:
                best_result = result
        return best_result
    else:
        worst_result = float("inf")
        for move in current_board.getLegalMoves():
            is_maximizing = True
            result = minimax(current_board.getNewBoardWithMove(move),
                            is_maximizing, original_player)
            #update worst_result if appropriate

            if result < worst_result:
                worst_result = result
        return worst_result


def findBestMove(current_board: Board, debug: bool = False) -> int:
    ''' Function for the computer to find its best possible move among all
        remaining moves.  This is accomplished by calling the recursive
        minimax, which will alternate player turns who are alternating
        minimizing and maximizing (i.e., O is trying to minimize X's outcome,
        while X is trying to maximize X's outcome).
    Parameters:
        current_board: a Board object, the current board state
        debug: boolean -- if True, prints debugging info
    Returns:
        the evaluation of the best move for the computer (1 if leading to a
            win, -1 if leading to a loss, 0 if leading to a draw)
    '''
    best_result = float("-inf")
    best_move   = None
    for move in current_board.getLegalMoves():
        is_maximizing = False  # O will attempt to minimize X's outcome
        if debug: print(f"{current_board.getCurrentPlayer()} exploring {move}")
        # determine the eventual outcome when O tries the current move,
        # by exploring all possible outcomes along the decision tree when
        # O tries that move
        result = minimax(current_board.getNewBoardWithMove(move), \
                         is_maximizing, \
                         current_board.getCurrentPlayer(), \
                         debug)
        # keep track of best outcome that can occur across all possible moves
        if result > best_result:
            best_result = result
            best_move = move
    return best_move

def getPlayerMove(board: Board) -> int:
    ''' ask the user for a valid board space, returning that integer
    Parameters:
        board: the current state of the board
    Returns:
        a valid integer in [0,8] corresponding to an open square
    '''
    player_move = None
    while player_move not in board.getLegalMoves():
        try:
            player_move = int(input("Enter a legal square (0-8): "))
        except:
            pass  # ignore and loop back if input is invalid
    return player_move

def checkForEnd(board: Board, player_name: str) -> bool:
    ''' checks whether game is over, whether win, lose, or draw, and
        prints a corresponding message if so
    Parameters:
        board: the current state of the game board
        player_name: the player making the current move
    Returns:
        True if game is over; False o/w
    '''
    if board.isWin():
        print(f"{player_name} wins!")
        return True
    elif board.isDraw():
        print("It's a draw!")
        return True
    return False

def play(debug: bool = False) -> None:
    ''' function to control game play for Tic Tac Toe
    Parameters:
        debug: boolean; prints debuggint output if True
    '''

    board = Board()
    print(board)

    # main game loop
    while True:
        # assume the human player goes first as 'X'
        human_move = getPlayerMove(board)
        board = board.getNewBoardWithMove(human_move)
        print(board)
        if checkForEnd(board, "Human"):
            # game is over -- bail out
            break

        # then the computer gets to determine its best move via minimax
        computer_move = findBestMove(board, debug)
        print(f"Computer's move is {computer_move}")
        board = board.getNewBoardWithMove(computer_move)
        print(board)
        if checkForEnd(board, "Computer"):
            # game is over -- bail out
            break

def main():
    #play(debug = True)
    play()

if __name__ == "__main__":
    main()
