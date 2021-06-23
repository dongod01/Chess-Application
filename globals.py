import chess.pgn

window = None
lock = None
board = None
game = chess.pgn.Game()
node = None
pop = None                  # pop is used for promotion
main_window = None

moves_table = None
button_list = []
chess_list = []

entry_list = [None]*300

move_counter = 0
move_list = []

color_val = None
resign_draw_socket = None
my_socket = None

voice_label = None

name1 = ""
name2 = ""

name_label3 = None
name_label4 = None

newp='t'

#Even_clicks checker
x = True
prev = -1
draw_offer_count = 0
game_ended = False