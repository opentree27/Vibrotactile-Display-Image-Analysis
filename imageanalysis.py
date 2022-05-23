import cv2
import numpy as np
from matplotlib import image, pyplot as plt
import usbcontroller,usbcontrollertest, time


def convertimage(filename,debug=False):
    start = time.time()

    #Taxel array count
    resolution = (16,16)

    #Load image
    image = cv2.imread(filename)

    #Converting to gray scale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #Resize Image
    image = cv2.resize(image, resolution)

    #Remove noise and edge detect
    taxelarray = cv2.Canny(image,200,400)

    #Set all active taxels to 1
    taxelarray[taxelarray > 1] = 1 


    
    ###################################################
    if debug:
        #Taxel plot
        fig, ax = plt.subplots()

        ax.matshow(taxelarray, cmap = 'gray')

        for i in range(resolution[0]):
            for j in range(resolution[1]):
                c = taxelarray[j,i]
                ax.text(i, j, str(c), va='center', ha='center')
        plt.show()

        #USB Test
        print('usbtest: ')
        usbcontrollertest.testusb(taxelarray)
    ####################################################


    try:
        if debug == False:
            arduino = usbcontroller.device()
        usbcontroller.sendtaxelcount(taxelarray, arduino, debug)
        usbcontroller.sendtaxeldata(taxelarray, arduino, debug)
        usbresult = True
    except:
        usbresult = False
    end = time.time()
    elapsed = end-start
    return usbresult