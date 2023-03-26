from cv2 import VideoCapture, CAP_PROP_FRAME_COUNT, CAP_PROP_FPS, imwrite
from os import mkdir
from os.path import isdir, join, basename
from pytube import YouTube
from numpy import arange
from shutil import rmtree
from moviepy.editor import VideoFileClip, AudioFileClip


def downloadVideo(link:str) -> str:
	try:
		yt_object = YouTube(link)
		yt_object = yt_object.streams.get_highest_resolution()

		try:
			yt_object.download()
			return(basename(yt_object.get_file_path()))
		except:
			print("error with download :(")
		
		print("download complete :)")
		
	except:
		print("please enter a valid URL")


def videoToFrames(videoPath:str, outputDir:str, fps:int) -> bool:
	if not isdir(outputDir):
		mkdir(outputDir)
	else: 
		rmtree(outputDir)
		mkdir(outputDir)

	video = VideoCapture(videoPath)
	normalFps = video.get(CAP_PROP_FPS)
	fps = min(fps, normalFps)

	# list of timestamps to save
	timestampsToSave = getFrameSaveTS(video, fps)

	count = 0
	fCount = 0
	while True:
		is_read, frame = video.read()
		if not is_read:
			# break out of the loop if there are no frames to read
			break
		# get the duration by dividing the frame count by the FPS
		frame_duration = count / normalFps
		try:
			# get the earliest duration to save
			closest_duration = timestampsToSave[0]
		except IndexError:
			# the list is empty, all duration frames were saved
			break
		if frame_duration >= closest_duration:
			# if closest duration is less than or equals the frame duration, 
			# then save the frame
			imwrite(join(outputDir, f"{fCount}.jpg"), frame)
			fCount += 1
			# drop the duration spot from the list, since this duration spot is already saved
			try:
				timestampsToSave.pop(0)
			except IndexError:
				pass
		# increment the frame count
		count += 1
	
	return True


def getFrameSaveTS(cap:VideoCapture, fps:int) -> list[int]:
	timestamps = []

	videoLength = int(cap.get(CAP_PROP_FRAME_COUNT))/cap.get(CAP_PROP_FPS)

	for i in arange(0, videoLength, 1/fps):
		timestamps.append(i)
	return timestamps

def mp4ToMp3(mp4filepath:str, mp3filepath:str) -> None:
	videoclip=VideoFileClip(mp4filepath)
	audioclip=videoclip.audio
	audioclip.write_audiofile(mp3filepath)
	audioclip.close()
	videoclip.close()
