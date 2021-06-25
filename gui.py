# This is the main Gui Program
# Wherever it is not mentioned explicitly True means white and False means black

import globals 
from gui_Implementation import *
from sound import sound_impl

def resign():
    if (not globals.game_ended):
        resultant_string = "1"
        globals.resign_draw_socket.sendall(resultant_string.encode())

        string_response = globals.resign_draw_socket.recv(1024).decode()
        if (string_response == "1"):
            print("Opponent has resigned!!!")
            globals.name_label3["text"] = " You lose by resignation :("
            if not globals.color_val:
                globals.game.headers["Result"] = "1-0"
            else:
                globals.game.headers["Result"] = "0-1"
        print("Game Ended")
        addPGNbutton()
        globals.game_ended = True

def draw():
    if (not globals.game_ended and globals.draw_offer_count == 0):
        resultant_string = "0"
        globals.resign_draw_socket.sendall(resultant_string.encode())

        string_response = globals.resign_draw_socket.recv(1024).decode()
        
        if (string_response == "1"): 
            print("Opponent has accepted the draw offer!!")
            globals.name_label3["text"] = " Draw by Agreement"
            globals.game.headers["Result"] = "1/2-1/2"
            addPGNbutton()
            globals.game_ended = True
            print("Game has ended!!!")

        elif (string_response == "0"):
            print("Opponent has declined the draw offer so continue playing !!")

            globals.name_label3["text"] = " Draw offer rejected"

        globals.draw_offer_count += 1

def start_capture_thread():
    t2 = threading.Thread(target=sound_impl)
    t2.start()

def initialize_board():
    
    
    print("Initializing board wait!!!")
    highest = 400
    k=0
    for i in range(8):
        
        left_most = 50
        for j in range(8):
            
            k = 8*i +j
            if (i+j)%2 == 0:
                globals.button_list.append(tk.Button(globals.window,bg='#8af542',text=str(8*i+j),command = lambda k=k: my_move(k)))
            else:
                globals.button_list.append(tk.Button(globals.window,bg='white',text=str(8*i+j),command = lambda k=k: my_move(k)))

            globals.button_list[k].place(height=50,width=50, x=left_most, y=highest)
            left_most+=50

        highest-=50
    
    name_label1 = tk.Label( globals.window, text=globals.name1+ "(you)",font = ("Arial",20))
    name_label2 = tk.Label( globals.window, text=globals.name2+ "(opponent)",font = ("Arial",20))
    globals.name_label3 = tk.Label( globals.window, text="Match Ongoing",font = ("Arial",12))
    
    if globals.color_val:
        globals.name_label4 = tk.Label( globals.window, text="Your move",font = ("Arial",12))
    elif not globals.color_val:
        globals.name_label4 = tk.Label( globals.window, text="Opponent's move",font = ("Arial",12))
    
    voice_btn = tk.Button(globals.window,bg='#388e8e',text = "Speak!", command = start_capture_thread)  
    globals.voice_label = tk.Label( globals.window, text = "(Empty)", font = ("Arial",12))

    frame = tk.Frame(globals.window)
    frame.place(height=200,width=400, x=500, y=150)
    
    globals.moves_table = Moves_Table(frame)
    globals.moves_table.pack(side="top", fill="both", expand=True)

    resign_button = tk.Button(globals.window,bg='#388e8e',text = "Resign", command = resign)
    resign_button.place(height=30,width=100, x=550, y=355)
    
    draw_button = tk.Button(globals.window,bg='#388e8e',text = "Draw", command = draw)
    draw_button.place(height=30,width=100, x=740, y=355)

    globals.name_label3.configure(anchor="center")

    name_label1.place(height=100,width=300, x=550, y=390)
    name_label2.place(height=100,width=300, x=550, y=20)
    globals.name_label3.place(height=30,width=200, x=177, y=10)
    globals.name_label4.place(height=50,width=200, x=145, y=450)
    
    globals.voice_label.place(height=50,width=250, x=750, y=470)
    voice_btn.place(height=35,width=100, x=600, y=480)
    
def initialize_chess():
    for i in range(16):
        globals.chess_list.append(i)
    for i in range(48,64):
        globals.chess_list.append(i)
    
    png_path = {       "wr":"alpha/wr.png",
                       "wn":"alpha/wn.png",
                       "wb":"alpha/wb.png",
                       "wq":"alpha/wq.png",
                       "wk":"alpha/wk.png",
                       "wp":"alpha/wp.png",
                       "br":"alpha/br.png",
                       "bn":"alpha/bn.png",
                       "bb":"alpha/bb.png",
                       "bq":"alpha/bq.png",
                       "bk":"alpha/bk.png",
                       "bpawn":"alpha/bp1.jpg"}
    
    if (globals.color_val == True):
        print("Initializing for white man!!!")
        assign_new_piece(globals.button_list[0],png_path["wr"])
        assign_new_piece(globals.button_list[1],png_path["wn"])
        assign_new_piece(globals.button_list[2],png_path["wb"])
        assign_new_piece(globals.button_list[3],png_path["wq"])
        assign_new_piece(globals.button_list[4],png_path["wk"])
        assign_new_piece(globals.button_list[5],png_path["wb"])
        assign_new_piece(globals.button_list[6],png_path["wn"])
        assign_new_piece(globals.button_list[7],png_path["wr"])

        for i in range(8):
            assign_new_piece(globals.button_list[8+i],png_path["wp"])
            assign_new_piece(globals.button_list[48+i],png_path["bpawn"])

        assign_new_piece(globals.button_list[56],png_path["br"])
        assign_new_piece(globals.button_list[57],png_path["bn"])
        assign_new_piece(globals.button_list[58],png_path["bb"])
        assign_new_piece(globals.button_list[59],png_path["bq"])
        assign_new_piece(globals.button_list[60],png_path["bk"])
        assign_new_piece(globals.button_list[61],png_path["bb"])
        assign_new_piece(globals.button_list[62],png_path["bn"])
        assign_new_piece(globals.button_list[63],png_path["br"])

    if (globals.color_val == False):
        print("Initializing for black man!!!")
        
        assign_new_piece(globals.button_list[56],png_path["wr"])
        assign_new_piece(globals.button_list[57],png_path["wn"])
        assign_new_piece(globals.button_list[58],png_path["wb"])
        '''New comment'''
        assign_new_piece(globals.button_list[59],png_path["wk"])
        assign_new_piece(globals.button_list[60],png_path["wq"])
        assign_new_piece(globals.button_list[61],png_path["wb"])
        assign_new_piece(globals.button_list[62],png_path["wn"])
        assign_new_piece(globals.button_list[63],png_path["wr"])

        for i in range(8):
            assign_new_piece(globals.button_list[48+i],png_path["wp"])
            assign_new_piece(globals.button_list[8+i],png_path["bpawn"])

        assign_new_piece(globals.button_list[0],png_path["br"])
        assign_new_piece(globals.button_list[1],png_path["bn"])
        assign_new_piece(globals.button_list[2],png_path["bb"])
        assign_new_piece(globals.button_list[3],png_path["bk"])
        assign_new_piece(globals.button_list[4],png_path["bq"])
        assign_new_piece(globals.button_list[5],png_path["bb"])
        assign_new_piece(globals.button_list[6],png_path["bn"])
        assign_new_piece(globals.button_list[7],png_path["br"])
    
def main():
    globals.lock = threading.Lock()
    globals.window = tk.Toplevel(globals.main_window)
    globals.board = chess.Board()
    
    globals.game.headers["Event"] = "Chess Application Practice Game"
    today = date.today()
    dt = today.strftime("%Y.%m.%d")
    globals.game.headers["Date"] = dt

    print("This is " + str(globals.color_val))
    globals.main_window.title('Chess Application - ' + globals.name1)
    globals.window.title('Chess - ' + globals.name1)
    globals.window.geometry("960x540")
    globals.window.resizable(True,True)

    print("*********************************************************")
    print("*********************************************************")
    print("*********************************************************")

    initialize_board()
    initialize_chess()

    threading.Thread(target=wait_for_resign_or_draw_event).start()

    if not globals.color_val:
        threading.Thread(target=others_move).start()

    globals.window.mainloop()    