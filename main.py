# Debayan Majumder 2022
# Version 3.3

# Importing libraries
from source import *
from tkinter.filedialog import *
import tkinter as tk
import cv2

#hiding root window
root = tk.Tk()
root.withdraw()

#Extract Path as tuple
multiplePaths = ""
while multiplePaths=="":
    multiplePaths = askopenfilenames(title='Choose an Image', filetypes=[('Image Files', '*.jpg *.png')])

# Running for loop for number of Paths
for i in range(0, len(multiplePaths)):
    #sending image data to get numberplate data
    path = multiplePaths[i]             #Extracting paths from tuple
    imageData = getNumberPlateData(path)
    processedImage = imageData[0]
    data = removeCharacterNoise(imageData[1][0][1]);
    confidenceLevel = round(round(imageData[1][0][2], 2)*100)
    processedImage = resize_image(processedImage)

    print("Detected Number Plate Data: %s"%(data))
    print("The Image processed has an AI Confidence of: %s%%"%(confidenceLevel))

    # Output of Image
    cv2.imshow('Processed Image Data', processedImage)
    cv2.imshow('Number Plate Data', display_text(disText1=data, disText2=confidenceLevel, value=12, width=400, height=150))

    # Quiting/Closing all windows on pressing Q
    # Quit: Q/q
    while True:
        k = cv2.waitKey(0) & 0xFF
        if (k == ord('q')) or (k == ord('Q')):
            print("Program Executed & Terminated with no visible errors.")
            cv2.destroyAllWindows()
            break