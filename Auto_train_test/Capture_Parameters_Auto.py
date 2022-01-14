import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
import time
import mediapipe as mp
from imutils.video import FileVideoStream
from imutils.video import FPS
import imutils
import pathlib
import shutil
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import TensorBoard
from sklearn.metrics import multilabel_confusion_matrix, accuracy_score
from scipy import stats

mp_holistic = mp.solutions.holistic # Holistic model
mp_drawing = mp.solutions.drawing_utils # Drawing utilities
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # COLOR CONVERSION BGR 2 RGB
    image.flags.writeable = False                  # Image is no longer writeable
    results = model.process(image)                 # Make prediction
    image.flags.writeable = True                   # Image is now writeable 
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # COLOR COVERSION RGB 2 BGR
    return image, results


def draw_styled_landmarks(image, results):
    mp_drawing.draw_landmarks(image,
          results.left_hand_landmarks,
          mp_hands.HAND_CONNECTIONS,
          mp_drawing_styles.get_default_hand_landmarks_style(),
          mp_drawing_styles.get_default_hand_connections_style())

    mp_drawing.draw_landmarks(
          image,
          results.right_hand_landmarks,
          mp_hands.HAND_CONNECTIONS,
          mp_drawing_styles.get_default_hand_landmarks_style(),
          mp_drawing_styles.get_default_hand_connections_style())
def extract_keypoints(results):
    #pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
    #face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([ lh, rh])

# rescale the frame by function
def rescale(frame,scale):
    #get the webcam size
    height, width, channels = frame.shape
    #prepare the crop
    centerX,centerY=int(height/3),int(width/3)
    radiusX,radiusY= int(scale*height/96),int(scale*width/96)

    minX,maxX=centerX-radiusX,centerX+radiusX
    minY,maxY=centerY-radiusY,centerY+radiusY
    cropped = frame[minX:maxX, minY:maxY]
    return cv2.resize(cropped, (width, height))

def cap(act,DATA_PATH,path_video):
    #act=input("Enter Variable for Capture=") uncomment for mannual capture
    # Path for exported data, numpy arrays
    
    print(path_video)
    # Actions that we try to detect
    actions = np.array([act])

    # Fifteen videos worth of data
    #no_sequences = 50

    # Videos are going to be 15 frames in length
    #sequence_length = 50

    # Folder start
    start_folder = 0
    try:
        os.makedirs(os.path.join(DATA_PATH, actions[0], str(0)))
    except:
        pass



        
    # Set mediapipe model 
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        # NEW LOOP
        # Loop through actions
        for action in actions:

            #if pathlib.Path(DATA_PATH).joinpath(action).is_dir():
            print(action)
                #continue
            print("Going Loop")
            cap = cv2.VideoCapture(0)
            # Loop through sequences aka videos
            length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            start=20
            end=round(length-fps*2)
            mid=(length//2)
            end=mid-28
            cap.set(cv2.CAP_PROP_POS_FRAMES, start)
            loop=1
            frame_counter = start
            flip=False
            temp_stop = 0
            next=False
            while loop <= mid:
                print(loop,"frame")
                # Loop through video length aka sequence length
                f=0
                while next is not True:

                    # Read feed
                    ret, frame = cap.read()
                    #frame=rescale(frame,32)
                    frame_counter+=1
                    f+=1
                    #print(frame_counter)
                    if frame_counter == mid:
                        next=True
                        print("end")
                        frame_counter = start
                        cap.set(cv2.CAP_PROP_POS_FRAMES, start)
                        break

                    # Make detections
                    image, results = mediapipe_detection(frame, holistic)

                    # Draw landmarks
                    draw_styled_landmarks(image, results)
                
                
                    cv2.imshow('OpenCV Feed', image) #Uncomment to enable
                    # NEW Export keypoints
                    keypoints = extract_keypoints(results)
                    #pathlib.Path(data_path).joinpath(action,str(loop)).mkdir(parents=True, exist_ok=True)
                    npy_path = os.path.join(DATA_PATH, action, str(loop-1), str(f))
                
                    #npy_path = pathlib.Path(data_path).joinpath(action,str(loop),str(f))
                    np.save(npy_path, keypoints)
                    print(npy_path,"Saving Path Points")
                
                    # Break gracefully
                    if cv2.waitKey(5) & 0xFF == ord('q'):
                        break
                loop=mid+1
                    
            cap.release()
        cv2.destroyAllWindows()

    #Counting no_of_sequences in directory
    no_f=os.listdir(str(DATA_PATH)+'\\'+str(actions[0])+'\\'+str(0)+'\\')
    no_f=len(no_f)
    print("files=",no_f)


    for action in actions: 
        for sequence in range(1,no_f+1):
            try: 
                os.makedirs(os.path.join(DATA_PATH, action, str(sequence)))
            except:
                pass


    for fi in range(1,no_f+1):
        for fi2 in range(1,no_f+1):
            print("dir copy=",str(DATA_PATH)+'\\'+str(actions[0])+"\\"+str(fi)+'\\'+str(fi)+'.npy') Uncomment for real results
            shutil.copy(str(DATA_PATH)+'\\'+str(actions[0])+'\\'+str(0)+'\\'+str(fi)+'.npy',str(DATA_PATH)+'\\'+str(actions[0])+'\\'+str(fi)+'\\'+str(fi2)+'.npy')

DATA_PATH = data_path=pathlib.Path.cwd().joinpath('Auto_train_data')
path_video=data_path=pathlib.Path.cwd().joinpath('Videos\Science')
l=os.listdir(path_video)
li=[x.split('.')[0] for x in l]
print(li)
       

for items in li:
    cap(items,DATA_PATH,path_video)

