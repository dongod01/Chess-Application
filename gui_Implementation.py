import globals 
from helper import *

def GUI_move_impl(prev,k,prom_char,called_from):

    globals.newp = prom_char
    islegal=False
    '''If the move is legal'''
    
    print("this is "+str(prev) +" and " + str(k))
    
    if globals.color_val:
        uci = generate_uci(prev,k)
    else:
        uci = generate_uci(63-prev,63-k)

    #uci = generate_uci(prev,k)
     
    yuci = chess.Move.from_uci(uci)
    print(globals.board.legal_moves)
    
    if promotion_check(prev,k,called_from):
                
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