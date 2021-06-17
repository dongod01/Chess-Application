""" This is the central python file that will maintain two threads and verify if they are the
	same move and if they are then update gui and send the move to the other player. 
"""

""" always use loopback or ::1 or [::1] for local please """ 

import globals
from gui import main as gui_main
import socket
import tkinter as tk
import threading 

def negotiate_color_without_name():
	global negotiated
	negotiated = False
	
	print("What color do you want ??? Please enter b/B or w/W inside function")
	color1 = color_entry_box.get()
	globals.my_socket.sendall(color1.encode())
	color2 = globals.my_socket.recv(1024).decode()

	if ((color1 == 'b' or color1 == 'B') and (color2 == 'w'or color2 == 'W')):
			globals.color_val = False
			negotiated = True

	elif ((color1 == 'w' or color1 == 'W') and (color2 == 'b' or color2 == 'B')):
			globals.color_val = True
			negotiated = True
	
	if (negotiated):
		if globals.color_val:
			globals.game.headers["White"] = globals.name1
			globals.game.headers["Black"] = globals.name2
		else:
			globals.game.headers["White"] = globals.name2
			globals.game.headers["Black"] = globals.name1
		
		player_name_label.destroy()
		color_entry_box.destroy()
		Submit_Button.destroy()
		heading_label.place(height=400,width=500, x=50, y=0)
		if globals.color_val:
			heading_label["text"] = "Game:\n" + str(globals.name1) + "\n(White)\n vs \n(Black)\n" + str(globals.name2)
		else:
			heading_label["text"] = "Game:\n" + str(globals.name2) + "\n(White)\n vs \n(Black)\n" + str(globals.name1)
		
		details_label = tk.Label(globals.main_window, text="Hey",font = ("Arial",14))
		details_label.place(height=300,width=500, x=50, y=350)
		hostname = socket.gethostname()
		#ip1, port1 = globals.my_socket.getsockname()
		#ip2, port2 = globals.my_socket.getpeername()
		ip_address = socket.gethostbyname(hostname)
		#details_label["text"] = "Server IP Address: " + str(ip1) + "\n Port: " + str(port1) + "\nClient IP Address: " + str(ip2) + "\n Port: " + str(port2)


		threading.Thread(target = gui_main).start()

def gui_negotiate_color():
	global negotiated
	
	color_button.destroy()
	heading_label["text"] = "Choose Color"
	globals.my_socket.sendall(globals.name1.encode())
	globals.name2 = globals.my_socket.recv(1024).decode()

	global color_entry_box
	color_entry_box = tk.Entry(globals.main_window)
	color_entry_box.place(height=50,width=300, x=150, y=350) 

	global Submit_Button
	Submit_Button = tk.Button(globals.main_window,text = "Submit",command = negotiate_color_without_name)
	Submit_Button.place(height=50,width=300, x=150, y=500)


def gui_server():
	Server_button.destroy()
	Client_button.destroy()

	threading.Thread(target = make_server).start()
	hostname = socket.gethostname()
	ip_address = socket.gethostbyname(hostname)
	heading_label["text"] = "Host: " + str(hostname) + "\nIP address: " + str(ip_address)

	global color_button
	color_button = tk.Button(globals.main_window,text="Select Color",command = gui_negotiate_color)
	color_button.place(height=50,width=300, x=150, y=350)

def submit_client():
	server_ip = IP_Entry_Box.get()
	server_port = int(Port_Entry_Box.get())

	IP_Entry_Box.destroy()
	Port_Entry_Box.destroy()
	Client_Submit_Button.destroy()

	make_client(server_ip,server_port)

	global color_button
	color_button = tk.Button(globals.main_window,text="Select Color",command = gui_negotiate_color)
	color_button.place(height=50,width=300, x=150, y=350)

def gui_client():
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