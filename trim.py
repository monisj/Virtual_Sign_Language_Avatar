import subprocess
import string,os,pathlib
from moviepy.editor import *
def trim(vid,path,outpath):
    skip=False
    try:
        os.makedirs(outpath)
    except FileExistsError:
        # directory already exists
        pass
    original_video = VideoFileClip(path)
    duration = original_video.duration
    print(duration)
    clip1=original_video.subclip(0,(duration/2))
    try:
        os.remove(pathlib.Path(__file__).parent.absolute().joinpath(outpath,f'{vid}_1.mp4'))
        os.remove(pathlib.Path(__file__).parent.absolute().joinpath(outpath,f'{vid}_2.mp4'))
    except:
        pass
    clip1.write_videofile(str(pathlib.Path(__file__).parent.absolute().joinpath(outpath,f'{vid}_1.mp4')))
    clip2=original_video.subclip((duration/2),duration)
    clip2.write_videofile(str(pathlib.Path(__file__).parent.absolute().joinpath(outpath,f'{vid}_2.mp4')))
    return
#trim('B',r'D:/FYP/Sign-Language-Recognition--MediaPipe-DTW/videos/Alphabets/B.mp4',r'D:\FYP\Sign-Language-Recognition--MediaPipe-DTW\temp_videos\B')

