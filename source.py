# Debayan Majumder 2022
# Version 4.3

# Importing Libraries
import cv2
import numpy as np
import imutils
import easyocr

# Function to get the path as input and return the number plate as output
def getNumberPlateData(path):
    # Read in Image, Grayscale and Blur
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Converting image to grayscale

    # Apply filter and Find edges for localisation
    bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
    edged = cv2.Canny(bfilter, 30, 200) #Edge detection

    # Find contours and Mask
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    #Searching for rectangle
    location = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10, True)
        if len(approx) == 4:
            location = approx
            break

    # Finding the bottom left coordinate
    coorX = approx[0][0][0] #Coordinate X
    coorY = approx[0][0][1] #Coordinate Y

    # For getting the bottom left coordinate, we are finding
    # the lowest coor of X and highest of Y
    for i in approx:
        if(i[0][0] < coorX):
            coorX = i[0][0]
        if(i[0][1] > coorY):
            coorY = i[0][1]

    #masking of image
    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [location], 0,255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)

    # Cropping image to number plate
    (x,y) = np.where(mask==255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = gray[x1:x2+1, y1:y2+1]

    # Using EasyOCR to read text from Image
    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(cropped_image)

    # If reader detects text
    if len(result) != 0:
        #Rendering Image
        color = (255,255,255) #Colour of the Text and rectangle
        text = removeCharacterNoise(result[0][-2])
        font = cv2.FONT_HERSHEY_SIMPLEX
        gammaAdjImg = adjust_gamma(brighten_image(img))

        fontscale = 1 if img.shape[0] < 500 else int(img.shape[0]/500)

        res = cv2.putText(gammaAdjImg, text=text, org=(coorX, coorY + 30), fontFace=font,
        fontScale=fontscale, color=color, thickness=int(fontscale)+1, lineType=cv2.LINE_AA) #Adding Text

        res = cv2.rectangle(gammaAdjImg, tuple(approx[0][0]), tuple(approx[2][0]), color, 3, lineType=cv2.LINE_AA) #Drawing Rectangle

    else:
        # Making Copies
        overlay = img.copy()
        output = img.copy()
        alpha = 0.45

        # Text Initialisation
        font = cv2.FONT_HERSHEY_SIMPLEX
        text = "NO NUMBER PLATE FOUND"
        fontScale = 1
        thickness = 2

        # Getting the Text Size
        textsize = cv2.getTextSize(text, font, fontScale=fontScale, thickness=thickness)[0]

        # Getting Text Coordinates
        textX = int((img.shape[1] - textsize[0]) / 2)
        textY = int((img.shape[0] + textsize[1]) / 2)

        # Rendering the image
        newImg = cv2.rectangle(overlay, (0, 0), (img.shape[1], img.shape[0]) ,(0,0,255), -1)
        newImg = cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)
        res = cv2.putText(newImg, text=text, org=(textX, textY), fontFace=font, 
        fontScale=fontScale, color=(255,255,255), thickness=thickness, lineType=cv2.LINE_AA)

        result = [([[0, 0], [0, 0], [0, 0], [0, 0]], 'DATA NOT FOUND', 0)]

    #return value
    return [res, result]

# Removing characters other than A-Z, a-z and 0-9 and Uppercasing any lowercase alphabets
def removeCharacterNoise(data):
    newData=""
    for i in data:
        char = ord(i)
        if((char>=65 and char<=90) or (char>=97 and char<=122) or (char>=48 and char<=57) or (char==32)):
            if((char>=97 and char<=122)):
                newData += i.upper()
            else:
                newData += i
    return newData

# Adjusting gamma to the desired choice
def adjust_gamma(image, gamma=0.5):
   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)]).astype("uint8")

   return cv2.LUT(image, table)

# Brightening the Image
def brighten_image(image, brightness=20, gamma=0.5):
    # Creating a gray image with Brightness value defaulted at 60
    value = int(brightness/100*255)
    overlay = np.ones(image.shape, dtype="uint8")*value
    blend = cv2.addWeighted(image, 1, overlay, gamma, 0.0)
    return blend

# Resizing image to 720p
def resize_image(image, size=720):
    scale = image.shape[0]/size;
    height = int(image.shape[0] / scale)
    width = int(image.shape[1] / scale)
    dimensions = (width, height)

    return cv2.resize(image, dimensions, interpolation=cv2.INTER_AREA)

# Displaying Number plate data with AI Confidence level
def display_text(width=512, height=256, value=15, disText1="Hello World!",
    disText2="50", txtColor=(255,255,255), txtColor2=(100,100,100),
    fontScale=1, thickness=2, newFontScale=0.5, newThickness=1):

    #Creating a blank canvas with value being the Brightness.
    grayImg = np.ones((height, width), dtype="uint8")*int(value/100*255)

    # Font & Text Initialisation
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = disText1
    confidence = "AI Confidence level: %s%%"%(disText2)

    #Extracting Textbox sizes
    textsize = cv2.getTextSize(text, font, fontScale=fontScale, thickness=thickness)[0]
    textsize2 = cv2.getTextSize(confidence, font, fontScale=newFontScale, thickness=newThickness)[0]

    #Calculation Coordinates for textsize 1
    textX = int((grayImg.shape[1] - textsize[0]) / 2)
    textY = int((grayImg.shape[0] + textsize[1]) / 2)

    #Rendering Results
    finalImg = cv2.putText(grayImg, text=text, org=(textX, textY), fontFace=font, 
        fontScale=fontScale, color=txtColor, thickness=thickness, lineType=cv2.LINE_AA)

    # Final Cooridinates
    textX = textX - int((textsize2[0] - textsize[0]) / 2)
    textY = textY + textsize2[1] + 12
    
    finalImg = cv2.putText(grayImg, text=confidence, org=(textX, textY), fontFace=font, 
        fontScale=newFontScale, color=txtColor2, thickness=newThickness, lineType=cv2.LINE_AA)

    return finalImg