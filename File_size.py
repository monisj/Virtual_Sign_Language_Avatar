import os
import subprocess
import string,os,pathlib
from moviepy.editor import *
import shutil
from utils.landmark_utils import save_landmarks_from_new_video
from utils.dataset_utils import new_load_reference_signs
import os.path


root=pathlib.Path.cwd()
dataset=pathlib.Path.cwd().joinpath('data')
#path_video=pathlib.Path.cwd().joinpath('PSL Videos')
#print(path_video)
b=os.listdir(dataset)
count=0
#f=open("File_size.txt","a")
#f=open("size.txt","w+")
for i in b:
    c=os.listdir(str(dataset)+'\\'+i)
    for j in c:
        size=os.stat(str(dataset)+'\\'+i+'\\'+j+'\\'+f'{j}_1'+'\\'+f'embeddings_{j}_1.pickle')

        if size.st_size//1024<2:
            count+=1
            print("File Names = {}".format(str(dataset)+'\\'+i+'\\'+j+'\\'+f'{j}_1'+'\\'+f'embeddings_{j}_1.pickle'))
            #f.write("\nFile Names = {}".format(str(dataset)+'\\'+i+'\\'+j+'\\'+f'{j}_1'+'\\'+f'embeddings_{j}_1.pickle'))

for i in b:
    c=os.listdir(str(dataset)+'\\'+i)
    for j in c:
        size=os.stat(str(dataset)+'\\'+i+'\\'+j+'\\'+f'{j}_2'+'\\'+f'embeddings_{j}_2.pickle')

        if size.st_size//1024<2:
            count+=1
            print("File Names = {}".format(str(dataset)+'\\'+i+'\\'+j+'\\'+f'{j}_2'+'\\'+f'embeddings_{j}_2.pickle'))
            #f.write("\nFile Names = {}".format(str(dataset)+'\\'+i+'\\'+j+'\\'+f'{j}_2'+'\\'+f'embeddings_{j}_2.pickle'))
#f.close()
print(count)

# get file stats
#stats = os.stat('main.py')
#print('Size of file is', stats.st_size/1024, 'kilobytes')
