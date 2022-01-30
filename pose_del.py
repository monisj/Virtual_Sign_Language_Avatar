import os
import pathlib

data_path=pathlib.Path.cwd().joinpath('data\dataset')
l=os.listdir(data_path)
li=[]
li=[x.split('.')[0] for x in l]
print(li)
a=1
for pose_d in li:
    for i in range(1,3):
        if os.path.exists(f'{data_path}\{pose_d}\{pose_d}-{i}\pose_{pose_d}-{i}.pickle'):
            os.remove(f'{data_path}\{pose_d}\{pose_d}-{i}\pose_{pose_d}-{i}.pickle')
        else:
            print("File {} Does not exists".format("pose_"+pose_d+"-"+str(i)+".pickle"))
            
 
