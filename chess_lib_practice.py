# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 10:38:57 2021

@author: Ayush
"""

import chess
board  = chess.Board()

board.push_san("e4")
board.push_san("e5")
board.push_san("Nf3")
board.push_san("Nc6")
board.push_san("Bc4")
board.push_san("Bc5")

# print(board.legal_moves)

'''Converts string to move type'''
y = chess.Move.from_uci("e1g1")     

'''Converts move type to san'''
x = board.san(y)
print("Checking castle")
print(board.is_castling(y))
print(x)


board.push_san(x)
board.push_san("Nf6")
board.push_san("b4")
board.push_san("g5")
board.push_san("b5")

print("The next bool shows false indicating black to move.")
print(board.turn)

board.push_san("a5")

# print(board.legal_moves)


print (board)

y = chess.Move.from_uci("b5a6")
move1 = board.san(y)
move2 = "b5a6"
ymove2 = chess.Move.from_uci(move2)
print(str(board.is_capture(ymove2)) )
print(x)

