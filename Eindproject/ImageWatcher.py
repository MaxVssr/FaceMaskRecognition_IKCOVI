import os
import time
import getpass
from Email import sendMail

# Deze functie kijkt naar de map waar de foto's zonder masker worden opgeslagen. In het multithreading proces wordt deze functie 
# uitgevoerd tijdens de startFaceRecognition(). Als de functie een nieuwe toevoeging in de map zit verschijnen print het "Added: *filenaam*".
# Dit is voor extra confirmation tijdens het testen.
# Hierna wordt de foto naar de functie sendMail() gestuurd als parameter genaamd 'foto'
# Als laatste wordt het script gereset door before = after zodat het script weer nieuwe veranderingen kan detecteren in de map met foto's. 
def startWatchingNoMaskFolder():
    # Definieer het pad voor de folder waar de foto's zonder masker worden opgeslagen
    path_to_watch = "D:\Oud Bureaublad\School\Hogeschool Leiden\Jaar_3\IKCOVI\Eindproject\zonderMasker"
    before = dict([(f, None) for f in os.listdir(path_to_watch)])
    while 1:
        time.sleep(5)
        after = dict([(f, None) for f in os.listdir(path_to_watch)])
        added = [f for f in after if not f in before]
        if added:
            print("Added: ", ", ".join(added))
            for file in added:
                foto = path_to_watch + "/" + file
                sendMail(foto)
        before = after