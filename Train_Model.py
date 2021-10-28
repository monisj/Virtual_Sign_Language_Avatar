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
import Video_train as vt
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical

mp_holistic = mp.solutions.holistic # Holistic model
mp_drawing = mp.solutions.drawing_utils # Drawing utilities

def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # COLOR CONVERSION BGR 2 RGB
    image.flags.writeable = False                  # Image is no longer writeable
    results = model.process(image)                 # Make prediction
    image.flags.writeable = True                   # Image is now writeable 
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # COLOR COVERSION RGB 2 BGR
    return image, results

def draw_landmarks(image, results):
    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACE_CONNECTIONS) # Draw face connections
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS) # Draw pose connections
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS) # Draw left hand connections
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS) # Draw right hand connections

def draw_styled_landmarks(image, results):
    # Draw face connections
    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACE_CONNECTIONS, 
                             mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1), 
                             mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
                             ) 
    # Draw pose connections
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                             mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4), 
                             mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
                             ) 
    # Draw left hand connections
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                             mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4), 
                             mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
                             ) 
    # Draw right hand connections  
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                             mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4), 
                             mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                             )


def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
    face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([pose, face, lh, rh])



pose = []
for res in results.pose_landmarks.landmark:
    test = np.array([res.x, res.y, res.z, res.visibility])
    pose.append(test)

pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(132)
face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(1404)
lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)



face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(1404)
result_test = extract_keypoints(results)
if input("Press Enter to save the Video Nodes !!"):
    np.save('0', result_test)

# Path for exported data, numpy arrays
DATA_PATH = data_path=pathlib.Path.cwd().joinpath('MP_DATA')

# Actions that we try to detect
actions = np.array(['hello', 'alright', 'Assalam-o-Alaikum','good afternoon','good evening','good morning'])

# Thirty videos worth of data
no_sequences = 14

# Videos are going to be 30 frames in length
sequence_length = 14

# Folder start
start_folder = 0


# Set mediapipe model 
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    
    # NEW LOOP
    # Loop through actions
    for action in actions:
        if pathlib.Path(DATA_PATH).joinpath(action).is_dir():
            print(action)
            continue
        cap = cv2.VideoCapture(f'{action}.mp4')
        # Loop through sequences aka videos
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps    = cap.get(cv2.CAP_PROP_FPS)
        start=round(fps*1.5)
        end=round(length-fps*2)
        mid=(start+end)//2
        end=mid-fps
        cap.set(cv2.CAP_PROP_POS_FRAMES, start)
        loop=1
        frame_counter = start
        flip=False
        while loop <= no_sequences:
            # Loop through video length aka sequence length
            next=False
            f=0
            while next is not True:

                # Read feed
                ret, frame = cap.read()
                if flip:
                    frame=cv2.flip(frame,1)
                frame_counter+=1
                f+=1
                #print(frame_counter)
                if frame_counter == end:
                    #print(loop,end)
                    #print(loop//2)
                    if flip is False:
                        flip=True
                    else:
                        flip=False
                        if loop%2 == 0 and loop >= 2:
                            start=round(fps*1.5)
                            end=mid-fps
                        else:
                            start=mid+fps
                            end=round(length-fps*2)
                        loop+=1
                    next=True
                    frame_counter = start
                    cap.set(cv2.CAP_PROP_POS_FRAMES, start)
                    continue

                # Make detections
                image, results = mediapipe_detection(frame, holistic)

                # Draw landmarks
                draw_styled_landmarks(image, results)
                
                
                cv2.imshow('OpenCV Feed', image)
                # NEW Export keypoints
                keypoints = extract_keypoints(results)
                pathlib.Path(data_path).joinpath(action,str(loop)).mkdir(parents=True, exist_ok=True)
                npy_path = pathlib.Path(data_path).joinpath(action,str(loop),str(f))
                np.save(npy_path, keypoints)

                # Break gracefully
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
                    
    cap.release()
    cv2.destroyAllWindows()


    
