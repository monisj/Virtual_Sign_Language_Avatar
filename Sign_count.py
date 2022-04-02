import subprocess
import string,os,pathlib
import shutil
import os.path
from fuzzywuzzy import fuzz

##pip install fuzzywuzzy, python-Levenshtein

root=pathlib.Path.cwd()
path_video=pathlib.Path.cwd().joinpath('data')
b=os.listdir(path_video)

f=open('1000_signs.txt',"r+")
f=f.read().splitlines()
vid_found=0

vid_present=open("Videos_Present_After_Updation.txt","a")
vid_absent=open("Videos_Absent_After_Updation.txt","a")
#vid_absent=0
found=[]
#absent=[]
for i in b:
    video_path=pathlib.Path.cwd().joinpath(f'data\\{i}')
    vid=os.listdir(video_path)
    for v in vid:
        for im in f:
            vid1=im.lower()
            vid2=v.lower()
            if vid1==vid2:
                vid_found+=1
                found.append(v)
                vid_present.write(str(i)+'/'+str(v) + "\n")
                break
            else:
                im,v=str(im),str(v)
                ratio=fuzz.ratio(im,v)
                if ratio>75:
                    vid_found+=1
                    found.append(im)
                    vid_present.write(str(i)+'/'+str(v) + "\n")
                    break
        if v in found:
            pass
        else:
            b=str(video_path)+'\\'+v
            if os.path.isdir(str(video_path)+'\\'+v):
                print(f'Remove = {b}')
                shutil.rmtree(str(video_path)+'\\'+v)
                vid_absent.write(str(i)+'/'+str(v) + "\n")
for j in b:
    video_path=os.listdir(f'data\\{j}')
    if len(video_path)==0:
        shutil.rmtree(str(video_path)+'\\'+j)
    
            
print(f'Videos Found = {found}')
print(len(found))

vid_present.close()
vid_absent.close()
#print(f'Videos Absent = {absent}')
