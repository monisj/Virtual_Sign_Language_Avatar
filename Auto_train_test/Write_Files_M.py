import os
import pathlib
path_video=data_path=pathlib.Path.cwd().joinpath('alpha')
DATA_PATH = data_path=pathlib.Path.cwd().joinpath('Model_Count_Files')
os.chdir(DATA_PATH)

l=os.listdir(path_video)
li=[x.split('.')[0] for x in l]
print(li)

for items in li:
    numb=os.listdir(str(path_video)+'\\'+items+'\\')
    numb=len(numb)
    print("items of {} are ={}".format(items,numb))
    f = open(items+".txt", "w")
    f.write(str(numb))
    f.close()


f = open(str(DATA_PATH)+'\\'+str('A')+".txt", "r")
print(f.read())
#open and read the file after the appending:
#f = open("demofile3.txt", "r")
#print(f.read()) 
