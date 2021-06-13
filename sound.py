import speech_recognition as sr
import globals
import threading
from gui_Implementation import my_move as sound_move

preferred_text = [("a1",1),("a2",1),("a3",1),("a4",1),("a5",1),("a6",1),("a7",1),("a8",1),
                  ("b1",1),("b2",1),("b3",1),("b4",1),("b5",1),("b6",1),("b7",1),("b8",1),
                  ("c1",1),("c2",1),("c3",1),("c4",1),("c5",1),("c6",1),("c7",1),("c8",1),
                  ("d1",1),("d2",1),("d3",1),("d4",1),("d5",1),("d6",1),("d7",1),("d8",1),
                  ("e1",1),("e2",1),("e3",1),("e4",1),("e5",1),("e6",1),("e7",1),("e8",1),
                  ("f1",1),("f2",1),("f3",1),("f4",1),("f5",1),("f6",1),("f7",1),("f8",1),
                  ("g1",1),("g2",1),("g3",1),("g4",1),("g5",1),("g6",1),("g7",1),("g8",1),
                  ("h1",1),("h2",1),("h3",1),("h4",1),("h5",1),("h6",1),("h7",1),("h8",1), ]

preferred_text_string = ["a1","a2","a3","a4","a5","a6","a7","a8",
                         "b1","b2","b3","b4","b5","b6","b7","b8",
                        "c1","c2","c3","c4","c5","c6","c7","c8",
                        "d1","d2","d3","d4","d5","d6","d7","d8",
                        "e1","e2","e3","e4","e5","e6","e7","e8",
                        "f1","f2","f3","f4","f5","f6","f7","f8",
                        "g1","g2","g3","g4","g5","g6","g7","g8",
                        "h1","h2","h3","h4","h5","h6","h7","h8" ]

def sound_impl():
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