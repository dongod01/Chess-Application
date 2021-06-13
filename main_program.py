""" This is the central python file that will maintain two threads and verify if they are the
	same move and if they are then update gui and send the move to the other player. 
"""

""" always use loopback or ::1 or [::1] for local please """ 

import globals
from gui import main as gui_main
import socket
import tkinter as tk
import threading 

main_window = None
bool_color = "0"
negotiated = False

def change_bool_white():
	global bool_color
	bool_color = 1

def change_bool_black():
	global bool_color
	bool_color = 2

def negotiate_color_without_name():
	global bool_color,negotiated

	bool_color = 0

	print("What color do you want ??? Please enter b/B or w/W")
	color1 = bool_color
	
	globals.my_socket.sendall(str(color1).encode())
	color2 = int(globals.my_socket.recv(1024).decode())

	if (color1 == 1 and color2 == 2):
		globals.color_val = True
		negotiated = True

	elif color1 == 2 and color2 == 1:
		globals.color_val = False
		negotiated = True


def gui_negotiate_color():
	global negotiated
	color_button.destroy()
	heading_label["text"] = "Choose Color"
	globals.my_socket.sendall(globals.name1.encode())
	globals.name2 = globals.my_socket.recv(1024).decode()

	White_Button = tk.Button(main_window,text = "WHITE",command = change_bool_white)
	White_Button.place(height=50,width=300, x=150, y=350) 

	Black_Button = tk.Button(main_window,text = "BLACK",command = change_bool_black)
	Black_Button.place(height=50,width=300, x=150, y=500)
	
	while(not negotiated):
		negotiate_color_without_name()

	threading.Thread(target=gui_main).start()

def gui_server():
	Server_button.destroy()
	Client_button.destroy()

	threading.Thread(target = make_server).start()

	heading_label["text"] = 'Server Details are IP - BLAH - BLAH - BLAH port - BLAH - BLAH - BLAH'

	global color_button
	color_button = tk.Button(main_window,text="Select Color",command = gui_negotiate_color)
	color_button.place(height=50,width=300, x=150, y=350)

def submit_client():
	server_ip = IP_Entry_Box.get()
	server_port = int(Port_Entry_Box.get())

	IP_Entry_Box.destroy()
	Port_Entry_Box.destroy()
	Client_Submit_Button.destroy()

	make_client(server_ip,server_port)

	global color_button
	color_button = tk.Button(main_window,text="Select Color",command = gui_negotiate_color)
	color_button.place(height=50,width=300, x=150, y=350)

def gui_client():
	Server_button.destroy()
	Client_button.destroy()

	heading_label["text"] = 'Please Enter the Server Details'
	player_name_label.place(height=100,width=100, x=150, y=150)

	global IP_Entry_Box
	IP_Entry_Box = tk.Entry(main_window)
	IP_Entry_Box.place(height=50,width=300, x=150, y=250)

	global Port_Entry_Box
	Port_Entry_Box = tk.Entry(main_window)
	Port_Entry_Box.place(height=50,width=300, x=150, y=350)

	global Client_Submit_Button
	Client_Submit_Button = tk.Button(main_window,text="Submit",command = submit_client)
	Client_Submit_Button.place(height=50,width=100, x=150, y=450)

def gui_networking():
	heading_label["text"] = 'Do you want to be a Server or a Client ?'
	
	global Server_button
	Server_button = tk.Button(main_window,text="Server",command = gui_server)
	Server_button.place(height=50,width=100, x=250, y=350)

	global Client_button
	Client_button = tk.Button(main_window,text="Client",command = gui_client)
	Client_button.place(height=50,width=100, x=250, y=450)


def set_name():
	globals.name1 = name_entry_widget.get()
	Enter_button.destroy()
	player_name_label["text"] = globals.name1

	name_entry_widget.destroy()
	gui_networking()


def load_gui():
	global main_window
	main_window = tk.Tk()
	main_window.title('Chess Application')
	main_window.geometry("600x600")
	main_window.resizable(False,False)

	global heading_label
	heading_label = tk.Label(main_window, text="Login Details",font = ("Arial",18,"bold"))
	heading_label.place(height=100,width=500, x=50, y=50)
	
	global player_name_label
	player_name_label =  tk.Label( main_window, text="Name",font = ("Arial",13))
	player_name_label.place(height=100,width=300, x=150, y=250)

	global name_entry_widget
	name_entry_widget = tk.Entry(main_window)
	name_entry_widget.place(height=50,width=300, x=150, y=350)
	
	global Enter_button
	Enter_button = tk.Button(main_window,text="Submit",command = set_name)
	Enter_button.place(height=50,width=100, x=250, y=450)

	print(globals.name1)

	main_window.mainloop()


def negotitiate_color():	## True is white and false is black
	print("What is your name")
	globals.name1 = input()
	globals.my_socket.sendall(globals.name1.encode())

	globals.name2 = globals.my_socket.recv(1024).decode()
	
	while (True):
		print("What color do you want ??? Please enter b/B or w/W")
		color1 = input()
		globals.my_socket.sendall(color1.encode())
		color2 = globals.my_socket.recv(1024).decode()

		if ((color1 == 'b' or color1 == 'B') and (color2 == 'w'or color2 == 'W')):
			globals.color_val = False
			break
		elif ((color1 == 'w' or color1 == 'W') and (color2 == 'b' or color2 == 'B')):
			globals.color_val = True
			break
	
def make_client(server_ip_addr,socket_port_number):
	if socket.has_ipv6:
		globals.my_socket = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
	else:
		globals.my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	globals.my_socket.connect((server_ip_addr, socket_port_number))

def make_server():
    addr = ("", 8080)  
    if socket.has_dualstack_ipv6():
        my_server_socket = socket.create_server(addr, family=socket.AF_INET6, dualstack_ipv6=True)
    else:
        my_server_socket = socket.create_server(addr)

    globals.my_socket, address = my_server_socket.accept()
	
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