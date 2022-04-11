import pathlib,os
dataset=pathlib.Path.cwd().joinpath('videos')
data_len=os.listdir(dataset)
print(data_len)
