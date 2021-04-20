""" This is the central python file that will maintain two threads and verify if they are the
	same move and if they are then update gui and send the move to the other player. 
"""

""" always use loopback or ::1 or [::1] for local please """ 

import globals
from gui import main
import socket

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

def primary_main():
	networking()
	negotitiate_color()
	print(globals.color_val)
	main()
	
if __name__ == "__main__":
    primary_main()