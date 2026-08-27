# Tesseract OCR = converts an image → into text
# pipline: Preprocessed Image (convert an image into binary image)
        #  Segmentation (breaking down the image into smaller parts (pages -> lines -> words -> characters))
        #  Extraction (seeing each character and identifying what shape it is)
        #  Recognition (identifying what character it is by seeing the shapes)
        #  Post-processing (fix spelling errors)


# difference btw Tesseract and pytesseract OCR

# when u send an image the Tesseract recives it and then sends the images to the pytesseract OCR and then the pytesseract OCR 
# processes the images and its responsibility is to recognise the text from the image and send the result back to the Tesseract
# and then the Tesseract returns the result back to the user

# simple

# user gives image -> Tesseract -> pytesseract OCR -> Tesseract -> user

import pytesseract
import cv2

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# step one is pre processing

# step 1: reading the image 

image =  cv2.imread("text.jpg", cv2.IMREAD_GRAYSCALE)
#cv2.imshow("imageeee",image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

# step 2: using adapting thresholding

adaptive_thresholding = cv2.adaptiveThreshold(
    image,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    11,
    2
)

#cv2.imshow("better image", adaptive_thresholding)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

# lets try using noraml threshold as asdaptive did bad cox its good only for images with uneven lighting

_ , normal = cv2.threshold(
   image,
   180, # did try btw 150,170 and finally 180 and this is the benst for this umage as we got every text fo the image correctly
   255,
   cv2.THRESH_BINARY
)

#cv2.imshow("better image", normal)
#cv2.waitKey(0)
#cv2.destroyAllWindows()



# step 3: resizing
# we dont need it for now 

# step 4: pass the obj to the Tesseract 

text = pytesseract.image_to_string(normal)

print(text)

# if u want to know how sure is pytesseract OCR when its returing each work u can use this ucntion and chekc how confident it is 
# in each word for example it migh be like 94% sure that the word is happy like that
data = pytesseract.image_to_data(normal,output_type=pytesseract.Output.DICT) # it gives the data in the form of dictionary

#for item,value in data.items():
#    print(item, value)

coordinates = []

for i , value in enumerate(data["text"]):
    if value.strip(): # if there is the word after stripping and no empty string only then we will continue 
        x = data["left"][i]
        y = data["top"][i]
        width = data["width"][i]
        height = data["height"][i]
        coordinates.append([value,x,y,width,height])


search = [item[0] for item in coordinates]

for item in coordinates:
    if item[0] in   search:
        Word = item[0]
        x_axis = item[1]
        y_axis = item[2]
        width_h = item[3]
        height = item[4]

        draw_lines = cv2.rectangle(image,(x_axis,y_axis),(x_axis+width_h,y_axis+height),(0,0,255),2)

 # here we can draw a box using cv2.draw lines and the syntax is 
#(image,(x,y),(x+width,x+height),(brg color),(thickness))
        cv2.imshow("Draw_lines",draw_lines)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

#and y OCR MIGHT FAIL 

# 1. blury image
# 2. tilted image, even a 5-10 degree tilt will reduce accuracy so resizing is actually important
# 3. low constrast, isnted of black and white we have light gray and dark gray again reduces accuracy
# 4. noice,  unwanted things in the image 
# 5. weird fonts
# 6. handwritting

