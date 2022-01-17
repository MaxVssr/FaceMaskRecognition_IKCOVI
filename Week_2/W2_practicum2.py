#!/usr/bin/env python

"""
Dit script is onderdeel van de standaard scripts
voor de module ikcovi van de HS Leiden
"""
import PySimpleGUI as sg
import cv2 as cv

from W2_practicum2_functies import *

__author__ = "Alize Pistidda"
__copyright__ = "Copyright 2021, HS Leiden"
__license__ = "GPL"
__version__ = "1.0"
__email__ = "pistidda.a@hsleiden.nl"

#initialisatie van variableen
img1 = img2 = resultaat = None
#hier kun je voor jou gemak het pad naar jouw plaatjes zetten:
baseFolder =  'C:/temp/ikcovi'

#deze worden gebruikt voor de buttons en de implemtenatie van de operators function calls
operatorList = ["thresholding", "Histogram Enhancement","Binary Operators","Morphology", "Percentile Filterering",
                "Gaussian Filtering", "Canny Edge Detection","Sobel Edge Detectie", "Image Pyramid","Algemene Convolutie"]
operatorFuncties = []
pijplijnDefault = "Selecteer Operator"
pijplijnLengte = 3

#maakt van de namen uit operatorList, functienamen voor in de key en die kunnen worden aangeroepen.
#deze functie helpt de overhead als je een nieuw filter wilt toevoegen :)
def createButton (operatorName):
    global operatorFuncties
    functieNaam = "do" + operatorName.replace(" ", "")
    operatorFuncties.append(functieNaam)
    return(sg.Button(operatorName, key =functieNaam))

#-------------------------------GUI-------------------------------------------------------------------------
# gemaakt met PySImpleGUI, Voor meer info hierover
# lees https://pysimplegui.readthedocs.io/en/latest/
# en https://pysimplegui.readthedocs.io/en/latest/call%20reference/
l_fileOpenSave = [[sg.Text('Open een file: '), sg.Button('Open plaatje 1'), sg.Button('Open plaatje 2'),
                  sg.Text('File opslaan: '), sg.Button('Sla resultaat op')]]
l_BeeldOperaties = [[sg.Text('Bewerk het plaatje: ')] +
                    [createButton(elem) for elem in operatorList]]
l_BvPijplijn = [[sg.Text('Voer de volgende operaties achter elkaar uit: ')] +
                [sg.Combo([pijplijnDefault] + operatorList, key="combo"+str(combiID), default_value=pijplijnDefault) for combiID in range(pijplijnLengte)] +
                [sg.Button('Start de Pijplijn')]]
l_imageInput = [[sg.Image(filename='', key='origineel')],[sg.Image(filename='', key='image2')]]

layout = [[sg.Column(l_fileOpenSave)],
          [sg.Column(l_BeeldOperaties)],
          [sg.Column(l_BvPijplijn)],
          [sg.Column(l_imageInput), sg.Image(filename='', key='bewerkt')]]
window = sg.Window("Operator Demo", layout)

#--------------------------BASIS OPEN & SAVE FUNCTIES ---------------------------------------------------
def readImage ():
    global baseFolder

    fname = sg.popup_get_file('Kies een plaatje om te openen', default_path=baseFolder, initial_folder=baseFolder)
    if (not fname) and (fname is None):
        sg.popup_error("Filenaam is leeg, kan plaatje niet inlezen")
        return None

    try:
        img = cv.imread(fname)
    except:
        sg.popup_error("Fout bij openen plaatje\n:" + fname);
    return img

def saveImage(plaatje):
    global baseFolder

    if plaatje is None:
        sg.popup_error("Er is niks om op te slaan")
        return

    fname = sg.popup_get_file('Save Image', default_path=baseFolder+"/resultaat.png", initial_folder=baseFolder, save_as=True, file_types=(
    ("Portable Network Graphics ", "*.png"), ("JPEG file ", "*.jpg"), ("TIFF files", "*.tiff"), ('ALL Files', '*.*')))

    if (not fname) and (fname is None):
        sg.popup_error("Filenaam is leeg, kan plaatje niet wegschrijven")
        return

    try:
        cv.imwrite(fname, plaatje)
    except:
        sg.popup_error("Fout bij opslaan van het plaatje:\n" + fname)

#--------------------------BEGIN EVENT LOOP ---------------------------------------------------

# Event Loop, wacht op "events" en lees de "values" of the inputs
while True:
    event, values = window.read(timeout=100)        # Poll every 100 ms

#    print(event)
#    print(values)

    # test of de gebruiker het window heeft afgesloten
    if event == sg.WIN_CLOSED:
        break

    #test zodat ik verderop event[0] zou kunnen gebruiken zonder foutmelding
    if not event:
        continue

    #functies om een plaatje te openen
    if event == 'Open plaatje 1':
        img1 = readImage();

    if event == 'Open plaatje 2':
        img2 = readImage();

      #functie om het resultaat op te slaan
    if event == 'Sla resultaat op':
        saveImage(resultaat)

    #operatorList
    for elem in operatorFuncties:
        if event == elem:
            #er is op een van de operatorfilters gedrukt, voor het bijbehorend filter uit
            #haal eerst even de spaties tussen de woorden weg en zet er 'do' voor:
            resultaat = eval(elem)(img1, img2)

    #pijplijn van comboboxes
    if event == "Start de Pijplijn":
        #als de eerste combo nog op default staat, stop met uitvoeren:
        if values['combo0'] == pijplijnDefault:
            sg.popup_error('Selecteer operators voor je de pijplijn gaat uitvoeren')
            continue
        else:
            functieNaam = "do" + values['combo0'].replace(" ", "")
            resultaat = eval(functieNaam)(img1, img2)

            #ga nu de andere comboboxen af en gebruik daarbij het resultaat van de vorige:
            for i in range(1,pijplijnLengte):
                if values['combo'+str(i)] == pijplijnDefault:
                    #pijplijn is klaar, we kunnen stoppen
                    continue
                else:
                    functieNaam = "do" + values['combo'+str(i)].replace(" ", "")
                    resultaat = eval(functieNaam)(resultaat, img2)

    #toon de plaatjes op het scherm
    if img1 is not None:
        window['origineel'](data=cv.imencode('.png', img1)[1].tobytes())

    if img2 is not None:
        window['image2'](data=cv.imencode('.png', img2)[1].tobytes())

    if resultaat is not None    :
        # toon de plaatjes op het scherm:
        window['bewerkt'](data=cv.imencode('.png', resultaat)[1].tobytes())

window.close()
cv.destroyAllWindows()