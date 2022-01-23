import subprocess
import string,os,pathlib
from moviepy.editor import *
cur=pathlib.Path.cwd()
path_video=data_path=pathlib.Path.cwd().joinpath('videos')
write=pathlib.Path.cwd().joinpath('utils\Base_G_Acc')
videos="videos"
l=os.listdir(path_video)
li=[]
for i in l:
    if '.mp4' in i:
        li.append(i.split('.')[0])
s="A"
print(l)
for i in li:
    skip = False
    f=open(f'{write}\{i}.txt',"w")
    f.write("3000")
    f.close()
    try:
        os.makedirs(f'{cur}\data\{videos}\{i}')
    except FileExistsError:
        # directory already exists
        skip = True
    if skip is False:
        original_video = VideoFileClip(f"{path_video}\{i}.mp4")
        duration = original_video.duration
        print(duration)
        #clip1=original_video.subclip(0,(duration/2))
        #clip1.write_videofile(os.path.join(f'{cur}\data\{videos}\{i}',f'{i}-1.mp4'))
        clip2=original_video.subclip((duration/2),duration)
        clip2.write_videofile(os.path.join(f'{cur}\data\{videos}\{i}',f'{i}-2.mp4'))
    

