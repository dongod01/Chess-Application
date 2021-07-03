import speech_recognition as sr
import globals
import threading
from gui_Implementation import my_move as sound_move

def sound_impl():
    if (not globals.game_ended):
        print("the thread count at sound_impl is " + str(threading.active_count()))
        
        print(str(globals.color_val) + " " +  str(globals.move_counter))

        if (not globals.color_val and globals.move_counter == 0): return

        r = sr.Recognizer()
        sound_found = 0
        sound_flag = False

        while (not sound_flag) :
            globals.voice_label["text"] = "Not read,speak again"
            with sr.Microphone() as source:
                print("Talk")
                
                audio_text = r.listen(source,phrase_time_limit=5)
                
                print("Time over, thanks")

                x = r.recognize_google(audio_text,language = "en-IN")
                
                globals.voice_label["text"] = x
                s = x.lower().replace(" ","")
                
                print("Text: " + s)
            
            sound_found = 0
            sound_k = -1
            sound_prev = -1

            for i in range(1,len(s)):
                #p1k1p2k2p3k3
                if not sound_flag:
                    if sound_found == 2:
                        sound_found = 0
                        sound_prev = -1
                        sound_k = -1

                    if s[i]>='1' and s[i]<='8':
                        if (sound_found == 0 ) :          
                            if (s[i-1] >= 'a' and s[i-1] <= 'h') :
                                sound_prev = 8*int(ord(s[i])-ord('1'))
                                sound_found = 1
                                sound_prev += int((ord(s[i-1])-97))
                        
                        elif (sound_found == 1) :
                            if (s[i-1] >= 'a' and s[i-1] <= 'h') :
                                sound_k = 8*int(ord(s[i])-ord('1'))
                                sound_found = 2
                                sound_k += int((ord(s[i-1])-97))
                        
                if (sound_found == 2):
                    if not globals.color_val:
                        sound_k = 63 - sound_k
                        sound_prev = 63 - sound_prev
                    sound_move(sound_prev)
                    if(sound_move(sound_k)): 
                        sound_flag = True
                        break

            
            print(str(sound_found)+" "+str(sound_prev) + " " + str(sound_k))
    else :
        print("Game has ended!!!")