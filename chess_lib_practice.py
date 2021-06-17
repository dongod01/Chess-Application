# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 10:38:57 2021

@author: Ayush
"""

import chess
import chess.pgn
from helper import *
board  = chess.Board()

board.push_san("f3")
board.push_san("e5")
board.push_san("g4")
board.push_san("Qh4")

game = chess.pgn.Game()
game.headers["Event"] = "Example"
node = game.add_variation(chess.Move.from_uci("f2f3"))
node = node.add_variation(chess.Move.from_uci("e7e5"))
node = node.add_variation(chess.Move.from_uci("g2g4"))
node = node.add_variation(chess.Move.from_uci("d8h4"))
today = date.today()
d4 = today.strftime("%Y.%m.%d")
game.headers["Date"] = d4

game.headers["Result"] = "0-1"
#node.comment = "Comment"

print(game)

'''board.push_san("a5")
board.push_san("b4")
board.push_san("axb4")
board.push_san("a5")
board.push_san("Ra6")
board.push_san("Nf3")
board.push_san("Rc6")
board.push_san("a6")
board.push_san("b6")
board.push_san("a7")
board.push_san("g6")
alpha1 = board.san("")'''
#print(board)

board.apply_transform(chess.flip_horizontal)
board.apply_transform(chess.flip_vertical)

print(board.legal_moves)

print("\n\n")

print()


#print(game)
#print (board)

# board.push_san("a8=Q")

# board.push_san("e5")


# board.push_san("Nf3")
# board.push_san("Nc6")
# board.push_san("Bc4")
# board.push_san("Bc5")

# print(board.legal_moves)

# '''Converts string to move type'''
# y = chess.Move.from_uci("e1g1")     

# '''Converts move type to san'''
# x = board.san(y)
# print("Checking castle")
# print(board.is_castling(y))
# print(x)


# board.push_san(x)
# board.push_san("Nf6")
# board.push_san("b4")
# board.push_san("g5")
# board.push_san("b5")

# print("The next bool shows false indicating black to move.")
# print(board.turn)

# board.push_san("a5")

# print(board.legal_moves)


# print (board)

# y = chess.Move.from_uci("b5a6")
# move1 = board.san(y)
# move2 = "b5a6"
# ymove2 = chess.Move.from_uci(move2)
# print(str(board.is_capture(ymove2)) )
# print(x)

