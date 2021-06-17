import tkinter as tk
from tkinter.constants import RIGHT, Y

def txtEvent(event):
    if(event.state==12 and event.keysym=='c' ):
        return
    else:
        return "break"

class Table(tk.Frame):  
    def __init__(self,root):
        # code for creating table
        '''tk.Frame.__init__(self, root)
        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.place(height=40,width=10, x=150, y=150)
        self.canvas.place(height=180,width=380,x=550, y=130 )
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",
                                  tags="self.frame")
        #self.frame.bind("<Configure>", self.onFrameConfigure)'''
        canvas = tk.Canvas(self)
        
        sb = tk.Scrollbar(canvas)  
        canvas.place(height=200,width=400, x=550, y=130)
        sb.place(height=200,width=400, x=950, y=130)
        sb.config( command = canvas.yview )

        for k in range(150):
            i = 1 + int(k/2)
            j = 1 + int(k%2)
            self.e = tk.Entry(root, width=20, fg='blue',
                               font=('Arial',16,'bold'))
            
            self.e.place(height=30,width=100, x=(j-1)*100, y=30*(i-1))
            if k<len(move_list):
                self.e.insert(tk.END, move_list[k])
                self.e.bind("<Key>", lambda e: txtEvent(e))
                
            else:
                self.e.insert(tk.END, "-")
                self.e.bind("<Key>", lambda e: txtEvent(e))
    
    def fill(self,k,s):
        i = 1 + int(k/2)
        j = 1 + int(k%2)
        self.e.place(height=30,width=200, x=(j-1)*200, y=50*(i-1))
        self.e.insert(tk.END, s)
        #print("Whatcha")
        

move_list = ["e4","e5","Nf3","Nf6"]

root = tk.Tk()
frame = tk.Frame(root)
frame.place(height=200,width=400, x=550, y=130)
t = Table(frame)
#t.place(height=100,width=300, x=550, y=130)
t.fill(15,"Hello")
root.mainloop()
