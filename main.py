# Debayan Majumder 2022
# Version 4.1

# Importing libraries
from source import *
from tkinter.filedialog import *
import tkinter as tk
import cv2
import os
from datetime import date, datetime

#hiding root window
root = tk.Tk()
root.withdraw()

#Extract Path as tuple
multiplePaths = ""
while multiplePaths=="":
    multiplePaths = askopenfilenames(title='Choose an Image', filetypes=[('Image Files', '*.jpg *.png')])

#Creating Export directory
rootDir = "Exported Keys"
os.makedirs(rootDir, exist_ok=True)

# Exporting Current Date
tD = str(date.today())
tT = str(datetime.now().time())
currentDate = "".join([i for i in tD if i != "-"])
currentTime = "".join([i for i in tT if i != ":"])[:6]

#Initialising Text File Heading and variable
exportContent = "!!Exported Keys!! \n"
exportContent =  exportContent + "Exported Number Plate Data from Selected Images. \n"
exportContent =  exportContent + "\n"
exportContent =  exportContent + "\n"

# Running for loop for number of Paths
for i in range(0, len(multiplePaths)):
    #sending image data to get numberplate data
    path = multiplePaths[i]             #Extracting paths from tuple
    imageData = getNumberPlateData(path)
    processedImage = imageData[0]
    data = removeCharacterNoise(imageData[1][0][1]);
    confidenceLevel = round(round(imageData[1][0][2], 2)*100)
    processedImage = resize_image(processedImage)

    # Creating File name and appenting text to it
    fileName = "Session%s_%s_BatchOf%s.txt"%(currentDate, currentTime, len(multiplePaths))
    exportContent = exportContent + "----" + "\n"
    exportContent = exportContent + "File: %s"%(os.path.basename(path)) + "\n"
    exportContent = exportContent + "Detected Number Plate: %s"%(data) + "\n"
    exportContent = exportContent + "AI Confidence level: %s%%"%(confidenceLevel) + "\n"
    exportContent = exportContent + "----" + "\n"
    exportContent = exportContent + " " + "\n"
    
    # print("Detected Number Plate Data: %s"%(data))
    # print("The Image processed has an AI Confidence of: %s%%"%(confidenceLevel))

    # Output of Image
    cv2.imshow('Processed Image Data', processedImage)
    cv2.imshow('Number Plate Data', display_text(disText1=data, disText2=confidenceLevel, value=12, width=400, height=150))

    # Window closes after 2 sec or force quit by Q
    # Quiting/Closing all windows on pressing Q
    # Quit: Q/q
    while True:
        k = cv2.waitKey(2000) & 0xFF
        if (k == ord('q')) or (k == ord('Q') or (k == 255)):
            cv2.destroyAllWindows()
            break

#Creating file and writing to it
    with open("%s/%s"%(rootDir, fileName), "w") as export:
        export.write(exportContent)
    
print("Keys Exported.")
print("Program Executed & Terminated with no visible errors.")
