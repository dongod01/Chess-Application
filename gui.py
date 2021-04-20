# This is the main Gui Program
# Wherever it is not mentioned explicitly True means white and False means black

import globals 
from gui_Implementation import *

def others_move():
    globals.lock
    globals.lock.acquire()
    try:
        str_other = globals.my_socket.recv(1024).decode()
        str1,str2,str3 = str_other.split(',')
            
        prev = 63 - int(str1)
        k = 63 - int(str2)
            
        print("this is in others move " + str(prev) + "  " + str(k))
        print("the thread count is " + str(threading.active_count()))

        globals.name_label4["text"] = "Your Move"
        GUI_move_impl(prev,k,str3,False)
    finally:
        globals.lock.release()

def my_move(k):
    if globals.x:
        ind4 = globals.chess_list.index(k)
        if (ind4 in range(0,16)):   
            globals.prev = k
            print(k)
            globals.button_list[k].configure(bg = 'green')
        else:
            globals.x = not globals.x

    else:
        print(k)
        # Handling the case when sam==e square is clicked twice
        if k==globals.prev and (k//8+k%8)%2==0:
            globals.button_list[k].configure(bg = '#8af542')
        elif k==globals.prev and (k//8+k%8)%2!=0:
            globals.button_list[k].configure(bg = 'white')

        else: 
            globals.name_label4["text"] = "Opponent's Move"
            ret1,ret2 = GUI_move_impl(globals.prev,k,'t',True)       

            if(ret1):
                reinstate_color(globals.prev)
                reinstate_color(k)
                
                send_move(globals.prev,k,ret2)
                threading.Thread(target=others_move).start()
                
                globals.prev = -1

    globals.x = not globals.x   
    
def initialize_board():
    print("Initializing board wait!!!")
    highest = 450
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

    name_label1 = tk.Label( globals.window, text=globals.name1+ "(you)",font = ("Arial",12))
    name_label2 = tk.Label( globals.window, text=globals.name2+ "(opponent)",font = ("Arial",12))
    globals.name_label3 = tk.Label( globals.window, text="Match Ongoing",font = ("Arial",12))
    globals.name_label4 = tk.Label( globals.window, text="Your move",font = ("Arial",12))

    

    name_label1.place(height=100,width=300, x=500, y=400)
    name_label2.place(height=100,width=300, x=500, y=100)
    globals.name_label3.place(height=100,width=300, x=500, y=200)
    globals.name_label4.place(height=100,width=300, x=500, y=300)

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
        
        #board.apply_transform(chess.flip_horizontal)
        #board.apply_transform(chess.flip_vertical)
        
        #Mirror is WRONG, no second thoughts
        
        #board.apply_mirror()
        #board.apply_transform(chess.flip_horizontal)

        '''Black needs to know he's not playing from white side on library board'''
        
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
    globals.window = tk.Tk()
    globals.board = chess.Board()

    print("This is " + str(globals.color_val))

    globals.window.title('Chess')
    globals.window.geometry("960x540")
    globals.window.resizable(True,True)

    print("*********************************************************")
    print("*********************************************************")
    print("*********************************************************")

    initialize_board()
    initialize_chess()

    if not globals.color_val:
        threading.Thread(target=others_move).start()

    globals.window.mainloop()    