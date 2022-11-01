# **Automatic Number Plate Recognition**
This is an AI, which will detect the number plate of a car from a given image and extract the Number Plate data from that Image.

### Libraries Used :-
- OpenCV
- Tkinter
- Numpy
- EasyOCR
- iMultils

## **The Basics**
The *Automatic Number Plate Detection* or ANPR works by taking input of an Image (jpeg or png) and searches for a rectangular shaped number plate and finally Extracting the number from it.
An exponential increase in the number of vehicles necessitates the use of automated systems to maintain vehicle information for various purposes. But for now this Program takes images as input ie, live video input not supported.

<!-- ![Demonstration](Demo Images/image1.jpg) -->

## **Implementation**
There are five steps to the detection.
- Read Image and Convert to Grayscale using OpenCV
- Apply Filters and Find edges for Localization
- Find contours and Mask it
- Using EasyOCR and convert ImageToText
- Render Result using OpenCV and Tkinter



