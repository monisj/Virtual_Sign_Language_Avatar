import string,os,pathlib
root=pathlib.Path.cwd()
dataset=pathlib.Path.cwd().joinpath('data')
path_video=pathlib.Path.cwd().joinpath('videos')
d=''
list1=[]
b=os.listdir(path_video)
for videos_folder in b:
    c=os.listdir(str(path_video)+'\\'+videos_folder)
    try:
        d=os.listdir(str(dataset)+'\\'+videos_folder+'_dataset')
        for videos in c:
            vid=videos.replace('.mp4','')
            if vid in d:
                pass
            else:
                os.remove(str(path_video)+'\\'+videos_folder+'\\'+videos)
    except:
        pass
    
    # for videos in c:
    #     for vid in d:
    #         if vid==videos:
    #             pass
    #         else:
    #             list1.append(str(c)+'\\'+videos)
        
