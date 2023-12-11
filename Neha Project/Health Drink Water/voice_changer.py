import pyttsx3 #import the library

def voiceChange():
    eng = pyttsx3.init() #initialize an instance
    voice = eng.getProperty('voices') #get the available voices
    # eng.setProperty('voice', voice[0].id) #set the voice to index 0 for male voice
    eng.setProperty('voice', voice[1].id) #changing voice to index 1 for female voice
    eng.say("This is a demonstration of how to convert index of voice using pyttsx3 library in python.") #say method for passing text to be spoken
    eng.runAndWait() #run and process the voice command

if __name__ == "__main__":
    voiceChange()


# https://www.codespeedy.com/how-to-change-voice-in-pyttsx3-in-python-male-to-female/