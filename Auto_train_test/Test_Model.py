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
#import Video_train as vt
from sklearn.model_selection import train_test_split
from tensorflow import keras
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
# Path for exported data, numpy arrays

#alphabet=input("Enter Variable to Predict=")

<<<<<<< HEAD
DATA_PATH = data_path=pathlib.Path.cwd().joinpath('Model_Count_files')

# Actions that we try to detect
actions = np.array(['A','NG'])
#no_f=os.listdir(str(DATA_PATH)+'\\'+str(actions[0])+'\\'+str(0)+'\\')
f = open(str(DATA_PATH)+'\\'+str(actions[0])+".txt", "r")
no_f=int(f.read())-1

print("files=",no_f)

# Thirty videos worth of data
no_sequences = no_f

# Videos are going to be 30 frames in length
sequence_length = no_f
=======
DATA_PATH = data_path=pathlib.Path.cwd().joinpath('Auto_train_data')

# Actions that we try to detect
actions = np.array(['B','NG'])

# Thirty videos worth of data
no_sequences = 29

# Videos are going to be 30 frames in length
sequence_length = 29
>>>>>>> bdc99018a82ec7840c03a68115ed26f33c6c7e72

# Folder start
start_folder = 0

def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # COLOR CONVERSION BGR 2 RGB
    image.flags.writeable = False                  # Image is no longer writeable
    results = model.process(image)                 # Make prediction
    image.flags.writeable = True                   # Image is now writeable 
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # COLOR COVERSION RGB 2 BGR
    return image, results

def draw_landmarks(image, results):
    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION) # Draw face connections
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS) # Draw pose connections
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS) # Draw left hand connections
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS) # Draw right hand connections

def draw_styled_landmarks(image, results):
    # Draw face connections
#    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION, 
#                             mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1), 
#                             mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
#                             ) 
    # Draw pose connections
#    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
#                             mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4), 
#                             mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
#                             ) 
    # Draw left hand connections
#    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
#                             mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4), 
#                             mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
#                             ) 
    # Draw right hand connections  
#    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
#                             mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4), 
#                             mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
#                             )

    mp_drawing.draw_landmarks(image,results.left_hand_landmarks,mp_hands.HAND_CONNECTIONS,mp_drawing_styles.get_default_hand_landmarks_style(),mp_drawing_styles.get_default_hand_connections_style())
    mp_drawing.draw_landmarks(image,results.right_hand_landmarks,mp_hands.HAND_CONNECTIONS,mp_drawing_styles.get_default_hand_landmarks_style(),mp_drawing_styles.get_default_hand_connections_style())

def extract_keypoints(results):
    #pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
    #face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([ lh, rh])


def prob_viz(res, actions, input_frame):
    colors = [(245,117,16), (117,245,16), (16,117,245)]
    output_frame = input_frame.copy()
    for num, prob in enumerate(res):
        cv2.rectangle(output_frame, (0,60+num*40), (int(prob*100), 90+num*40), colors[num], -1)
<<<<<<< HEAD
        print("Accuracy of {} = {:.2f}%".format(actions[num],prob*100))
=======
        print("Accuracy of {} =".format(actions[num]),prob)
>>>>>>> bdc99018a82ec7840c03a68115ed26f33c6c7e72
        cv2.putText(output_frame, actions[num], (0, 85+num*40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
        
    return output_frame


<<<<<<< HEAD
model = keras.models.load_model('model_files'+'\\'+actions[0]+'.h5')
model.load_weights('model_files'+'\\'+actions[0]+'.h5')


=======
model = keras.models.load_model('actions_auto.h5')
model.load_weights('actions_auto.h5')
>>>>>>> bdc99018a82ec7840c03a68115ed26f33c6c7e72
colors = [(245,117,16), (117,245,16), (16,117,245)]
#plt.figure(figsize=(18,18))
#plt.imshow(prob_viz(res, actions, image, colors))
#sequence.reverse()
#len(sequence)
#sequence.append('def')
#sequence.reverse()
#sequence[-30:]
res = [.7, 0.2, 0.1]


# 1. New detection variables
sequence = []
sentence = []
predictions = []
<<<<<<< HEAD
threshold = 0.1
=======
threshold = 0.5
>>>>>>> bdc99018a82ec7840c03a68115ed26f33c6c7e72
colors = [(245,117,16), (117,245,16), (16,117,245)]


cap = cv2.VideoCapture(0)
<<<<<<< HEAD
with mp_holistic.Holistic(min_detection_confidence=0.1, min_tracking_confidence=0.1) as holistic:
=======
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
>>>>>>> bdc99018a82ec7840c03a68115ed26f33c6c7e72
    while cap.isOpened():
       
        # Read feed
        ret, frame = cap.read()

        # Make detections
        image, results = mediapipe_detection(frame, holistic)
        #print(results)
        
        # Draw landmarks
        draw_styled_landmarks(image, results)
        
        # 2. Prediction logic
        keypoints = extract_keypoints(results)
        sequence.append(keypoints)
        #sequence.reverse()
<<<<<<< HEAD
        sequence = sequence[-no_f:]
        #print(len(sequence))
        if len(sequence) == no_f:
=======
        sequence = sequence[-29:]
        #print(len(sequence))
        if len(sequence) == 29:
>>>>>>> bdc99018a82ec7840c03a68115ed26f33c6c7e72
            #x=np.array(sequence)
            #x=x.reshape(15,126,1)
            res = model.predict(np.expand_dims(sequence, axis=0),use_multiprocessing=True)[0] #Work on this side
            #print(actions[np.argmax(res)],"Gesture")
            predictions.append(np.argmax(res))
            
            
        #3. Viz logic
<<<<<<< HEAD
            if np.unique(predictions[-30:])[0]==np.argmax(res): 
=======
            if np.unique(predictions[-10:])[0]==np.argmax(res): 
>>>>>>> bdc99018a82ec7840c03a68115ed26f33c6c7e72
                if res[np.argmax(res)] > threshold: 
                    if len(sentence) > 0: 
                        if actions[np.argmax(res)] != sentence[-1]:
                            sentence.append(actions[np.argmax(res)])
                    else:
                        sentence.append(actions[np.argmax(res)])

<<<<<<< HEAD
            if len(sentence) > 1: 
                sentence =[]
=======
            if len(sentence) > 5: 
                sentence = sentence[-5]
>>>>>>> bdc99018a82ec7840c03a68115ed26f33c6c7e72
                print(actions[np.argmax(res)],"Gesture")
            # Viz probabilities
            image = prob_viz(res, actions, image)
            
        cv2.rectangle(image, (0,0), (640, 40), (245, 117, 16), -1)
        cv2.putText(image, ' '.join(sentence), (3,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
        # Show to screen
        cv2.imshow('OpenCV Feed', image)

        # Break gracefully
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
