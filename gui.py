""" This is the main Gui Program
"""

# import chess
import tkinter as tk
from PIL import Image, ImageTk

button_list = []
chess_list = []

x = True
#Even_clicks checker

def exchange_piece_and_generate_string(button1,button2,i,j):
	button2["image"]=button1["image"]
	button1["image"]=''

def move(k):
    
    global x
    global prev
    
    if x:
        prev = k
        print(k)
        button_list[k].configure(bg = 'green')

    else:
        print(k)
        exchange_piece_and_generate_string(button_list[prev],button_list[k],prev,k)
        button_list[k].configure(activebackground = 'red')
        
        if prev%2==0:
            button_list[prev].configure(bg = '#8af542')
        else:
            button_list[prev].configure(bg = 'white')

        if k%2==0:
            button_list[k].configure(bg = '#8af542')
        else:
            button_list[k].configure(bg = 'white')
        prev = -1
    x = not x    


def assign_new_piece(button,path):
    
    img=None
    img = Image.open(path)
    img = img.resize((45,45))
    ph = ImageTk.PhotoImage(img)
    button.config(image=ph)
    button.image = ph

    
def initialize_board(button_list,window):

    highest = 450
    k=0
    for i in range(8):
        
        left_most = 280
        for j in range(8):
            
            k = 8*i +j
            if (i+j)%2 == 0:
                button_list.append(tk.Button(window,bg='#8af542',text=str(8*i+j),command = lambda k = k:move(k)))
            else:
                button_list.append(tk.Button(window,bg='white',text=str(8*i+j),command = lambda k = k :move(k)))

            button_list[k].place(height=50,width=50, x=left_most, y=highest)
            left_most+=50

        highest-=50

def initialize_chess(chess_list,button_list,window):
    for i in range(16):
        chess_list.append(i)
    for i in range(48,64):
        chess_list.append(i)
    
    file_path = {      "wr":"merida_chess_set/wr.svg",
                       "wn":"merida_chess_set/wn.svg",
                       "wb":"merida_chess_set/wb.svg",
                       "wq":"merida_chess_set/wq.svg",
                       "wk":"merida_chess_set/wk.svg",
                       "wp":"merida_chess_set/wp.svg",
                       "br":"merida_chess_set/br.svg",
                       "bn":"merida_chess_set/bn.svg",
                       "bb":"merida_chess_set/bb.svg",
                       "bq":"merida_chess_set/bq.svg",
                       "bk":"merida_chess_set/bk.svg",
                       "bp":"merida_chess_set/bp.svg"}
    
    png_path = {	   "wr":"alpha/wr.png",
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
    

def main():
    window = tk.Tk()
    window.title('Chess')
    window.geometry("960x540")
    window.resizable(False,False)
    
    initialize_board(button_list,window)
    initialize_chess(chess_list,button_list,window)
    
    #game (button_list)
    
    window.mainloop()
    
if __name__ == "__main__":
    main()