import speech_recognition as sr
import globals

def sound_impl():
    r = sr.Recognizer()
    sound_found = 0
    while (sound_found < 2) :
        with sr.Microphone() as source:
            print("Talk")
            audio_text = r.listen(source,phrase_time_limit=5)
            print("Time over, thanks")
            
            s = r.recognize_google(audio_text).lower().replace(" ","")
            print("Text: " + s)
        
        sound_found = 0
        sound_k=-1
        sound_prev=-1

        for i in range(1,len(s)):
            if (sound_found >= 2): break
            if s[i]>='1' and s[i]<='8':
                if (sound_found == 0 ) :         
                    sound_prev = int(ord(s[i])-ord('1')) 
                    if (s[i-1] >= 'a' and s[i-1] <= 'h') :
                        sound_found = 1
                        sound_prev += int(8*(ord(s[i-1])-97))
                
                elif (sound_found == 1) :
                    sound_k = int(ord(s[i])-ord('1')) 
                    if (s[i-1] >= 'a' and s[i-1] <= 'h') :
                        sound_found = 2
                        sound_k += int(8*(ord(s[i-1])-97))
        
        print(sound_found+" "+sound_prev + " " + sound_k)


if __name__ == "__main__":
    sound_impl()
    
        








        
        

