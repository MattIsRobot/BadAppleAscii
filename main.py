from videoManager import *
from asciiTransformer import *
from os import listdir, rename, remove
from os.path import join, isfile

fps = 30
#outputFile = 'asciiframes.txt'
#if isfile(outputFile): remove(outputFile)


videoName = downloadVideo('https://www.youtube.com/watch?v=FtutLA63Cp8')
if isfile("source.mp4"): remove("source.mp4")
rename(videoName, "source.mp4")

videoName = "source.mp4"

videoToFrames(videoName, f'{videoName}frames', fps)

frames = listdir(f'{videoName}frames')
numFrames = len(frames)

for i in range(numFrames):
	framePath = join(f'{videoName}frames', f"{i}.jpg")
	#with open(outputFile, 'a', encoding="utf-8") as file:
		#file.write('```')
		#file.write(frame:=imgToASCII(framePath, 70, "newline"))
		#file.write('```\n')
	print(imgToASCII(framePath, 70, "\n"))
	print('\n\n')
		

