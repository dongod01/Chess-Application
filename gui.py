# This is the main Gui Program
# Wherever it is not mentioned explicitly True means white and False means black

import main_program
import chess
import tkinter as tk
from PIL import Image, ImageTk
import time
import threading
#from helper import *

button_list = []
chess_list = []

board = chess.Board()

x = True
#Even_clicks checker
def promotion_check(prev,k):
    if chess_list.index(prev) in range(8,16):
        if ( k in range(56,64) ):
            return True
    return False

def assign_new_piece(button,path):
    
    img=None
    img = Image.open(path)
    img = img.resize((45,45))
    ph = ImageTk.PhotoImage(img)
    button.config(image=ph)
    button.image = ph    

def reinstate_color(prev):
    if (prev//8 + prev %8)%2==0:
        button_list[prev].configure(bg = '#8af542')
    else:
        button_list[prev].configure(bg = 'white')

def sqr_notation(i):
    if i<=63:
        c = 'a'
        c = chr(ord(c) + i%8)
        c += str(i//8 +1)
        return c
    return None
    
def exchange_piece(button1,button2):
    if (button1["image"]!=''):
        button2["image"]=button1["image"]
        button1["image"]=''
        
def remove_piece(button1):
    button1["image"] = ''
    print("Removing")
        
def generate_uci(i,j):
   
    s1 = sqr_notation(i)
    s1+= sqr_notation(j)
    
    print("this is the uci "+ s1)
    
    return s1

def func_return(string1): 
    global newp                 
    newp = string1
    pop.destroy()

def call_message_box():
    global pop
    pop = tk.Toplevel(window)
    pop.geometry("50x200")
    if (color_val):
        button1 = tk.Button(pop,bg='white',command = lambda : func_return('q'))
        button1.place(height=50,width=50, x=0, y=0)
        assign_new_piece(button1,"alpha/wq.png")
        
        button2 = tk.Button(pop,bg='white',command = lambda : func_return('b'))
        button2.place(height=50,width=50, x=0, y=50)
        assign_new_piece(button2,"alpha/wb.png")
        
        button3 = tk.Button(pop,bg='white',command = lambda : func_return('n'))
        button3.place(height=50,width=50, x=0, y=100)
        assign_new_piece(button3,"alpha/wn.png")
        
        button4 = tk.Button(pop,bg='white',command = lambda : func_return('r'))
        button4.place(height=50,width=50, x=0, y=150)
        assign_new_piece(button4,"alpha/wr.png")
    else:
        button1 = tk.Button(pop,bg='white',command = lambda : func_return('q'))
        button1.place(height=50,width=50, x=0, y=0)
        assign_new_piece(button1,"alpha/bq.png")

        button2 = tk.Button(pop,bg='white',command = lambda : func_return('b'))
        button2.place(height=50,width=50, x=0, y=50)
        assign_new_piece(button2,"alpha/bb.png")
        
        button3 = tk.Button(pop,bg='white',command = lambda : func_return('n'))
        button3.place(height=50,width=50, x=0, y=100)
        assign_new_piece(button3,"alpha/bn.png")
        
        button4 = tk.Button(pop,bg='white',command = lambda : func_return('r'))
        button4.place(height=50,width=50, x=0, y=150)
        assign_new_piece(button4,"alpha/br.png")

def send_move(prev,k,prom_char):    
    resultant_string = str(prev) + "," + str(k)+ "," + prom_char
    my_socket.sendall(resultant_string.encode())

def GUI_move_impl(prev,k,prom_char):
    global newp
    newp=prom_char
    islegal=False
    '''If the move is legal'''
    
    print("this is "+str(prev) +" and " + str(k))
    
    if color_val:
        uci = generate_uci(prev,k)
    else:
        uci = generate_uci(63-prev,63-k)

    #uci = generate_uci(prev,k)
     
    yuci = chess.Move.from_uci(uci)
    print(board.legal_moves)
    
    if promotion_check(prev,k):
                
        print("Inside promotion check")
        if (prom_char == 't'):
            call_message_box()    
            window.wait_window(pop)     # the function waits for the other window to close

            if newp=='q' and color_val:
                    assign_new_piece(button_list[prev],"alpha/wq.png")
            elif newp=='r' and color_val:
                    assign_new_piece(button_list[prev],"alpha/wr.png")
            elif newp=='b' and color_val:
                    assign_new_piece(button_list[prev],"alpha/wb.png")
            elif newp=='n' and color_val:
                    assign_new_piece(button_list[prev],"alpha/wn.png")
            elif newp=='q' and not color_val:
                    assign_new_piece(button_list[prev],"alpha/bq.png")
            elif newp=='r' and not color_val:
                    assign_new_piece(button_list[prev],"alpha/br.png")
            elif newp=='b' and not color_val:
                    assign_new_piece(button_list[prev],"alpha/bb.png")
            elif newp=='n' and not color_val:
                    assign_new_piece(button_list[prev],"alpha/bn.png")
            uci += newp
        else:
            uci += prom_char
            if prom_char=='q' and not color_val:
                    assign_new_piece(button_list[prev],"alpha/wq.png")
            elif prom_char=='r' and not color_val:
                    assign_new_piece(button_list[prev],"alpha/wr.png")
            elif prom_char=='b' and not color_val:
                    assign_new_piece(button_list[prev],"alpha/wb.png")
            elif prom_char=='n' and not color_val:
                    assign_new_piece(button_list[prev],"alpha/wn.png")
            elif prom_char=='q' and color_val:
                    assign_new_piece(button_list[prev],"alpha/bq.png")
            elif prom_char=='r' and color_val:
                    assign_new_piece(button_list[prev],"alpha/br.png")
            elif prom_char=='b' and color_val:
                    assign_new_piece(button_list[prev],"alpha/bb.png")
            elif prom_char=='n' and color_val:
                    assign_new_piece(button_list[prev],"alpha/bn.png")
        
        exchange_piece(button_list[prev],button_list[k])
        
        try:
            # Index of capturing piece
            ind1 = chess_list.index(prev, 0, len(chess_list))
            
        except ValueError:
            print("No piece in initial index in move function of promotion")
        
        # Index of captured piece
        ind2 = chess_list.index(k, 0, len(chess_list)) if k in chess_list else -1
        chess_list[ind1] = k

        if ind2!=-1:
            chess_list[ind2] = -1  #Making the captured piece -1 in chesslist
        
       
        islegal=True

        board.push_san(uci)

        print(chess_list)

        print(board)           
    
    elif yuci in board.legal_moves:
            
        # First piece move
        
        print("Verifying move:")
        
        '''Standard algebraic notation san'''
        
        if (board.is_castling(yuci)):
            # Works fine
            # 4 cases white-black and short castle-long castle
            # True indicates white's turn'
            
            # These two checks work to include the case when the rook is clicked for castling
            if 	 (k == 0 or k == 56):
                k+=2

            elif (k == 7 or k == 63): 	
                k-=1  

            alpha = board.san(yuci)
            exchange_piece(button_list[prev],button_list[k])
            print("Inside castling")
            
            if alpha=="O-O" and board.turn==True and color_val:
                exchange_piece(button_list[7],button_list[5])
                chess_list[7] = 5
            elif alpha=="O-O" and board.turn==True and not color_val:
                exchange_piece(button_list[56],button_list[58])
                chess_list[24] = 58
            elif alpha=="O-O" and board.turn==False and color_val:
                exchange_piece(button_list[63],button_list[61])
                chess_list[31] = 61
            elif alpha=="O-O" and board.turn==False and not color_val:
                exchange_piece(button_list[0],button_list[2])
                chess_list[0] = 2
            elif alpha=="O-O-O" and board.turn==True and color_val:
                exchange_piece(button_list[0],button_list[3])
                chess_list[0] = 3
            elif alpha=="O-O-O" and board.turn==True and not color_val:
                exchange_piece(button_list[63],button_list[60])
                chess_list[31] = 60
            elif alpha=="O-O-O" and board.turn==False and color_val:
                exchange_piece(button_list[56],button_list[59]) 
                chess_list[24] = 59
            elif alpha=="O-O-O" and board.turn==False and not color_val:
                exchange_piece(button_list[7],button_list[4])
                chess_list[7] = 4
             

        elif board.is_en_passant(yuci):
            # Works fine
            exchange_piece(button_list[prev],button_list[k])
            print("Inside en passant")
            mod = (k-prev)%8
            if mod==7:
                mod = -1
            
            delpawn = prev + mod
            print("Deleting")
            remove_piece(button_list[delpawn])
            
            ind_del = chess_list.index(delpawn)
            chess_list[ind_del] = -1
        
        elif board.is_capture(yuci):
            exchange_piece(button_list[prev],button_list[k])
            print("Okok")
        
        else:
            exchange_piece(button_list[prev],button_list[k])
            print("Xyz")

        board.push_san(uci)
        print(board)
        islegal=True
        
        try:
            # Index of capturing piece
            ind1 = chess_list.index(prev, 0, len(chess_list))
            
        except ValueError:
            print("No piece in initial index in move function")
        
        # Index of captured piece
        ind2 = chess_list.index(k, 0, len(chess_list)) if k in chess_list else -1
        chess_list[ind1] = k

        if ind2!=-1:
            chess_list[ind2] = -1  #Making the captured piece -1 in chesslist

        print(chess_list)
        
    return islegal,newp

def others_move():
    global lock
    lock.acquire()
    try:
        str_other = my_socket.recv(1024).decode()
        str1,str2,str3 = str_other.split(',')
            
        prev = 63 - int(str1)
        k = 63 - int(str2)
            
        print("this is in others move " + str(prev) + "  " + str(k))
        print("the thread count is " + str(threading.active_count()))

        GUI_move_impl(prev,k,str3)
    finally:
        lock.release()

def my_move(k):
    global x
    global prev
    
    if x:
        ind4 = chess_list.index(k)
        if (ind4 in range(0,16)):   
            prev = k
            print(k)
            button_list[k].configure(bg = 'green')
        else:
            x = not x

    else:
        print(k)
        # Handling the case when sam==e square is clicked twice
        if k==prev and (k//8+k%8)%2==0:
            button_list[k].configure(bg = '#8af542')
        elif k==prev and (k//8+k%8)%2!=0:
            button_list[k].configure(bg = 'white')

        else: 
            ret1,ret2 = GUI_move_impl(prev,k,'t')         
            if(ret1):
                reinstate_color(prev)
                reinstate_color(k)
                
                

                send_move(prev,k,ret2)
                threading.Thread(target=others_move).start()
                
                prev = -1

    x = not x   
    
def initialize_board():

    print("Initializing board wait!!!")
    highest = 450
    k=0
    for i in range(8):
        
        left_most = 280
        for j in range(8):
            
            k = 8*i +j
            if (i+j)%2 == 0:
                button_list.append(tk.Button(window,bg='#8af542',text=str(8*i+j),command = lambda k=k: my_move(k)))
            else:
                button_list.append(tk.Button(window,bg='white',text=str(8*i+j),command = lambda k=k: my_move(k)))

            button_list[k].place(height=50,width=50, x=left_most, y=highest)
            left_most+=50

        highest-=50

def initialize_chess():
    for i in range(16):
        chess_list.append(i)
    for i in range(48,64):
        chess_list.append(i)
    
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
    
    if (color_val == True):
        print("Initializing for white man!!!")
        assign_new_piece(button_list[0],png_path["wr"])
        assign_new_piece(button_list[1],png_path["wn"])
        assign_new_piece(button_list[2],png_path["wb"])
        assign_new_piece(button_list[3],png_path["wq"])
        assign_new_piece(button_list[4],png_path["wk"])
        assign_new_piece(button_list[5],png_path["wb"])
        assign_new_piece(button_list[6],png_path["wn"])
        assign_new_piece(button_list[7],png_path["wr"])

        for i in range(8):
            assign_new_piece(button_list[8+i],png_path["wp"])
            assign_new_piece(button_list[48+i],png_path["bpawn"])

        assign_new_piece(button_list[56],png_path["br"])
        assign_new_piece(button_list[57],png_path["bn"])
        assign_new_piece(button_list[58],png_path["bb"])
        assign_new_piece(button_list[59],png_path["bq"])
        assign_new_piece(button_list[60],png_path["bk"])
        assign_new_piece(button_list[61],png_path["bb"])
        assign_new_piece(button_list[62],png_path["bn"])
        assign_new_piece(button_list[63],png_path["br"])

    if (color_val == False):
        print("Initializing for black man!!!")
        
        #board.apply_transform(chess.flip_horizontal)
        #board.apply_transform(chess.flip_vertical)
        
        #Mirror is WRONG, no second thoughts
        
        #board.apply_mirror()
        #board.apply_transform(chess.flip_horizontal)

        '''Black needs to know he's not playing from white side on library board'''
        
        assign_new_piece(button_list[56],png_path["wr"])
        assign_new_piece(button_list[57],png_path["wn"])
        assign_new_piece(button_list[58],png_path["wb"])
        '''New comment'''
        assign_new_piece(button_list[59],png_path["wk"])
        assign_new_piece(button_list[60],png_path["wq"])
        assign_new_piece(button_list[61],png_path["wb"])
        assign_new_piece(button_list[62],png_path["wn"])
        assign_new_piece(button_list[63],png_path["wr"])

        for i in range(8):
            assign_new_piece(button_list[48+i],png_path["wp"])
            assign_new_piece(button_list[8+i],png_path["bpawn"])

        assign_new_piece(button_list[0],png_path["br"])
        assign_new_piece(button_list[1],png_path["bn"])
        assign_new_piece(button_list[2],png_path["bb"])
        assign_new_piece(button_list[3],png_path["bk"])
        assign_new_piece(button_list[4],png_path["bq"])
        assign_new_piece(button_list[5],png_path["bb"])
        assign_new_piece(button_list[6],png_path["bn"])
        assign_new_piece(button_list[7],png_path["br"])
    
def main(val,soc):
    global color_val
    color_val = val

    global my_socket 
    my_socket = soc

    global lock
    lock = threading.Lock()

    print("This is " + str(color_val))

    global window
    window = tk.Tk()
    window.title('Chess')
    window.geometry("960x540")
    window.resizable(True,True)

    initialize_board()
    initialize_chess()

    if not color_val:
        threading.Thread(target=others_move).start()

    window.mainloop()    
    
