import cv2
import imutils


def threshold(img):
	# threshold checknum to improve ocr numbers detection
    # from the noisy backgroun 
    blurred = cv2.GaussianBlur(img,(11,11),0)
    _,thresh= cv2.threshold(blurred,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return thresh

def	segmentation_detection(image):
	# convert the image to grayscale, blur it, and apply edge detection
	# to reveal the outline of the check
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (5, 5), 0)
	edged = cv2.Canny(blurred, 30, 150)
	# detect contours in the edge map, sort them by size (in descending
	# order), and grab the largest contours
	cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
	# initialize a contour that corresponds to the business card outline
	cardCnt = None
 	# loop over the contours
	for c in cnts:
		# approximate the contour
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)
		# if this is the first contour we've encountered that has four
		# vertices, then we can assume we've found the segment
		if len(approx) == 4:
			cardCnt = approx
			break
	x,y,w,h= cv2.boundingRect(cardCnt)
	cropedCheckNum=gray[y:y+h, x:x+w]
    #convert checknum contour to white in the original image
	image[y:y+h, x:x+w]=255
	checkNum=threshold(cropedCheckNum)
	
	return image,checkNum