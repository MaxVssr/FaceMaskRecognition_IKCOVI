"""
Dit script is onderdeel van de standaard scripts
voor de module ikcovi van de HS Leiden
"""
import PySimpleGUI as sg
import numpy as np
import cv2 as cv

__author__ = "ikcovi 21-22"
__copyright__ = "Copyright 2021, HS Leiden"
__license__ = "GPL"
__version__ = "1.0"
__email__ = "pistidda.a@hsleiden.nl"


# Deze functie kan worden gebruikt door convolutie filters om aan de gebruiker
# te vragen met welk kernel er gebruikt moet worden
def vraagKernelInput(defaultKernal = np.zeros((3, 3), np.float32)):

    #default kernel: een 1 op 1 kopie van het plaatje
    kernel = defaultKernal
    kernelSize = len(defaultKernal[0])

    #hier geeft ik elke waarde in de 2D matrix een aparte key op basis van de index
    #zo kan ik daarna de waardes makkelijk weer uitlezen en in de 2D kernel plaatsen
    l_kernel = [[sg.Input(size=(5, 1),default_text=kernel[row][col],
                          key=('k' + str(kernelSize * row + col)))
                 for col in range(kernelSize)] for row in range(kernelSize)] + \
                [[sg.Submit(), sg.Cancel()]]
    window = sg.Window('Geef een kernel op', l_kernel)
    event, values = window.read()
    window.close()

    #als de gebruiker submit heeft gedrukt en dus zinnige waardes heeft ingevuld
    if event == "Submit":
        for row in range(kernelSize):
            for col in range(kernelSize):
                if values['k' + str(kernelSize * row + col)]:
                    kernel[row][col] = values['k' + str(kernelSize * row + col)]
                    #print("kernel[", row, "][", col, "] = ", kernel[row][col])
                else:
                    kernel[row][col] = 0
                    #print("kernel[", row, "][", col, "] = 0!")

    return kernel

# Deze functie vraagt de gebruiker te antwoorden op een vraag met een vast aantal opties:
# textVraag: de vraag die je de gebruiker wilt stellen
# opties: een lijst met opties, dit kunnen strings zijn, maar ook integers of floats
# idxDefault: de index van de door jou gezette defaultwaarde
def vraagOperatorInput(textVraag, opties, idxDefault=0):
    if len(opties) == 0:
        sg.popup_error(textVraag + '\n Er zijn geen opties om aan de gebruiker te vragen')
        return -1

    l_listbox = [[sg.Text(textVraag)],
                [sg.Listbox(opties, size=(20, 3), key='LB')],
                 [sg.Submit(), sg.Cancel()]]
    window = sg.Window('Gebruikers info gevraagd:', l_listbox)
    event, values = window.read()
    window.close()

    # als de gebruiker submit heeft gedrukt en dus zinnige waardes heeft ingevuld
    if event == "Submit":
        resultaat = values["LB"][0]
    else:
        #gebruik anders de defaultwaarde
        #als de index tenminste geldig is, anders geef je de eerste waarde terug
        try:
            resultaat = opties[idxDefault]
        except:
            resultaat = opties[0]

    return resultaat

#----------------------------- FUNCTIES VOOR THRESHOLDING ---------------------------------------
# Deze functie vraagt de gebruiker te antwoorden op een vraag met een vast aantal opties:
# textVraag: de vraag die je de gebruiker wilt stellen
# opties: een lijst met opties, dit kunnen strings zijn, maar ook integers of floats
# idxDefault: de index van de door jou gezette defaultwaarde
def vraagOperatorInputThreshold(textVraag, opties, idxDefault=0):
    if len(opties) == 0:
        sg.popup_error(textVraag + '\n Er zijn geen opties om aan de gebruiker te vragen')
        return -1
    input_window_name = 'Gebruikers info gevraagd:'
    input_window_name_margin = 10  # Ruimte voor de standaard vensterknoppen.
    window_text_margin = 2  # Extra witruimte rechts naast de tekst.
    maximum_listed_options = 20  # Aantal opties die tegelijkertijd zichtbare zijn in het venster.
    # Berekent hoe groot het venster moet zijn aan de hand van het aantal opties en de grootte van de langste tekst.
    l_listbox = [
        [sg.Text(textVraag)],
        [sg.Listbox(
            opties,
            size=(max(len(input_window_name) + input_window_name_margin,
                      max(len(max(map(str, opties), key=len)), len(textVraag))) +
                  window_text_margin, min(maximum_listed_options, len(opties))),
            key='LB',
            font='Consolas 10',
        )],
        [sg.Submit(), sg.Cancel()],
    ]
    window = sg.Window(input_window_name, l_listbox)
    event, values = window.read()
    window.close()

    # als de gebruiker submit heeft gedrukt en dus zinnige waardes heeft ingevuld
    if event == "Submit":
        resultaat = values["LB"][0]
    else:
        #gebruik anders de defaultwaarde
        #als de index tenminste geldig is, anders geef je de eerste waarde terug
        try:
            resultaat = opties[idxDefault]
        except:
            resultaat = opties[0]

    return resultaat


def simple_thresholding(afbeelding, max_value):
    thresh = vraagOperatorInputThreshold(
        "Geef threshold waarde op:",
        range(0, 256),
    )
    thresholdType = vraagOperatorInputThreshold(
        "Kies thresholtype:",
        (
            'THRESH_BINARY',
            'THRESH_BINARY_INV',
            'THRESH_TRUNC',
            'THRESH_TOZERO',
            'THRESH_TOZERO_INV',
        ),
    )
    return cv.threshold(
        afbeelding,
        thresh,
        max_value,
        getattr(cv, 'THRESH_BINARY')
    )[1]

def adaptive_thresholding(afbeelding, max_value):
    adaptiveMethod = vraagOperatorInputThreshold(
        "Kies adaptieve methode:",
        (
            'ADAPTIVE_THRESH_MEAN_C',
            'ADAPTIVE_THRESH_GAUSSIAN_C',
        ),
    )
    thresholdType = vraagOperatorInputThreshold(
        "Kies thresholtype:",
        (
            'THRESH_BINARY',
            'THRESH_BINARY_INV',
        ),
    )
    blockSize = vraagOperatorInputThreshold(
        "Geef getal op voor het [getal] x [getal] buurpixelraster:",
        range(3, 202, 2),
    )
    C = vraagOperatorInputThreshold(
        "Geef correctiewaarde op dat van de berekende mediaan wordt afgetrokken:",
        range(0, 201),
    )
    return cv.adaptiveThreshold(
        afbeelding,
        max_value,
        getattr(cv, adaptiveMethod),
        getattr(cv, thresholdType),
        blockSize,
        C,
    )


def threshold_operator(afbeelding):
    maxValue = 255
    if len(afbeelding.shape) == 3:  # Plaatje bevat kleurkanalen, niet toegestaan.
        afbeelding = cv.cvtColor(afbeelding, cv.COLOR_BGR2GRAY)
    threshold_functies = {
        'Simple Thresholding': simple_thresholding,
        'Adaptive Thresholding': adaptive_thresholding,
        "Otsu's Thresholding": otsu_thresholding,
    }
    threshold_algoritme = vraagOperatorInputThreshold(
        "Kies threshold algoritme:",
        tuple(threshold_functies.keys()),
    )
    return threshold_functies[threshold_algoritme](afbeelding, maxValue)

#----------------------------- FUNCTIES VOOR HISTOGRAM NORMALISATIE _ EQUALISATIE--------------------

def normalize (plaatje1, plaatje2 = None ): # NORMALIZE
    print("NORMALIZING")
    if plaatje1 is None:
        sg.popup_error('Plaatje 1 is leeg...')
        return None

    if len(plaatje1.shape) == 3:  # Plaatje bevat kleurkanalen, niet toegestaan.
        src = cv.cvtColor(plaatje1, cv.COLOR_BGR2GRAY)

    norm_image = cv.normalize(src, src, 0, 255, cv.NORM_MINMAX)

    return norm_image

def equalize (plaatje1, plaatje2 = None ): # EQUALZE
    print("EQUALIZING")
    if plaatje1 is None:
        sg.popup_error('Plaatje 1 is leeg...')
        return None

    if len(plaatje1.shape) == 3:  # Plaatje bevat kleurkanalen, niet toegestaan.
        src = cv.cvtColor(plaatje1, cv.COLOR_BGR2GRAY)
    print(src)

    equ = cv.equalizeHist(src)

    return equ

def equalizeCustom (plaatje1, plaatje2 = None ): # EQUALIZE CUSTOM
    if plaatje1 is None:
        sg.popup_error('Plaatje 1 is leeg...')
        return None

    plt.hist(plaatje1.ravel(), 256, [0, 256])
    src = cv.cvtColor(plaatje1, cv.COLOR_BGR2GRAY)
    plt.hist(src.ravel(), 256, [0, 256])

    height, width = src.shape

    pixelCount = height * width
    countPerIntensity = {}
    cumProbPerIntensity = {}

    for y in range(0, height):
        for x in range(0, width):
            if (src[y, x] in countPerIntensity):
                countPerIntensity[src[y, x]] += 1
            else:
                countPerIntensity[src[y, x]] = 1

    for intensity in countPerIntensity:
        totalCount = 0

        for i in countPerIntensity:
            if (i <= intensity):
                totalCount += countPerIntensity[i]

        cumProbPerIntensity[intensity] = totalCount / pixelCount

    for y in range(0, height):
        for x in range(0, width):
            if (src[y, x] in cumProbPerIntensity):
                src[y, x] = floor(cumProbPerIntensity[src[y, x]] * 256)
            else:
                src[y, x] = 0

    plt.hist(src.ravel(), 256, [0, 256])
    # plt.show()

    return src
