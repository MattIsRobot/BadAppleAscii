from videoManager import *
from asciiTransformer import *
from os import listdir, rename, remove, system
from os.path import join, isfile
import argparse
from shutil import rmtree
from time import sleep, time
from playsound import playsound
import threading

parser = argparse.ArgumentParser()

parser.add_argument("yt_link")
parser.add_argument('-save_frames, --save_frames', '-sf', '--sf', action='store_true', help="Will save video frames if argument is passed")
parser.add_argument('-fps', '--fps', action='store', help="Fps to decode the video at, will default to native fps if invalid argument is passed")
parser.add_argument('-char_across', '--char_across', '-ca', '--ca', action='store', help="How many characters wide the ASCII art will appear Default is 75")
parser.add_argument('-braille', '--braille', '-b', '--b', action='store_true', help="Will render the video using braille ASCII characters (best for pure black and white / high contrast)")


args = parser.parse_args()

fps = int(args.fps) if args.fps != None else 144
charsAcross = int(args.char_across) if args.char_across != None else 75

videoName = downloadVideo(args.yt_link)
if isfile("source.mp4"): remove("source.mp4")
if isfile("source.mp4_audio.mp3"): remove("source.mp4_audio.mp3")
rename(videoName, "source.mp4")

videoName = "source.mp4"

videoToFrames(videoName, f'{videoName}_frames', fps)

frames = listdir(f'{videoName}_frames')
numFrames = len(frames)

displayFrames = []
# Load frames into memory
for i in range(numFrames):
	framePath = join(f'{videoName}_frames', f"{i}.jpg")
	display = imgToASCII(framePath, charsAcross, "\n") if not bool(args.braille) else imgToBraille(framePath, charsAcross, "\n", chr(10240))
	displayFrames.append(display)

#prepare audio
mp4ToMp3(videoName, f'{videoName}_audio.mp3')

def playAudioTask():
	playsound(f'{videoName}_audio.mp3')

# Display frames from memory and play audio
t = threading.Thread(target=playAudioTask)
t.daemon = True
t.start()
last = time()
for i in displayFrames:
	sleep((1/fps-0.00089)-(time()-last))
	last = time()
	system('cls')
	print(i)
		
if not bool(args.sf):
	rmtree(f'{videoName}_frames')
remove(videoName)
remove(f'{videoName}_audio.mp3')

