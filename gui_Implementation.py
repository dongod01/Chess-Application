import globals 
from helper import *

def resigned():
    global resign_window
    resign_window.destroy()
    resultant_string = "Resign_Accepted"
    globals.resign_draw_socket.sendall(resultant_string.encode())
    
    globals.name_label3["text"] = " You win by resignation :)"
    if globals.color_val:
        globals.game.headers["Result"] = "1-0"
    else:
        globals.game.headers["Result"] = "0-1"
    
    addPGNbutton()
    globals.game_ended = True
    print("Game has ended!!!")

def initiate_resign():
    print("\nThe other person has resigned !!!!\n")
    
    global resign_window
    resign_window = tk.Toplevel(globals.window)
    resign_window.geometry("300x200")

    label = tk.Label(resign_window,text = "Your Opponent has resigned!!")
    label.place(height=70,width=250,x=25,y=5)

    button1 = tk.Button(resign_window,text = "End Game" , command = resigned)
    button1.place(height=50,width=80, x=110, y=120)

def accepted():
    global draw_window
    draw_window.destroy()
    resultant_string = "Draw_Accepted"
    globals.resign_draw_socket.sendall(resultant_string.encode())
    globals.name_label3["text"] = " Draw by agreement"
    globals.game.headers["Result"] = "1/2-1/2"
    globals.game_ended = True
    addPGNbutton()
    print("Game has ended!!!")

def rejected():
    global draw_window
    draw_window.destroy()
    resultant_string = "Draw_Rejected"
    globals.resign_draw_socket.sendall(resultant_string.encode())

def initiate_draw():
    print("\nThe other person wants to draw !!!!\n")
    global draw_window
    draw_window = tk.Toplevel(globals.window)
    draw_window.geometry("300x200")

    label = tk.Label(draw_window,text = "Your Opponent has offered a draw!!")
    label.place(height=80,width=250,x=25,y=5)

    button1 = tk.Button(draw_window,text = "Accept" , command = accepted)
    button1.place(height=40,width=80, x=110, y=90)

    button2 = tk.Button(draw_window,text = "Reject" , command = rejected)
    button2.place(height=40,width=80, x=110, y=150)

def wait_for_resign_or_draw_event():
    while True:
        try:
            temp_str = globals.resign_draw_socket.recv(1024).decode()
        except Exception as e: 
            print(e)
            
            # Always the client connects to the server so if the connection is broken the server should
            # wait while the client should try to reconnect
            
            if (globals.is_client): globals.resign_draw_socket.connect((globals.other_ip_address,8080))
            else : time.sleep(3)
            
            continue    

        if (temp_str == "Resigning"):
            initiate_resign()
        elif (temp_str == "Drawing"):
            initiate_draw()

def others_move():
    globals.name_label3["text"] = "Match Ongoing"

    if (not globals.game_ended):
        globals.lock
        globals.lock.acquire()
        try:
            str_other = globals.my_socket.recv(1024).decode()
            if (len(str_other) == 1) :
                if (str_other == '1') :
                    initiate_resign()
                elif (str_other == "0") :
                    initiate_draw()
            else :            
                str1,str2,str3 = str_other.split(',')
                
                prev = 63 - int(str1)
                k = 63 - int(str2)
                    
                print("this is in others move " + str(prev) + "  " + str(k))
                print("the thread count is " + str(threading.active_count()))
                GUI_move_impl(prev,k,str3,False)

                globals.move_counter+=1

                globals.name_label4["text"] = "Your Move"

        finally:
            globals.lock.release()

def my_move(k):
    if not globals.game_ended:
        if globals.x:
            ind4 = globals.chess_list.index(k)
            if (ind4 in range(0,16)):   
                globals.prev = k
                print(k)
                globals.button_list[k].configure(bg = 'green')
            else:
                globals.x = not globals.x

        else:
            print(k)
            # Handling the case when sam==e square is clicked twice
            if k==globals.prev and (k//8+k%8)%2==0:
                globals.button_list[k].configure(bg = '#8af542')
            elif k==globals.prev and (k//8+k%8)%2!=0:
                globals.button_list[k].configure(bg = 'white')

            else: 
                if ((globals.move_counter%2 == 1 and not globals.color_val) or (globals.move_counter % 2 == 0 and globals.color_val)):
                    globals.name_label3["text"] = "Match Ongoing"
                    ret1,ret2 = GUI_move_impl(globals.prev,k,'t',True)       

                    if(ret1):
                        globals.name_label4["text"] = "Opponent's Move"
                        reinstate_color(globals.prev)
                        reinstate_color(k)
                        globals.move_counter+=1
                        send_move(globals.prev,k,ret2)
                        threading.Thread(target=others_move).start()
                        
                        globals.prev = -1

        globals.x = not globals.x
        
        if (globals.x and ret1) : return ret1   

def GUI_move_impl(prev,k,prom_char,called_from):

    globals.newp = prom_char
    islegal=False
    '''If the move is legal'''
    
    print("this is "+str(prev) +" and " + str(k))
    
    if globals.color_val:
        uci = generate_uci(prev,k)
    else:
        uci = generate_uci(63-prev,63-k)
     
    yuci = chess.Move.from_uci(uci)
    print(globals.board.legal_moves)

    if promotion_check(prev,k,called_from):
        uci1 = uci + 'q'
        yuci1 = chess.Move.from_uci(uci1)
        if yuci1 in globals.board.legal_moves:

            print("Inside promotion check")
            if (prom_char == 't'):
                call_message_box()    
                globals.window.wait_window(globals.pop)     # the function waits for the other window to close

                if globals.newp=='q' and globals.color_val:
                        assign_new_piece(globals.button_list[prev],"alpha/wq.png")
                elif globals.newp=='r' and globals.color_val:
                        assign_new_piece(globals.button_list[prev],"alpha/wr.png")
                elif globals.newp=='b' and globals.color_val:
                        assign_new_piece(globals.button_list[prev],"alpha/wb.png")
                elif globals.newp=='n' and globals.color_val:
                        assign_new_piece(globals.button_list[prev],"alpha/wn.png")
                elif globals.newp=='q' and not globals.color_val:
                        assign_new_piece(globals.button_list[prev],"alpha/bq.png")
                elif globals.newp=='r' and not globals.color_val:
                        assign_new_piece(globals.button_list[prev],"alpha/br.png")
                elif globals.newp=='b' and not globals.color_val:
                        assign_new_piece(globals.button_list[prev],"alpha/bb.png")
                elif globals.newp=='n' and not globals.color_val:
                        assign_new_piece(globals.button_list[prev],"alpha/bn.png")
                uci += globals.newp
            else:
                uci += prom_char
                if prom_char=='q' and not globals.color_val:
                        assign_new_piece(globals.button_list[prev],"alpha/wq.png")
                elif prom_char=='r' and not globals.color_val:
                        assign_new_piece(globals.button_list[prev],"alpha/wr.png")
                elif prom_char=='b' and not globals.color_val:
                        assign_new_piece(globals.button_list[prev],"alpha/wb.png")
                elif prom_char=='n' and not globals.color_val:
                        assign_new_piece(globals.button_list[prev],"alpha/wn.png")
                elif prom_char=='q' and globals.color_val:
                        assign_new_piece(globals.button_list[prev],"alpha/bq.png")
                elif prom_char=='r' and globals.color_val:
                        assign_new_piece(globals.button_list[prev],"alpha/br.png")
                elif prom_char=='b' and globals.color_val:
                        assign_new_piece(globals.button_list[prev],"alpha/bb.png")
                elif prom_char=='n' and globals.color_val:
                        assign_new_piece(globals.button_list[prev],"alpha/bn.png")
            
            exchange_piece(globals.button_list[prev],globals.button_list[k])
        
            try:
                # Index of capturing piece
                ind1 = globals.chess_list.index(prev, 0, len(globals.chess_list))
                
            except ValueError:
                print("No piece in initial index in move function of promotion")
            
            # Index of captured piece
            ind2 = globals.chess_list.index(k, 0, len(globals.chess_list)) if k in globals.chess_list else -1
            globals.chess_list[ind1] = k

            if ind2!=-1:
                globals.chess_list[ind2] = -1  #Making the captured piece -1 in chesslist
            
        
            islegal=True

            globals.node = globals.node.add_variation(chess.Move.from_uci(uci))
            
            current_move = globals.board.san(chess.Move.from_uci(uci))
            globals.move_list.append(current_move)
            globals.moves_table.set_Move_List_Cell(globals.move_counter,current_move)

            globals.board.push_san(uci)

            print(globals.chess_list)
            print(globals.board)           

    elif yuci in globals.board.legal_moves:
            
        # First piece move
        
        print("Verifying move:")
        
        '''Standard algebraic notation san'''
        
        if (globals.board.is_castling(yuci)):
            # Works fine
            # 4 cases white-black and short castle-long castle
            # True indicates white's turn'
            
            # These two checks work to include the case when the rook is clicked for castling
            if 	 (k == 0 or k == 56):
                k+=2

            elif (k == 7 or k == 63): 	
                k-=1  

            alpha = globals.board.san(yuci)
            exchange_piece(globals.button_list[prev],globals.button_list[k])
            print("Inside castling")
            
            if alpha=="O-O" and globals.board.turn==True and globals.color_val:
                exchange_piece(globals.button_list[7],globals.button_list[5])
                globals.chess_list[7] = 5
            elif alpha=="O-O" and globals.board.turn==True and not globals.color_val:
                exchange_piece(globals.button_list[56],globals.button_list[58])
                globals.chess_list[24] = 58
            elif alpha=="O-O" and globals.board.turn==False and globals.color_val:
                exchange_piece(globals.button_list[63],globals.button_list[61])
                globals.chess_list[31] = 61
            elif alpha=="O-O" and globals.board.turn==False and not globals.color_val:
                exchange_piece(globals.button_list[0],globals.button_list[2])
                globals.chess_list[0] = 2
            elif alpha=="O-O-O" and globals.board.turn==True and globals.color_val:
                exchange_piece(globals.button_list[0],globals.button_list[3])
                globals.chess_list[0] = 3
            elif alpha=="O-O-O" and globals.board.turn==True and not globals.color_val:
                exchange_piece(globals.button_list[63],globals.button_list[60])
                globals.chess_list[31] = 60
            elif alpha=="O-O-O" and globals.board.turn==False and globals.color_val:
                exchange_piece(globals.button_list[56],globals.button_list[59]) 
                globals.chess_list[24] = 59
            elif alpha=="O-O-O" and globals.board.turn==False and not globals.color_val:
                exchange_piece(globals.button_list[7],globals.button_list[4])
                globals.chess_list[7] = 4
             

        elif globals.board.is_en_passant(yuci):
            # Works fine
            exchange_piece(globals.button_list[prev],globals.button_list[k])
            print("Inside en passant")
            mod = (k-prev)%8
            if mod==7:
                mod = -1
            
            delpawn = prev + mod
            print("Deleting")
            remove_piece(globals.button_list[delpawn])
            
            ind_del = globals.chess_list.index(delpawn)
            globals.chess_list[ind_del] = -1
        
        elif globals.board.is_capture(yuci):
            exchange_piece(globals.button_list[prev],globals.button_list[k])
            print("Okok")
        
        else:
            exchange_piece(globals.button_list[prev],globals.button_list[k])
            print("Xyz")

        if(globals.move_counter==0):
            globals.node = globals.game.add_variation(yuci)
        else:
            globals.node = globals.node.add_variation(yuci)
        
        current_move = globals.board.san(yuci)
        globals.move_list.append(current_move)
        globals.moves_table.set_Move_List_Cell(globals.move_counter,current_move)

        globals.board.push_san(uci)
        print(globals.board)
        islegal=True
        
        try:
            # Index of capturing piece
            ind1 = globals.chess_list.index(prev, 0, len(globals.chess_list))
            
        except ValueError:
            print("No piece in initial index in move function")
        
        # Index of captured piece
        ind2 = globals.chess_list.index(k, 0, len(globals.chess_list)) if k in globals.chess_list else -1
        globals.chess_list[ind1] = k

        if ind2!=-1:
            globals.chess_list[ind2] = -1  #Making the captured piece -1 in chesslist

        print(globals.chess_list)

    position_checker(called_from)

    return islegal,globals.newp