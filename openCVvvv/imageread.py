import cv2

# every image is broken down into millions of small box called as pixel
# pixel is the smallest individual unit of the image 
# if the image has only white or black it will have a value btw 0- 255 0 is complete dark and 255 is complete white
# if the image has colours then it will have 3 values BGR [RGB] thats [[246,0,123],[...],[...]]

image = cv2.imread("wallpaper.png") # reading the image with colours by default and the image variable has the 2D numpy array 

image2 = cv2.imread("wallpaper.png", cv2.IMREAD_GRAYSCALE) # reading the image without any colour just black and white and gray

#cv2.imshow("test",image2) # shows the image the first arg is the title for the image, 2nd arg is the variable that has the numpy array of the image 
#cv2.waitKey(0) # why 0 ? as we r mentioning how long we shd wait in terms of miliseconds. and we r saying we have to wait forever that y we have written as 0
#cv2.destroyAllWindows() # destries what windows it has created

#cv2.imwrite("image name") saves the changes what we did in the file. different name then different file else overrides the original file



# ---------------------------------------
#           module 2 
# ---------------------------------------


# 1. when we read a colourfull image and then we want to convert it back into grayscale image then we use cv2.cvtcolor(image that we read using imread, what colour u want to convert it to (color_bgr2gray))


gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#cv2.imshow("new image", gray_image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()


# thresholding:  lets say we have a grayscale image and the OCR SHD decide if a pixel is from the backhroug or is it a part of the text?
# so we use thresholding where lets say the threshhold is 123 and we go to each and evry pixel and ask .. are u darker then this threshold?
# if yes then it makes that pixel completly black 0
# else it makes that pixel xompletly white 255

# so now u will have a binary image where there exist only 2 values 0 and 255 and OCR loves it as there is no gray pixels to compare 
# the backgroung is white anf the text is dark and much easier to read





# workflow grayscaleimage -> threshold -> binary image

# syntax retval, binary = cv2.threshold( # Returns 2 thinsg the first one is the threshold value this fun has used and th actual image
 #   grayscale_image,
#  threshold_value,
 #   max_value, the max value for white, give it as 255
  #  threshold_type # we r using cv2.THRESH_BINARY that is if pixal value >= threshold: make it white else black
#)

# this is binary thresholding
retrive , binary_image = cv2.threshold(
    gray_image,
    150,
    255,
    cv2.THRESH_BINARY
)

#cv2.imshow("new image", binary_image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()


# Binary thresholding is good when you have stable lighting And clean documents. In all of the images But what You take photos from your phone. Then you will have uneven lighting
# For example, when you take a photo in your phone, the sunlight may be like half bright to the document in the right side, and more darker to the document in the left side. So the ocr will just make the entire pay right side of the paper black.
# To solve this issue, we have something called as adaptive thresholding.
# Adaptive thresholding is where instead of us giving a fixed threshold value the programme compares the neighbour. Thresholds like the pixels around it, asking, how bright are the pixels around it
# And then automatically assigns the threshold value. By breaking down the image into multiple blocks and then comparing the pixel brightness around the block, and then automatically deciding the threshold value for the particular block

#binary = cv2.adaptiveThreshold(
 #   grayscale_image,
 #   maxValue,
 #   adaptiveMethod, this calculates how the local threshold is calculated, cv2.ADAPTIVE_THRESH_MEAN_C(Imagine a small 11×11 window around a pixel.OpenCV computes:Average brightness of those neighbouring pixels.)
 #                      2, cv2.ADAPTIVE_THRESH_GAUSSIAN_C  Instead of treating every neighbouring pixel equally, pixels closer to the centre are given more importance.
 #   thresholdType,
 #   blockSize, It defines the size of the local neighbourhood. ex if 11 then it means 11 x 11 pixels. it shd always be ODD NUMBERS 
 #   C after getting the local threshold form adaptivemethod we subreact that with the c value for Because it often makes the text stand out better.
#)

adaptive_threshold= cv2.adaptiveThreshold(
    gray_image,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    11,
    2
)


#cv2.imshow("new image", adaptive_threshold)
#cv2.waitKey(0)
#cv2.destroyAllWindows()



# next is about resizing


#  Let's say you scanned a document, and within the document there is a letter A, and it is very small. And the OCR finds it very tough to recognise what character it is
# So we resize it by adding a bit more pixels to the letter A, so that the ocr can actually understand it even better
# The process of adding extra pixels. Is called as interpolation
# There are multiple interpolation methods Which can be used. For example, the first one is
# inter_linear =  fast, simple, default 
# inter_cubix =  looks at the neighbour pixels
# inter_area = best for shrinking/smaller images

# syntax for resize
#resized = cv2.resize(src, dsize, fx, fy, interpolation)

# src  = the image
# dsize is the width and the height (300,400) -> width and height of the image
# fx = wgen u dont know the width of the image, You just want to make the image twice as large. so we write fx 2 so make the width twice as large the the height
# fy = same but does for the height
#interpolation : which method to choose to add extra pixels 

re = cv2.resize(adaptive_threshold,None ,fy = 3, fx= 5) # if u give the dsize then the function ignores the fy and fx values
#cv2.imshow("resized image", re)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

#--------------------------------------
# how do u rotate an image?
#--------------------------------------

#et the heigh and width

height, width = image.shape[:2]

# find the center

center = (width // 2 , height // 2)

# create a roation matrix

rotation_matrix = cv2.getRotationMatrix2D(center,20,1.0) # 20 is the degree i want to tilt, 1.0 says no zoom

# now apply this tilt in the image

rotated_image = cv2.warpAffine(binary_image,rotation_matrix,(width,height))
cv2.imshow("Rotated image", rotated_image)
cv2.waitKey(0)
cv2.destroyAllWindows()