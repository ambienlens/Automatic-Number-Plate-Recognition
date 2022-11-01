# Debayan Majumder 2022
# Version 1.2

# Importing libraries
from source import *
from tkinter.filedialog import *
import tkinter as tk
import cv2

#hiding root window
root = tk.Tk()
root.withdraw()

#Extract Path
path = ""
while path=="":
    path = '{}'.format(askopenfilename(title='Choose an Image', filetypes=[('Image Files', '*.jpg *.png')]))

#sending image data to get numberplate data
imageData = getNumberPlateData(path)
processedImage = imageData[0]
data = removeCharacterNoise(imageData[1][0][1]);
confidenceLevel = round(round(imageData[1][0][2], 2)*100)
processedImage = resize_image(processedImage)

print("Detected Number Plate Data: %s"%(data))
print("The Image processed has an AI Confidence of: %s%%"%(confidenceLevel))
# print(path)

# Output of Image
cv2.imshow('Detected Number Plate Data', processedImage)

# Quiting/Closing all windows on pressing Q
# Quit: Q/q
while True:
    k = cv2.waitKey(0) & 0xFF
    if (k == ord('q')) or (k == ord('Q')):
        cv2.destroyAllWindows()
        break