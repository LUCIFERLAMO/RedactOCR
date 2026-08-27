import pytesseract
import cv2
import regex as re 

# -------- this is for pytraceset to work
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# --------- loading the image AS black and white-----------
Raw_image = cv2.imread("blank.png",cv2.IMREAD_GRAYSCALE)
#print(Raw_image)


# ---------- Thresholding -------------------

# ---------- binary thresholding ----------------

_ , binary_thresholding = cv2.threshold(
    Raw_image,
    180,
    255,
    cv2.THRESH_BINARY
)

#cv2.imshow("demo",binary_thresholding)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

# ------------ Extract the text -----------------

text = pytesseract.image_to_string(binary_thresholding)

if not text:
    print("No text found in this image --  exiting the code")
    exit(0)


# -------------- getting the data and the coordinates of the image using data and saving it in the form of dictionary -------------------

Image_data = pytesseract.image_to_data(binary_thresholding,output_type=pytesseract.Output.DICT)

# pint the dict values 

#for data_point, value in Image_data.items():
#    print(data_point,value)


# taking the text inside the image so that we can pass it to the regex pattern 

data_and_its_coordinates =[]
text_from_image = ""


for i, current_text in enumerate(Image_data["text"]):
    if current_text.strip():
         text = current_text
         x = Image_data["left"][i]
         y = Image_data["top"][i]
         height = Image_data["height"][i]
         width = Image_data["width"][i]

         text_from_image += text + " "
         data_and_its_coordinates.append([text,x,y,height,width])




#print(data_and_its_coordinates)

# --------------- creating the regex pattern to identify addhar number and pan number -----------------


patterns = {
    "ADDHAR_NUMBER":r"\d{4} \d{4} \d{4}",
    "PAN_NUMBER":r"\w{5}\d{4}\w"
}

sensitive_data_found = []

for data_type, pattern in patterns.items():
     for matchh in re.finditer(pattern,text_from_image):
          sensitive_data = matchh.group() # gives the actual match 
          starting_index = matchh.start() # starting index of the match
          ending_index = matchh.end() # ending index of the match

          sensitive_data_found.append({
               "Data_type":data_type,
               "Sensitive_text": sensitive_data,
               "Starting_index":starting_index,
               "Ending_index":ending_index
          })

if not sensitive_data_found:
    print("No sensitive data found -- exiting program :)")
    exit(0)

# for better printing

#for item in sensitive_data_found:
#     print(item)


# ------------------- taking the sensitive data [sensitive text] and storing in the list----------------------- 

box_in_the_image_words = [item["Sensitive_text"].split() for item in sensitive_data_found]
#print(box_in_the_image_words)




# -------------------- making boxes in the image to point out where the sensitive data is -------------------

# first take the coordinates


matched_coordinates = []
for sensitive_word in box_in_the_image_words:
      for position,coordinate in enumerate(data_and_its_coordinates):
        if sensitive_word[0] == coordinate[0]:
            #print(position,coordinate)

            #matched_coordinates.append([coordinate[1],coordinate[2],coordinate[3],coordinate[4]]), removing this line as That means if "1234" appears somewhere else in the document with no "5678"/"9012" following it, you'd still get a box drawn around that lone "1234" — a false positive.

           

            # for addhar number search
            # adding a if condition to check the len of the sensitive work if its 3 then, we kn its a addhar card and then olnly we will execute the rest 

            if len(sensitive_word) == 3:
               if data_and_its_coordinates[position + 1][0] == sensitive_word[1] and data_and_its_coordinates[position + 2][0] == sensitive_word[2]:
                    matched_coordinates.append([data_and_its_coordinates[position][1],data_and_its_coordinates[position][2],data_and_its_coordinates[position][3],data_and_its_coordinates[position][4]])
                    matched_coordinates.append([data_and_its_coordinates[position + 1][1],data_and_its_coordinates[position + 1][2],data_and_its_coordinates[position + 1][3],data_and_its_coordinates[position + 1][4]])
                    matched_coordinates.append([data_and_its_coordinates[position + 2][1],data_and_its_coordinates[position + 2][2],data_and_its_coordinates[position + 2][3],data_and_its_coordinates[position + 2][4]])
            else:
                matched_coordinates.append([coordinate[1],coordinate[2],coordinate[3],coordinate[4]])
                    
               
               

#print(matched_coordinates)

for coordinate_position in matched_coordinates:
    x_axis = coordinate_position[0]
    y_axis = coordinate_position[1]
    hhight = coordinate_position[2]
    wweight = coordinate_position[3]

    rectange_image = cv2.rectangle(Raw_image,(x_axis,y_axis),(x_axis+wweight,y_axis+hhight),(0,0,255),3)

    # performing redaction (bluring the image)
    # we will use cv2.GaussianBlur() but this blurs the entire image by default so we have to take the positions of the area which we need to blur 
    # so here is the workflow

    # cut the postion that has to be blured 
    # blur it 
    # put the blur pice back

    # cutting the part of the image
    region = Raw_image[y_axis : y_axis + hhight, x_axis : x_axis + wweight] # give me rows from a-b and columns from c-d so its like list slicing but here we r taking only that part of the image 

    bluring = cv2.GaussianBlur(region,(51,51),0) # making the blur 
    # syntax is cv2.GaussianBlur(image, kernel_size, sigma) where
    # image is the pice that u want to cut
    # kernal sise: controls how strong the blur is — it must be a tuple of two odd numbers
    # sigma is 0

    # it works but averaging the pixels to the nearby pixels by smothening it

    Raw_image[y_axis : y_axis + hhight, x_axis : x_axis + wweight] = bluring # assinging the pice back to the positon 


    


# so moving the 4 lines outside the forloop will give the final output for us rather then us closing all the window one at a time
resized_image = cv2.resize(rectange_image, (800,600))
cv2.imshow("Rectange",resized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()


# creating a copy of the new blurred image

cv2.imwrite("redacted_image_output.png",Raw_image) # as the blurring was done in the raw image we have to use the raw_image itself 






