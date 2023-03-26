from cv2 import imread, resize
import cv2
from numpy import ndarray
from math import floor, ceil
from unicodedata import bidirectional

def imgToBraille(path:str, charAcross:int, newline:str="\n", blank:str=f" {chr(6069)}{chr(6069)} {chr(6069)}{chr(6069)}") -> str:
	img = imread(path)
	dims = img.shape
	#print(f"Width: {dims[1]} Height: {dims[0]}")
	
	dotsAcross = charAcross*2 + charAcross-1

	width = dotsAcross
	height = ceil(dims[0]/dims[1] * width)

	scaledImg = resize(img, (width, height))

	#print(f"Transforming to Width: {width} Height: {height}")
	
	brailleImg = ""
	brailleCharCount = 0
	# chunk into braille characters
	for y_count in range(floor(height/5)+1):
		y = 5*y_count
		for x_count in range(floor(width/3)+1):
			x = 3*x_count


			# add a new line if needed
			if brailleCharCount % charAcross == 0 and brailleCharCount != 0:
				brailleImg+=f"{newline}"

			# get braille character at coordinates (direct from binary value to base 10)
			brailleChar = 0

			mapX = [0,0,0,0,1,1,1,1]
			mapY = [0,1,2,3,0,1,2,3]

			for i in range(8):
				power = 2**i
				if (subX:=x+mapX[i]) < width and (subY:=y+mapY[i]) < height:
					brailleChar += getDotValue(scaledImg[subY, subX])*power

			emptyBraille = 10240 # Unicode value of empty braille character in base 10
			if brailleChar > 0:
				brailleImg += chr(emptyBraille + brailleChar)
			else:
				brailleImg += blank
			brailleCharCount += 1

	return brailleImg
	

def getDotValue(pixel:tuple[int]) -> int:
	bwVal = (int(pixel[0])+int(pixel[1])+int(pixel[2]))/(255*3)
	bwVal = round(bwVal)
	return bwVal

def imgToASCII(path:str, charAcross:int, newline:str="\n") -> str:
	img = imread(path)
	dims = img.shape
	#print(f"Width: {dims[1]} Height: {dims[0]}")
	
	width = charAcross
	height = ceil(dims[0]/dims[1] * width)

	scaledImg = resize(img, (width, height))
	
	asciiImg = ""
	asciiCharCount = 0
	# chunk into braille characters
	for y_count in range(height//2-1):
		y = y_count*2
		for x in range(width):
			# add a new line if needed
			if asciiCharCount % charAcross == 0 and asciiCharCount != 0:
				asciiImg+=f"{newline}"

			asciiImg += getPixelASCIIChar(scaledImg[y, x])
			asciiCharCount += 1

	return asciiImg

def getPixelASCIIChar(pixel:tuple[int]) -> str:
	luminanceScale = " .,-~:;=!*#$@"
	luminanceScaleSteps = len(luminanceScale)

	bwVal = (int(pixel[0])+int(pixel[1])+int(pixel[2]))/(255*3)
	bwVal = round(bwVal*12.4)
	return luminanceScale[bwVal]