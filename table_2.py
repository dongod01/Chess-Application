import tkinter as tk

entry_list = [None]*300
move_list = ["e4","e5","Nf3","Nf6"]

def setTextInput(k,text):
    entry_list[k].delete(0,"end")
    entry_list[k].insert(0, text)

def txtEvent(event):
    if(event.state==12 and event.keysym=='c' ):
        return
    else:
        return "break"

class Example(tk.Frame):
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
            i = 1 + int(k/2)
            j = 2 + int(k%2)
            if(k%2==0):
                tk.Label(self.frame, text="%s" % i, width=3
                     ).grid(row=i, column=0)
            '''t="this is the second column for row %s" %row
            tk.Label(self.frame, text=t).grid(row=row, column=1)'''
            

            entry_list[k] = tk.Entry(self.frame, width=16, fg='blue',
                               font=('Arial',16,'bold'))
            
            entry_list[k].grid(row=i, column=j)
            if k<len(move_list):
                entry_list[k].insert(tk.END, move_list[k])
                entry_list[k].bind("<Key>", lambda e: txtEvent(e))
                
            else:
                entry_list[k].insert(tk.END, "-")
                entry_list[k].bind("<Key>", lambda e: txtEvent(e))


    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))



if __name__ == "__main__":
    root=tk.Tk()
    heading_label = tk.Label(root, text="Login Details",font = ("Arial",18,"bold"))
    heading_label.place(height=100,width=500, x=50, y=50)

    frame = tk.Frame(root)
    frame.place(height=200,width=400, x=550, y=130)
    
    example = Example(frame)
    example.pack(side="top", fill="both", expand=True)

    setTextInput(0,"No way")
    setTextInput(13,"Ok")

    root.mainloop()