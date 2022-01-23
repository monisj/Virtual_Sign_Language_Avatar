import pathlib
ref_sign_name="A"
path_video=data_path=pathlib.Path.cwd().joinpath('Base_G_Acc')
f=open(f'{path_video}\{ref_sign_name}.txt',"r")
print(f.read())
