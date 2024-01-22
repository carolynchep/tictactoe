from __future__ import annotations  # allows us to use class name as type w/in that class
from enum import Enum
import copy
import random

###############################################################################
# for installing termcolor if it doesn't exist already
#
import sys
import subprocess
import pkg_resources
import os

required = {'termcolor'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    print(f"Installing Python libraries {', '.join(missing)}")
    python = sys.executable
    # subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
    subprocess.check_call([python, '-m', 'pip', 'install', *missing])  # will show install output

from termcolor import colored

######################################################################
class Player(Enum):
    X    = "X"
    O    = "O"
    NONE = " "
    
    def __str__(self) -> str: 
        return self.value # .value from Enum

######################################################################
class Square:
    __slots__ = ('_player')

    def __init__(self) -> None:
        self._player: Player = Player.NONE

    def getPlayer(self) -> Player:
        return self._player

    def setPlayer(self, player: Player) -> None:
        self._player = player

######################################################################
class Board:
    __slots__ = ('_board','_current_player')

    def __init__(self, board: list[Square] = [Square() for i in range(9)], 
                       current_player: Player = Player.X) -> None:
        ''' initializer for a TicTacToe board
        Parameters:
            board: a list of Square objects (default is all empty)
            current_player: the player to make the next move (default is X)
        '''
        self._board          : list[Square] = board
        self._current_player : Player       = current_player

    def __str__(self) -> str:
        ''' draws the Board object in traditional Tic-Tac-Toe 3x3 form 
        Returns:
            a string representation of the Board
        '''
        board_str = "\n"
        for s in range(len(self._board)):
            if self._board[s].getPlayer() == Player.NONE:
                pos_num = colored(str(s), "blue")
                board_str += f" {pos_num} "  # display the valid position number
            else:
                occupant = colored(str(self._board[s].getPlayer()), "red")
                board_str += f" {occupant} " # display the occupant
            if s % 3 < 2: board_str += '|'
            if s == 2 or s == 5: board_str += '\n' + str('-' * 11) + '\n'
        return board_str + "\n"

    @property
    def oppositePlayer(self) -> Player:
        ''' property (can treat as a variable rather than function call) to
            return the opposite of the current player
        Returns:
            Player.X if current player is O; o/w Player.O
        '''
        if self._current_player is Player.X: return Player.O
        if self._current_player is Player.O: return Player.X
        return Player.NONE

    def getCurrentPlayer(self) -> Player:
        ''' who has the current turn
        Returns:
            the current player, either Player.X or Player.O
        '''
        return self._current_player

    def getLegalMoves(self) -> list[int]:
        ''' returns a list of the still-valid moves to make
        Returns:
            a list of integers corresponding to valid moves
        '''
        moves = [s for s in range(len(self._board)) \
                    if self._board[s].getPlayer() == Player.NONE]
        return random.sample(moves, len(moves)) # so not always biasing early squares

    def getNewBoardWithMove(self, square: int) -> Board:
        ''' create a new copy of the Board with a given move by
            the current player
        Parameters:
            square: integer in [0,8] corresponding to desired Square
        Returns:
            a new Board with the current player taking the given square
        '''
        if square not in self.getLegalMoves():
            raise ValueError(f"Invalid move to square {square}")
        # create a copy of the board
        board_copy = copy.deepcopy(self._board)
        # current player takes indicated square
        board_copy[square].setPlayer(self._current_player)
        # return a new board updated with the current move, and swap
        # to indicate opposite player as the current player
        return Board(board = board_copy, \
                     current_player = self.oppositePlayer)

    def isWin(self) -> bool:
        ''' check whether the state of this Board is a win
        Returns:
            a tuple with:
                (True, winner) if either of X or O is in a winning state;
                (False, None)
        '''
        # list of possible wins in horizontal, vertical, diagonal
        wins = [(0,1,2), (3,4,5), (6,7,8), \
                (0,3,6), (1,4,7), (2,5,8), \
                (0,4,8), (2,4,6)]
        board = self._board # just for brevity below
        for win in wins:
            # check if the squares @ ordered triple locations match and aren't empty
            if board[win[0]].getPlayer() == \
               board[win[1]].getPlayer() == \
               board[win[2]].getPlayer() != Player.NONE:
                return True
        return False

    def isDraw(self) -> bool:
        ''' check whether the state of this Board is a draw
        Returns:
            True if the current board state is a draw; False o/w
        '''
        return not self.isWin() and len(self.getLegalMoves()) == 0

    def evaluate(self, original_player: Player) -> int:
        ''' evaluates the current board state, returning 0 on a draw, 1 on a
            win, or -1 on a loss
        Parameters:
            original_player: the original player kicking off this decision-tree
                exploration to determine what that player should do
        Returns:
            1 if the tree leaf corresponds to a win for the original player,
            -1 if the leaf corresponds to a loss, and 0 if a draw
        '''
        # this method is called at the top of minimax before the next
        # potential turn/move is considered -- therefore, if the board is in
        # a winning state right now, that means:
        #   - a win for the original player if the current player (who has yet
        #       to try the next move) is the other player
        #   - a loss for the original player if the current player is the
        #       original player
        if self.isWin() and self._current_player == original_player:
            return -1   # original player loses (other won on prev move)
        elif self.isWin() and self._current_player != original_player:
            return 1    # original player wins (on prev move)
        else:
            return 0

######################################################################
def main():
    b = Board()
    print(b)
    print(b.getLegalMoves())

    b = b.getNewBoardWithMove(3)  # here, O will win across diag
    b = b.getNewBoardWithMove(4)   # w/o above, X will win across dig
    b = b.getNewBoardWithMove(1)
    b = b.getNewBoardWithMove(8)
    b = b.getNewBoardWithMove(2)
    b = b.getNewBoardWithMove(0)
    print(b)
    print(b.isWin())

if __name__ == "__main__":
    main()
