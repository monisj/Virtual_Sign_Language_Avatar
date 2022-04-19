from asyncore import write
from pathlib import Path
import pickle
from queue import Queue
import os
import re
from tkinter import Frame
import mediapipe as mp
import csv
from progress.bar import ChargingBar


def analyze(path):
    connections = mp.solutions.holistic.HAND_CONNECTIONS
    path1=path.replace(re.search('embeddings.*pickle',path)[0],'')
        
    infile=open(path,'rb')
    dic1=pickle.load(infile)
    points_name= ["Wrist","Thumb_CMC","Thumb_MCP","Thumb_IP","Thumb_Tip",
        "Index_Finger_MPC","Index_Finger_PIP","Index_Finger_DIP","Index_Finger_TIP",
        "Middle_Finger_MCP","Middle_Finger_PIP","Middle_Finger_DIP","Middle_Finger_TIP",
        "Ring_Finger_MCP","Ring_Finger_PIP","Ring_Finger_DIP","Ring_Finger_TIP","Pinky_MCP",
        "Pinky_PIP","Pinky_DIP","Pinky_TIP"]

    if len(dic1.lh_embedding) !=0:
        print(f'********** Data of Left Hand in {path} **********')
        csv_file=open(f"{path1}/angle_between_vectors_left.csv","w").close()
        csv_file=open(f"{path1}/angle_between_vectors_left.csv","a")
        writer=csv.writer(csv_file)
        writer.writerow(["Frame","Vector1","Vector2","Angle between Vector1 and Vector2"])
        frame=len(dic1.lh_embedding)
        count1=0
        with ChargingBar(f'Loading data in CSV File',max=frame) as b:
            for k in range(frame):
                for connection_to in connections:
                    for connection_from in connections:
                        writer.writerow([k,(points_name[connection_to[0]],points_name[connection_to[1]]),(points_name[connection_from[0]],points_name[connection_from[1]]),dic1.lh_embedding[k][count1]])
                        count1+=1
                count1=0
                b.next()
            print('\n')

    if len(dic1.rh_embedding) !=0:
        print(f'********** Data of Right Hand in {path} **********')
        csv_file=open(f"{path1}/angle_between_vectors_right.csv","w").close()
        csv_file=open(f"{path1}/angle_between_vectors_right.csv","a")
        writer=csv.writer(csv_file)
        writer.writerow(["Frame","Vector1","Vector2","Angle between Vector1 and Vector2"])
        frame=len(dic1.rh_embedding)
        count1=0
        with ChargingBar(f'Loading data in CSV File',max=frame) as b:
            for k in range(frame):
                for connection_to in connections:
                    for connection_from in connections:
                        writer.writerow([k,(points_name[connection_to[0]],points_name[connection_to[1]]),(points_name[connection_from[0]],points_name[connection_from[1]]),dic1.rh_embedding[k][count1]])
                        count1+=1
                count1=0
                b.next()
            print('\n')
            


    



q=Queue()
q.put(str(f'{Path.cwd()}\data'))
while(q.empty()!=True):
    p=q.get()
    if re.search('.*embeddings.*pickle',p):
        analyze(p)
        continue
    elif os.path.isfile(p):
        continue
    for i in os.listdir(p):
        if re.search('.*embeddings.*pickle',str(os.path.join(p,i))):
            q.put(str(f'{os.path.join(p,i)}'))

        elif os.path.isfile(str(f'{os.path.join(p,i)}')):
            continue

        else:
            q.put(str(f'{os.path.join(p,i)}'))

