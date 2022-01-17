#!/usr/bin/env python

"""
Dit script is onderdeel van de standaard scripts
voor de module ikcovi van de HS Leiden
"""
import PySimpleGUI as sg
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

from W2_practicum2_helperFuncties import *

__author__ = "ikcovi 21-22"
__copyright__ = "Copyright 2021, HS Leiden"
__license__ = "GPL"
__version__ = "1.0"
__email__ = "pistidda.a@hsleiden.nl"

def dothresholding(plaatje1, plaatje2 = None ):
    print("Let's go dothresholding")
    if plaatje1 is None:
        sg.popup_error('Plaatje 1 is leeg...')
        return None
    maxValue = 255

    if len(plaatje1.shape) == 3:  # Plaatje bevat kleurkanalen, niet toegestaan.
        plaatje1 = cv.cvtColor(plaatje1, cv.COLOR_BGR2GRAY)

    threshold = vraagOperatorInputThreshold("Geef threshold waarde op:",range(0, 256))
    return cv.threshold(plaatje1,threshold,maxValue,getattr(cv, 'THRESH_BINARY'))[1]

def doHistogramEnhancement (plaatje1, plaatje2 = None ):
    print("Let's go doHistogramEnhancement")
    if plaatje1 is None:
        sg.popup_error('Plaatje 1 is leeg...')
        return None

    histogramType = vraagOperatorInput("Welke histogram techniek wil je toepassen?", ["NORMALIZE", "EQUALIZE"], -1)

    if (histogramType == "NORMALIZE"):
        return normalize(plaatje1)
    elif (histogramType == "EQUALIZE"):
        return equalize(plaatje1)
    else:
        return plaatje1

def doBinaryOperators(plaatje1, plaatje2 = None ):
    print("Let's go doBinaryOperators")
    if (plaatje1 is None):
        sg.popup_error('Plaatje 1 is leeg...')
        return None

    # vraagt de gebruiker te kiezen uit 3 opties: 3,5 of 7.
    # Optie 3 is de default waarde
    gewensteOperatie = vraagOperatorInputThreshold("Kies operator type:", ["AND", "OR", "XOR", "NOT"], 1)

    if gewensteOperatie == 'NOT':
        return cv.bitwise_not(plaatje1)

    if (plaatje2 is None):
        sg.popup_error('Plaatje 2 is leeg...')
        return plaatje1

    # functies om een plaatje te openen
    if gewensteOperatie == 'AND':
        return cv.bitwise_and(plaatje1, plaatje2)

    if gewensteOperatie == 'OR':
        return cv.bitwise_or(plaatje1,plaatje2)

    if gewensteOperatie == 'XOR':
        return cv.bitwise_xor(plaatje1,plaatje2)

def doMorphology(plaatje1, plaatje2 = None ):
    print("Let's go doMorphology")
    if plaatje1 is None:
        sg.popup_error('Plaatje 1 is leeg...')
        return None

    # vraag welke operator
    operatorType = vraagOperatorInput("Welke operator wil je gebruiken?", ["Erosion", "Dilation", "Opening", "Closing"],-1)
    # dict met correcte syntax voor alle operators
    operatorSynax = {"Opening": cv.MORPH_OPEN, "Closing": cv.MORPH_CLOSE}

    # de 2 regels hieronder zorgen voor een kernel die een 1 op 1 kopie van het plaatje maakt
    # Een kernel bestaande uit alleen maar nullen met de middelste waarde van de kernel een 1
    kernelSize = 3
    kernel = np.zeros((kernelSize, kernelSize), np.uint8)
    kernel[int((kernelSize - 1) / 2)][int((kernelSize - 1) / 2)] = 1

    # deze regel laat de gebruiker een andere kernel instellen
    kernel = vraagKernelInput(kernel)

    # dit is het openCV operator die een plaatje teruggeeft.
    outputImg = None

    if operatorType == "Erosion":
        outputImg = cv.erode(plaatje1, kernel, iterations=3)
    elif operatorType == "Dilation":
        outputImg = cv.dilate(plaatje1, kernel, iterations=3)
    else:
        outputImg = cv.morphologyEx(plaatje1, operatorSynax[operatorType], kernel)

    return outputImg

def doPercentileFilterering(plaatje1, plaatje2 = None ):
    print("Let's go doPercentileFilterering")
    if plaatje1 is None:
        sg.popup_error('Plaatje 1 is leeg...')
        return None

    kernelSize = vraagOperatorInput("Wat is de grootte van de kernel?", [3, 5, 7], 0)
    median = cv.medianBlur(plaatje1, kernelSize)
    return median

def doGaussianFiltering(plaatje1, plaatje2 = None ):
    print("Let's go doGaussianFiltering")
    if plaatje1 is None:
        sg.popup_error('Plaatje 1 is leeg...')
        return None

    # vraagt de gebruiker te kiezen uit 3 opties: 3,5 of 7.
    kernelSize = vraagOperatorInput("Wat is de grootte van de kernel?", [3, 5, 7], 0)
    # Optie 3 is de default waarde
    dev = vraagOperatorInput("Wat is de standaarddeviatie", range(kernelSize*2), 2)
    return cv.GaussianBlur(plaatje1, (kernelSize, kernelSize), dev)

def doCannyEdgeDetection(plaatje1, plaatje2 = None ):
    print("Let's go doCannyEdgeDetection")
    if plaatje1 is None:
        sg.popup_error('Plaatje 1 is leeg...')
        return None

    # VERVANG ONDERSTAANDE CODE VOOR CODE DIE JOUW FUNCTIE IMPLEMENTEERT:
    img = plaatje1
    edges = cv.Canny(img, 100, 200)
    return edges

def doSobelEdgeDetectie(plaatje1, plaatje2 = None ):
    print("Let's go doSobelEdgeDetectie")
    if plaatje1 is None:
        sg.popup_error('Plaatje 1 is leeg...')
        return None

    if len(plaatje1.shape) == 3:  # Plaatje bevat kleurkanalen, niet toegestaan.
        plaatje1 = cv.cvtColor(plaatje1, cv.COLOR_BGR2GRAY)

    grad_x = cv.Sobel(plaatje1, cv.CV_16S, 1, 0, ksize=3, scale=1, delta=0, borderType=cv.BORDER_DEFAULT)
    grad_y = cv.Sobel(plaatje1, cv.CV_16S, 0, 1, ksize=3, scale=1, delta=0, borderType=cv.BORDER_DEFAULT)

    abs_grad_x = cv.convertScaleAbs(grad_x)
    abs_grad_y = cv.convertScaleAbs(grad_y)

    grad = cv.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

    return cv.filter2D(grad, -1, 3)

def doImagePyramid(plaatje1, plaatje2 = None ):
    print("Let's go doImagePyramid")
    if plaatje1 is None:
        sg.popup_error('Plaatje 1 is leeg...')
        return None

    verkleining = vraagOperatorInput("Hoevaak wil je de afbeelding verkleinen?", [1, 2, 3, 4, 5, 6,7,8,9,10], 2)

    resultaat = None
    layer = plaatje1.copy()

    for i in range(4):
        plt.subplot(2, 2, i + 1)

        # using pyrDown() function
        layer = cv.pyrDown(layer)

        if i == verkleining:
            resultaat = layer

        cv.imshow("plaatje level " + str(i), layer)

    return resultaat


def doAlgemeneConvolutie (plaatje1, plaatje2 = None ):
    print("Let's go doAlgemeneConvolutie")
    if plaatje1 is None:
        sg.popup_error('Plaatje 1 is leeg...')
        return None


    #vraagt de gebruiker te kiezen uit 3 opties: 3,5 of 7.
    #Optie 3 is de default waarde
    kernelSize = vraagOperatorInput("Wat is de grootte van de kernel?", [3,5,7], 1)

    #de 2 regels hieronder zorgen voor een kernel die een 1 op 1 kopie van het plaatje maakt
    #Een kernel bestaande uit alleen maar nullen met de middelste waarde van de kernel een 1
    kernel = np.zeros((kernelSize, kernelSize), np.float32)
    kernel[int((kernelSize-1)/2)][int((kernelSize-1)/2)] = 1

    #deze regel laat de gebruiker een andere kernel instellen
    kernel = vraagKernelInput (kernel)

    # Plaatje bevat kleurkanalen, niet toegestaan.
    if len(plaatje1.shape) == 3:
        plaatje1 = cv.cvtColor(plaatje1, cv.COLOR_BGR2GRAY)

    # dit is het openCV operator die een plaatje teruggeeft.
    return cv.filter2D(plaatje1, -1, kernel)
