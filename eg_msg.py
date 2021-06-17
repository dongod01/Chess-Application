from tkinter import *
from tkinter import ttk

send_y = 70

def main():

    window =Tk()
    window.geometry("780x600")
    window.configure(bg="#b3b6ba")
    window.resizable(False,False)
    window.bind('<Return>',lambda event:send())


    # create a main frame

    main_frame=Frame(window,height=565,width=780)
    main_frame.place(x=0,y=0)
    main_frame.propagate(False)

    # create a canvas

    my_canvas=Canvas(main_frame)
    my_canvas.pack(side=LEFT,fill=BOTH,expand=1)

    # Add a scrollbar

    my_scrollbar=ttk.Scrollbar(main_frame,orient=VERTICAL,command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT,fill=Y)


    # Configure the canvas

    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind("<Configure>",lambda e:my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    # create another frame inside the canvas

    second_frame=Frame(my_canvas,bg="pink",height=10,width=10)

    # add that frame to a window in the canvas

    my_canvas.create_window((0,0),window=second_frame,anchor="nw")

    testlabel = Label(second_frame, width=0, text="blah blah blah", anchor=NW, justify=LEFT, bg="black", fg="white",
                          padx=0, pady=0, font=('helvetica', 12), wraplength=235)

    def send():
        global send_y
        
        send_msgLabel = Label(second_frame, width=0, textvariable=send_msg, anchor=NW, justify=LEFT, bg="black", fg="white",
                              padx=0, pady=0, font=('helvetica', 12), wraplength=235)
        
        send_msg.set(msg_entry.get())
        send_msgLabel.configure(textvariable=send_msg.get())
        msg_entry.delete(0, END)

        send_msgLabel.pack()

        window.update_idletasks()
        my_canvas.configure(scrollregion=my_canvas.bbox("all"))



        #send_msgLabel.place(x=0, y=send_y)
        send_y += send_msgLabel.winfo_reqheight()+10
        
        my_canvas.yview_moveto('1.0')
        my_canvas.configure(scrollregion=my_canvas.bbox("all"))
        
        #print(my_scrollbar.delta(10,20))
        #my_scrollbar.set(0,1.0)

    msg_entry = Entry(window,width=62,font=("helvetica",14))
    msg_entry.pack()
    msg_entry.place(x=10,y=565)

    send_msg=StringVar()

    send_butt=Button(text="Send",relief=GROOVE,width=9,command=send)
    send_butt.pack()
    send_butt.place(x=700,y=565)

    window.mainloop()

if __name__ == '__main__':
    main()