
import cv2
import imutils
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# read the img file
image = cv2.imread("C:/Users/Lenovo/Desktop/img4.jpeg")

# resize the img-change width to 500
image = imutils.resize(image, width=500)

# display the original image
cv2.imshow("original image", image)
cv2.waitKey(0)

# rgb to gray scale conversion
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("-Gray scale Conversion", gray)
cv2.waitKey(0)

# noise removal
gray = cv2.bilateralFilter(gray, 11, 17, 17)  
cv2.waitKey(0)


# find edges of the gray scale img
edged = cv2.Canny(gray, 170, 200)
cv2.imshow("3-Canny edges", edged)
cv2.waitKey(0)

# find contours based on edges
cnts, new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# Create copy of original img to draw all contours
img1 = image.copy()
cv2.drawContours(img1, cnts, -1, (0, 255, 0, 3))
cv2.imshow("4-All Contours", img1)
cv2.waitKey(0)

# sort contours based on their aera keeping minimum area as '30'
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
NumberPlateCnt = None  # we currently have no Number plate content

# top 30 contours
img2 = image.copy()
cv2.drawContours(img2, cnts, -1, (0, 255, 0), 3)
cv2.imshow("S -top 30 Contours", img2)
cv2.waitKey(0)

# loop over our contour to find
idx = 7
for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    # print("approx=",approx)
    if len(approx) == 4:  # select the contour with 4 contents
        NumberPlateCnt = approx

        # crop those contours and store it in cropped img folder
        x, y, w, h = cv2.boundingRect(c)
        new_img = image[y:y+h, x:x+w]
        cv2.imwrite('C:/Users/Lenovo/Desktop/nn/'+str(idx)+'.png', new_img)
        idx += 1

        break
# drawing the selected contour on the original img
# print(NumberPlateCnt)
cv2.drawContours(image, NumberPlateCnt, -1, (0, 255, 0), 3)
cv2.imshow("Final image with number plate detected", image)
cv2.waitKey(0)

Cropped_img_loc = 'C:/Users/Lenovo/Desktop/nn/7.png'
cv2.imshow("Cropped Image", cv2.imread(Cropped_img_loc))

# use tesseract to convert img into string
text = pytesseract.image_to_string(Cropped_img_loc, lang='eng')
print("Number is :", text)
cv2.waitKey(0)
