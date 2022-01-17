from threading import Thread
from Email import setEmailData
from ImageWatcher import startWatchingNoMaskFolder
from FaceMaskRecognition import startFaceRecognition

if __name__ == "__main__":
    setEmailData() # Functie uit Email.py om de sender email, password van de sender en receiver email te definieren
    t1 = Thread(target=startWatchingNoMaskFolder)   # definieer een thread waarbij de functie startWatchingNoMaskFolder gestart. Deze staat in de ImageWatcher.py
                                                    # Deze kijkt naar nieuwe toevoegingen in de map, het gaat hierbij om de foto's.
    t1.setDaemon(True)
    t1.start() # start de thread voor de functie startWatchingNoMaskFolder
    startFaceRecognition() #start de face mask recognition