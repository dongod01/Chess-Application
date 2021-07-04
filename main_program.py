""" This is the central python file that will maintain two threads and verify if they are the
    same move and if they are then update gui and send the move to the other player. 
"""

""" always use loopback or ::1 or [::1] for local please """ 
from helper import PGN_init
import os
import globals
from gui import main as gui_main
import socket
import tkinter as tk
import threading 

count_connected_clients = 0

def negotiate_color_without_name():
    global negotiated
    negotiated = False
    
    print("What color do you want ??? Please enter b/B or w/W inside function")
    color1 = color_entry_box.get()
    globals.game_socket.sendall(color1.encode())
    color2 = globals.game_socket.recv(1024).decode()

    if ((color1[0] == 'b' or color1[0] == 'B') and (color2[0] == 'w'or color2[0] == 'W')):
            globals.color_val = False
            negotiated = True

    elif ((color1[0] == 'w' or color1[0] == 'W') and (color2[0] == 'b' or color2[0] == 'B')):
            globals.color_val = True
            negotiated = True
    
    if (negotiated):
        PGN_init()
        if globals.color_val:
            globals.game.headers["White"] = globals.name1
            globals.game.headers["Black"] = globals.name2
        else:
            globals.game.headers["White"] = globals.name2
            globals.game.headers["Black"] = globals.name1
        
        player_name_label.destroy()
        color_entry_box.destroy()
        Submit_Button.destroy()
        heading_label.place(height=400,width=550, x=25, y=0)
        
        if globals.color_val:
            heading_label["text"] = "Game:\n" + str(globals.name1) + "\n(White)\n vs \n(Black)\n" + str(globals.name2)
        else:
            heading_label["text"] = "Game:\n" + str(globals.name2) + "\n(White)\n vs \n(Black)\n" + str(globals.name1)
        
        details_label = tk.Label(globals.main_window,font = ("Arial",14))
        details_label.place(height=300,width=550, x=25, y=300)
        
        ip1 = globals.game_socket.getsockname()
        ip2 = globals.game_socket.getpeername()

        #ip3 = globals.resign_draw_socket.getsockname()
        #ip4 = globals.resign_draw_socket.getpeername()

        details_label["text"] = "My IP Address: " + str(ip1[0]) + "\n Port: " + str(ip1[1]) + "\n\nOpponent's IP Address: " + str(ip2[0]) + "\n Port: " + str(ip2[1])
        #print("My Resign Address: " + str(ip3[0]) + "\n Port: " + str(ip3[1]) + "\n\nOpponent's Resign Address: " + str(ip4[0]) + "\n Port: " + str(ip4[1]))

        gui_main()

def gui_negotiate_color():
    if (count_connected_clients):
        global negotiated
    
        color_button.destroy()
        heading_label["text"] = "Choose Color"
        globals.game_socket.sendall(globals.name1.encode())
        globals.name2 = globals.game_socket.recv(1024).decode()

        global color_entry_box
        color_entry_box = tk.Entry(globals.main_window)
        color_entry_box.place(height=50,width=300, x=150, y=350) 

        global Submit_Button
        Submit_Button = tk.Button(globals.main_window,text = "Submit",command = negotiate_color_without_name)
        Submit_Button.place(height=50,width=300, x=150, y=500)

def gui_negotiate_color_server_wrapper():
    if (count_connected_clients > 0):
        gui_negotiate_color()
    else :
        print("the client has not connected wait")

def gui_server():
    globals.is_client = False
    Server_button.destroy()
    Client_button.destroy()
    
    threading.Thread(target = make_server).start()

    global color_button
    color_button = tk.Button(globals.main_window,text="Select Color",command = gui_negotiate_color_server_wrapper)
    color_button.place(height=50,width=300, x=150, y=350)

def submit_client():
    globals.other_ip_address = server_ip = IP_Entry_Box.get()
    server_port = int(Port_Entry_Box.get())

    IP_Entry_Box.destroy()
    Port_Entry_Box.destroy()
    Client_Submit_Button.destroy()

    make_client(server_ip,server_port)

    global color_button
    color_button = tk.Button(globals.main_window,text="Select Color",command = gui_negotiate_color)
    color_button.place(height=50,width=300, x=150, y=350)

def gui_client():
    globals.is_client = True
    Server_button.destroy()
    Client_button.destroy()

    heading_label["text"] = 'Please Enter the Server Details'
    player_name_label.place(height=100,width=100, x=150, y=150)

    global IP_Entry_Box
    IP_Entry_Box = tk.Entry(globals.main_window)
    IP_Entry_Box.place(height=50,width=300, x=150, y=250)

    global Port_Entry_Box
    Port_Entry_Box = tk.Entry(globals.main_window)
    Port_Entry_Box.place(height=50,width=300, x=150, y=350)

    global Client_Submit_Button
    Client_Submit_Button = tk.Button(globals.main_window,text="Submit",command = submit_client)
    Client_Submit_Button.place(height=50,width=100, x=150, y=450)

def gui_networking():
    heading_label["text"] = 'Do you want to be a Server or a Client ?'
    
    global Server_button
    Server_button = tk.Button(globals.main_window,text="Server",command = gui_server)
    Server_button.place(height=50,width=100, x=250, y=350)

    global Client_button
    Client_button = tk.Button(globals.main_window,text="Client",command = gui_client)
    Client_button.place(height=50,width=100, x=250, y=450)

def set_name():
    globals.name1 = name_entry_widget.get()
    Enter_button.destroy()
    player_name_label["text"] = globals.name1

    name_entry_widget.destroy()
    #player_name_label.destroy()
    gui_networking()

def load_gui():
    globals.main_window = tk.Tk()
    globals.main_window.title('Chess Application')
    globals.main_window.geometry("600x600")
    globals.main_window.resizable(False,False)

    global heading_label
    heading_label = tk.Label(globals.main_window, text="Login Details",font = ("Arial",18,"bold"))
    heading_label.place(height=100,width=500, x=50, y=50)
    
    global player_name_label
    player_name_label =  tk.Label( globals.main_window, text="Name",font = ("Arial",13))
    player_name_label.place(height=100,width=300, x=150, y=250)

    global name_entry_widget
    name_entry_widget = tk.Entry(globals.main_window)
    name_entry_widget.place(height=50,width=300, x=150, y=350)
    
    global Enter_button
    Enter_button = tk.Button(globals.main_window,text="Submit",command = set_name)
    Enter_button.place(height=50,width=100, x=250, y=450)

    print(globals.name1)

    globals.main_window.mainloop()

def negotitiate_color():	## True is white and false is black
    print("What is your name")
    globals.name1 = input()
    globals.game_socket.sendall(globals.name1.encode())

    globals.name2 = globals.game_socket.recv(1024).decode()
    
    while (True):
        print("What color do you want ??? Please enter b/B or w/W")
        color1 = input()
        globals.game_socket.sendall(color1.encode())
        color2 = globals.game_socket.recv(1024).decode()

        if ((color1 == 'b' or color1 == 'B') and (color2 == 'w'or color2 == 'W')):
            globals.color_val = False
            break
        elif ((color1 == 'w' or color1 == 'W') and (color2 == 'b' or color2 == 'B')):
            globals.color_val = True
            break
    
def make_client(server_ip_addr,socket_port_number):
    global count_connected_clients
    if socket.has_ipv6:
        globals.game_socket = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
        globals.resign_draw_socket_recieving = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
        globals.resign_draw_socket_sending = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
    else:
        globals.game_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        globals.resign_draw_socket_recieving = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        globals.resign_draw_socket_sending = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try:
        globals.game_socket.connect((server_ip_addr, socket_port_number))
        globals.resign_draw_socket_recieving.connect((server_ip_addr, socket_port_number))
        globals.resign_draw_socket_sending.connect((server_ip_addr, socket_port_number))

        count_connected_clients += 3
    except:
        count_connected_clients = 0

def make_server():
    global count_connected_clients
    addr = ("", 8080)  
    
    if socket.has_dualstack_ipv6():
        globals.my_server_socket = socket.create_server(addr, family=socket.AF_INET6, dualstack_ipv6=True)
    else:
        globals.my_server_socket = socket.create_server(addr)

    globals.game_socket, _ = globals.my_server_socket.accept()
    globals.resign_draw_socket_sending, _ = globals.my_server_socket.accept()
    globals.resign_draw_socket_recieving,_ = globals.my_server_socket.accept()
 
    if (globals.game_socket != None and globals.resign_draw_socket_recieving != None and globals.resign_draw_socket_sending != None): 
        count_connected_clients += 3
        heading_label["text"] = "Host: " + str(globals.game_socket.getsockname()[0]) + "\n\nIP address: " + str(globals.game_socket.getsockname()[1])

def networking():
    print("Enter 1 to make yourself a server or 2 to make yourself a client")
    val = int(input())

    if (val==1):
        make_server()
    elif (val==2):
        print("Enter server ip address and port number")
        ip = input()
        port = int(input())
        make_client(ip,port)
    
if __name__ == "__main__":
    load_gui()