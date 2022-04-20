import pathlib,os
root=pathlib.Path.cwd()
dataset=pathlib.Path.cwd().joinpath('data')
b=os.listdir(dataset)
for i in b:
    c=os.listdir(str(dataset)+'\\'+i)
    for v in c:
        d=str(dataset)+'\\'+i+'\\'+v+'\\'+v+'_1'+'\\'+'angle_between_vectors_right.csv'
        e=str(dataset)+'\\'+i+'\\'+v+'\\'+v+'_2'+'\\'+'angle_between_vectors_right.csv'
        f=str(dataset)+'\\'+i+'\\'+v+'\\'+v+'_1'+'\\'+'angle_between_vectors_left.csv'
        g=str(dataset)+'\\'+i+'\\'+v+'\\'+v+'_2'+'\\'+'angle_between_vectors_left.csv'
        try:
            os.remove(d)
        except:
            pass
        try:
            os.remove(e)
        except:
            pass
        try:
            os.remove(f)
        except:
            pass
        try:
            os.remove(g)
        except:
            pass

