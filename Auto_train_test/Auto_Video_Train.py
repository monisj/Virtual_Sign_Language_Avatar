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
#import tflearn
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical 
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import TensorBoard
from sklearn.metrics import multilabel_confusion_matrix, accuracy_score
from scipy import stats
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout #For CNN
import tensorflow.keras.utils as tf


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
    # Draw face connections
    #mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION, 
     #                        mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1), 
     #                        mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
      #                       ) 
    # Draw pose connections
    #mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
    #                         mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=2), 
     #                        mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
     #                        ) 
    # Draw left hand connections
    #mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
    #                         mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=2), 
     #                        mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
     #                        ) 
    # Draw right hand connections  
    #mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
     #                        mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
     #                        mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
      #                       )

    mp_drawing.draw_landmarks(
          image,
          resilts.left_hand_landmarks,
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





#alphabet=input("Enter Variable to Train=")



def train(act,DATA_PATH):
    # Actions that we try to detect
    actions = np.array([act,'NG'])
    no_f=os.listdir(str(DATA_PATH)+'\\'+str(actions[0])+'\\')
    no_f=len(no_f)
    print("files=",no_f)

    # Fifteen videos worth of data
    no_sequences = no_f

    # Videos are going to be 15 frames in length
    sequence_length = no_f

    # Folder start
    start_folder = 0

    label_map = {label:num for num, label in enumerate(actions)}
    print(label_map)
    sequences, labels = [], []
    for action in actions:
        for sequence in np.array(os.listdir(os.path.join(DATA_PATH, action))).astype(int):
            window = []
            for frame_num in range(1,sequence_length):
                res = np.load(os.path.join(DATA_PATH, action,str(sequence) ,"{}.npy".format(frame_num)))
                window.append(res)
            sequences.append(window)
            labels.append(label_map[action])

    

    np.array(sequences).shape
    np.array(labels).shape
    X = np.array(sequences)
    X.shape
    y = to_categorical(labels).astype(int)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05)
    y_test.shape

    log_dir = os.path.join('Logs')
    tb_callback = TensorBoard(log_dir=log_dir)

    model = Sequential()
    model.add(LSTM(64, return_sequences=True, activation='relu',input_shape=(no_f-1,126)))
    model.add(LSTM(128, return_sequences=True, activation='relu'))
    model.add(LSTM(64, return_sequences=False, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(actions.shape[0], activation='softmax'))


    model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])
    model.fit(X_train, y_train, epochs=25, callbacks=[tb_callback],use_multiprocessing=True)
    print(model.summary())

    res = model.predict(X_test)
    actions[np.argmax(res[0])]
    actions[np.argmax(y_test[1])]

    #Save Weights
    model.save('model_files'+'\\'+actions[0]+'.h5')
    model.load_weights('model_files'+'\\'+actions[0]+'.h5')

    #Evaluation using Confusion Matrix and Accuracy
    yhat = model.predict(X_test)
    ytrue = np.argmax(y_test, axis=1).tolist()
    yhat = np.argmax(yhat, axis=1).tolist()
    multilabel_confusion_matrix(ytrue, yhat)
    accuracy_score(ytrue, yhat)

    

DATA_PATH = data_path=pathlib.Path.cwd().joinpath('Auto_train_data')
#path_video=data_path=pathlib.Path.cwd().joinpath('Videos\Science')
l=os.listdir(DATA_PATH)
li=[x.split('.')[0] for x in l]
print(li)

for items in li:
    train(items,DATA_PATH)
