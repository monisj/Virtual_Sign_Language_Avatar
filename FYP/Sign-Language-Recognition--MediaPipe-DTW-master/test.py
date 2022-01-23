import os
import pathlib
path_video=pathlib.Path.cwd().joinpath('videos')
write=pathlib.Path.cwd().joinpath('utils\Base_G_Acc')
l=os.listdir(path_video)
li=[]
for i in l:
    if '.mp4' in i:
        li.append(i.split(".")[0])
for i in li:
    f=open(f'{write}\{i}.txt',"w")
    f.write("3000")
    f.close()

