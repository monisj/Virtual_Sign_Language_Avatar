import pathlib,os
dataset=pathlib.Path.cwd().joinpath('data')
data_len=os.listdir(dataset)
a=0
for i in data_len:
    if a<1000:
        temp=[root for root,dirs,files in os.walk(f'data\\{i}') if not dirs]
        a+=len(temp)
        print(a)
        print(i)