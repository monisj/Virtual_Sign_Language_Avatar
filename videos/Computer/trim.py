import subprocess
import string,os,pathlib
from moviepy.editor import *
path_video=data_path=pathlib.Path.cwd()
l=os.listdir(path_video)
li=[]
for i in l:
    if '.mp4' in i:
        li.append(i.split('.')[0])
s="A"
for i in li:
    skip = False
    try:
        os.makedirs(i)
    except FileExistsError:
        # directory already exists
        skip = True
    if skip is False:
        original_video = VideoFileClip(f"{i}.mp4")
        duration = original_video.duration
        print(duration)
        clip1=original_video.subclip(0,(duration/2))
        clip1.write_videofile(os.path.join(f'{i}',f'{i}_1.mp4'))
        clip2=original_video.subclip((duration/2),duration)
        clip2.write_videofile(os.path.join(f'{i}',f'{i}_2.mp4'))
    

