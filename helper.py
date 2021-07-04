import chess
import chess.pgn
import tkinter as tk
from PIL import Image, ImageTk
import time
import os
from datetime import datetime,date
import threading
from tkinter.filedialog import asksaveasfile
import globals

def PGN_init():
    globals.game = chess.pgn.Game()

def addPGN():
    folder_name = 'Games'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    today = datetime.today()
    dt = today.strftime("%d%m%Y")
    now = datetime.now()
    ct = now.strftime("%H%M%S")
    pgnfile_name = globals.name1 + '_' + dt + '_'  + ct + '.txt'
    fp = asksaveasfile(initialfile = pgnfile_name,defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Document","*.txt")])
    fp.write(str(globals.game))    

def addPGNbutton():
    globals.pgn_button = tk.Button(globals.main_window,text="Download PGN file",command = addPGN)
    globals.pgn_button.place(height=50,width=300, x=160, y=310)

def txtEvent(event):
    if(event.state==12 and event.keysym=='c' ):
        return
    else:
        return "break"

class Moves_Table(tk.Frame):
    def __init__(self, parent):

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

        self.populate()

    def populate(self):
        for k in range(100):
            '''tk.Label(self.frame, text="%s" % row, width=3, borderwidth="1",
                     relief="solid").grid(row=row, column=0)
            t="this is the second column for row %s" %row
            tk.Label(self.frame, text=t).grid(row=row, column=1)'''
            i = 1 + int(k/2)
            j = 1 + int(k%2)

            globals.entry_list[k] = tk.Entry(self.frame, width=16, fg='blue',
                               font=('Arial',16,'bold'))
            
            globals.entry_list[k].grid(row=i, column=j)
            if k<len(globals.move_list):
                globals.entry_list[k].insert(tk.END, globals.move_list[k])
                globals.entry_list[k].bind("<Key>", lambda e: txtEvent(e))
                
            else:
                globals.entry_list[k].insert(tk.END, "")
                globals.entry_list[k].bind("<Key>", lambda e: txtEvent(e))


    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def set_Move_List_Cell(self,k,text):
        i = 1 + int(k/2)
        if(k%2==0):
            tk.Label(self.frame, text="%s" % i, width=3).grid(row=i, column=0)
        globals.entry_list[k].delete(0,"end")
        globals.entry_list[k].insert(0, " "+text)

def position_checker(called_from):
    if(not globals.board.turn):
            s = "White"
    else:
            s = "Black"
    

    if globals.board.is_checkmate():
        if called_from:
            globals.name_label3["text"] = "Checkmate! You win :)"
            if globals.color_val:
                globals.game.headers["Result"] = "1-0"
            else:
                globals.game.headers["Result"] = "0-1"
        else:
            globals.name_label3["text"] = "Checkmate! Opponent wins :("
            if not globals.color_val:
                globals.game.headers["Result"] = "1-0"
            else:
                globals.game.headers["Result"] = "0-1"
        
        print("\n\n\n")
        print("Checkmate! " +s+ " wins!" )
        print("#########################################################")
        print("\n\n\n")
    elif globals.board.is_stalemate():
        globals.name_label3["text"] = "Stalemate -  Game ends in a draw."
        globals.game.headers["Result"] = "1/2-1/2"
        print("\n\n\n")
        print("Stalemate -  Game ends in a draw." )
        print("#########################################################")
        print("\n\n\n")
    elif globals.board.is_repetition():
        globals.name_label3["text"] = "Threefold Repetition -  Game ends in a draw."
        globals.game.headers["Result"] = "1/2-1/2"
        print("\n\n\n")
        print("Threefold Repetition -  Game ends in a draw." )
        print("#########################################################")
        print("\n\n\n")
    elif globals.board.is_fifty_moves():
        globals.name_label3["text"] = "50 move rule -  Game ends in a draw."
        globals.game.headers["Result"] = "1/2-1/2"
        print("\n\n\n")    
        print("50 move rule - Game ends in a draw." )
        print("#########################################################")
        print("\n\n\n")
    elif globals.board.is_insufficient_material():
        globals.name_label3["text"] = "Insufficient -  Game ends in a draw."
        globals.game.headers["Result"] = "1/2-1/2"
        print("Insufficient material for checkmate - Game ends in a draw." )
        print("#########################################################")

def promotion_check(prev,k,called_from):
    if globals.chess_list.index(prev) in range(8,16):
        if ( k in range(56,64) ) and (called_from):
            return True
    if globals.chess_list.index(prev) in range(16,24):
        if ( k in range(0,8) ) and (not called_from):
            return True
    return False

def assign_new_piece(button,path):
    img=None
    img = Image.open(path)
    img = img.resize((45,45))
    ph = ImageTk.PhotoImage(img)
    button.config(image=ph)
    button.image = ph    

def reinstate_color(box_index):
    if (box_index//8 + box_index %8)%2==0:
        globals.button_list[box_index].configure(bg = '#8af542')
    else:
        globals.button_list[box_index].configure(bg = 'white')

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
    globals.newp = string1
    globals.pop.destroy()

def call_message_box():
    globals.pop = tk.Toplevel(globals.window)
    globals.pop.geometry("50x200")
    
    if (globals.color_val):
        button1 = tk.Button(globals.pop,bg='white',command = lambda : func_return('q'))
        button1.place(height=50,width=50, x=0, y=0)
        assign_new_piece(button1,"alpha/wq.png")
        
        button2 = tk.Button(globals.pop,bg='white',command = lambda : func_return('b'))
        button2.place(height=50,width=50, x=0, y=50)
        assign_new_piece(button2,"alpha/wb.png")
        
        button3 = tk.Button(globals.pop,bg='white',command = lambda : func_return('n'))
        button3.place(height=50,width=50, x=0, y=100)
        assign_new_piece(button3,"alpha/wn.png")
        
        button4 = tk.Button(globals.pop,bg='white',command = lambda : func_return('r'))
        button4.place(height=50,width=50, x=0, y=150)
        assign_new_piece(button4,"alpha/wr.png")
    else:
        button1 = tk.Button(globals.pop,bg='white',command = lambda : func_return('q'))
        button1.place(height=50,width=50, x=0, y=0)
        assign_new_piece(button1,"alpha/bq.png")

        button2 = tk.Button(globals.pop,bg='white',command = lambda : func_return('b'))
        button2.place(height=50,width=50, x=0, y=50)
        assign_new_piece(button2,"alpha/bb.png")
        
        button3 = tk.Button(globals.pop,bg='white',command = lambda : func_return('n'))
        button3.place(height=50,width=50, x=0, y=100)
        assign_new_piece(button3,"alpha/bn.png")
        
        button4 = tk.Button(globals.pop,bg='white',command = lambda : func_return('r'))
        button4.place(height=50,width=50, x=0, y=150)
        assign_new_piece(button4,"alpha/br.png")

def send_move(prev,k,prom_char):    

    resultant_string = str(prev) + "," + str(k)+ "," + prom_char
    globals.game_socket.sendall(resultant_string.encode())
