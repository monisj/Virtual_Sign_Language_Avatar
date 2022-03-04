import subprocess
import string,os,pathlib
from moviepy.editor import *
import shutil
from utils.landmark_utils import save_landmarks_from_new_video
from utils.dataset_utils import new_load_reference_signs
import os.path




root=pathlib.Path.cwd()
dataset=pathlib.Path.cwd().joinpath('data')
path_video=pathlib.Path.cwd().joinpath('PSL Videos')
print(path_video)
b=os.listdir(path_video)
for i in b:
    print(i)
    try:
        os.mkdir('temp_'+i)
    except:
        pass
    try:
        os.mkdir(str(dataset)+'\\'+i+'_dataset')
    except:
        pass
    video_path=pathlib.Path.cwd().joinpath(f'PSL Videos\\{i}')
    vid=os.listdir(video_path)
    for v in vid:
        v=v.replace('.mp4','')
        if os.path.isdir(str(dataset)+'\\'+i+'_dataset'+'\\'+v+'\\'+f'{v}_1') and os.path.isdir(str(dataset)+'\\'+i+'_dataset'+'\\'+v+'\\'+f'{v}_2'):
            pass
        else:
            if os.path.exists(str(root)+'\\'+'temp_'+i+'\\'+f'{v}_1.mp4') and os.path.exists(str(root)+'\\'+'temp_'+i+'\\'+f'{v}_2.mp4'):
                pass
            else:
                original_video=VideoFileClip(str(video_path)+'\\'+v+'.mp4')
                duration=original_video.duration
                print(duration)
                clip1=original_video.subclip(0,(duration/2))
                #try:
                    #os.remove(pathlib.Path(__file__).parent.absolute().joinpath(video_path,f'{v}_1.mp4'))
                    #os.remove(pathlib.Path(__file__).parent.absolute().joinpath(video_path,f'{v}_2.mp4'))
                #except:
                    #pass
                clip1.write_videofile(str(pathlib.Path(__file__).parent.absolute().joinpath(str(root)+'\\'+'temp_'+i,f'{v}_1.mp4')))
                clip2=original_video.subclip((duration/2),duration)
                clip2.write_videofile(str(pathlib.Path(__file__).parent.absolute().joinpath(str(root)+'\\'+'temp_'+i,f'{v}_2.mp4')))
        
    for vi in vid:
        vi=vi.replace('.mp4','')
        try:
            os.mkdir(str(dataset)+'\\'+i+'_dataset'+'\\'+vi)
        except:
            pass
        if os.path.isdir(str(dataset)+'\\'+i+'_dataset'+'\\'+vi+'\\'+f'{vi}_1') and os.path.exists(str(dataset)+'\\'+i+'_dataset'+'\\'+vi+'\\'+f'{vi}_2'):
            pass
        else:
            vid1=f'{vi}_1'
            vid2=f'{vi}_2'
            #vid1=vid1.replace('.mp4','')
            #vid2=vid2.replace('.mp4','')
            temp=str(dataset)+'\\'+i+'_dataset'+'\\'+vi
            print(temp)
            temp1='temp_'+i
            temp3=str(dataset)+'\\'+i
            print(temp1)
            save_landmarks_from_new_video(vid1,temp1,temp)
            save_landmarks_from_new_video(vid2,temp1,temp)
            new_load_reference_signs([vid1,vid2],temp3)
        
    try:
        shutil.rmtree('temp_'+i)
    except:
        pass
    

#try:
#    os.makedirs(outpath)
#except FileExistsError:
#    # directory already exists
#    pass
#original_video = VideoFileClip(path)
#duration = original_video.duration
#print(duration)
#clip1=original_video.subclip(0,(duration/2))
#try:
#    os.remove(pathlib.Path(__file__).parent.absolute().joinpath(outpath,f'{vid}_1.mp4'))
#    os.remove(pathlib.Path(__file__).parent.absolute().joinpath(outpath,f'{vid}_2.mp4'))
#except:
#    pass
#clip1.write_videofile(str(pathlib.Path(__file__).parent.absolute().joinpath(outpath,f'{vid}_1.mp4')))
#clip2=original_video.subclip((duration/2),duration)
#clip2.write_videofile(str(pathlib.Path(__file__).parent.absolute().joinpath(outpath,f'{vid}_2.mp4')))
#return
#trim('B',r'D:/FYP/Sign-Language-Recognition--MediaPipe-DTW/videos/Alphabets/B.mp4',r'D:\FYP\Sign-Language-Recognition--MediaPipe-DTW\temp_videos\B')

