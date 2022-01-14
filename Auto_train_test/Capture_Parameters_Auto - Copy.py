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

# Path for exported data, numpy arrays
DATA_PATH = data_path=pathlib.Path.cwd().joinpath('Auto_train_data')
path_video=data_path=pathlib.Path.cwd().joinpath('Videos')
print(path_video)
# Actions that we try to detect
actions = np.array(['A'])

# Fifteen videos worth of data
no_sequences = 30

# Videos are going to be 15 frames in length
sequence_length = 30

# Folder start
start_folder = 0

for action in actions: 
    for sequence in range(no_sequences):
        try: 
            os.makedirs(os.path.join(DATA_PATH, action, str(sequence)))
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
        cap = cv2.VideoCapture(f'{path_video}/{action}.mp4')
        # Loop through sequences aka videos
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps    = cap.get(cv2.CAP_PROP_FPS)
        start=round(fps*2)
        end=round(length-fps*2)
        mid=(start+end)//2
        end=mid-28
        cap.set(cv2.CAP_PROP_POS_FRAMES, start)
        loop=1
        frame_counter = start
        flip=False
        temp_stop = 0
        while loop <= no_sequences:
            print(loop,"frame")
            # Loop through video length aka sequence length
            next=False
            f=0
            while next is not True:

                # Read feed
                ret, frame = cap.read()
                frame=rescale(frame,32)
                frame_counter+=1
                f+=1
                #print(frame_counter)
                if frame_counter == end and temp_stop !=1:
                    next=False
                    temp_stop=1
                    print("Temp end")
                    frame_counter = start
                    #frame_counter = start
                    cap.set(cv2.CAP_PROP_POS_FRAMES, start)
                    #continue
                elif frame_counter == end and temp_stop ==1:
                    loop+=1
                    next=True
                    temp_stop=0
                    print("end")
                    frame_counter = start
                    cap.set(cv2.CAP_PROP_POS_FRAMES, start)
                    continue

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
                    
        cap.release()
    cv2.destroyAllWindows()
#label_map = {label:num for num, label in enumerate(actions)}
#print(label_map)

#sequences, labels = [], []
#for action in actions:
#    for sequence in np.array(os.listdir(os.path.join(DATA_PATH, action))).astype(int):
#        window = []
#        for frame_num in range(1,sequence_length+1):
#            res = np.load(os.path.join(DATA_PATH, action, str(sequence), "{}.npy".format(frame_num)))
#            window.append(res)
#        sequences.append(window)
#        labels.append(label_map[action])

    
#np.array(sequences).shape
#np.array(labels).shape
#X = np.array(sequences)
#X.shape
#y = to_categorical(labels).astype(int)
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05)
#y_test.shape

#log_dir = os.path.join('Logs')
#tb_callback = TensorBoard(log_dir=log_dir)

#model = Sequential()
#model.add(LSTM(64, return_sequences=True, activation='relu',input_shape=(15,1662)))
#model.add(LSTM(128, return_sequences=True, activation='relu'))
#model.add(LSTM(64, return_sequences=False, activation='relu'))
#model.add(Dense(64, activation='relu'))
#model.add(Dense(32, activation='relu'))
#model.add(Dense(actions.shape[0], activation='softmax'))


#model = tflearn.DNN(net, tensorboard_verbose=0)
#model.fit(X_train, y_train, validation_set=(X_test, y_test), snapshot_step=100,n_epoch=10)
#res = [.7, 0.2, 0.1]
#actions[np.argmax(res)]

#model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])
#model.fit(X_train, y_train, epochs=500, callbacks=[tb_callback])
#print(model.summary())

#res = model.predict(X_test)
#actions[np.argmax(res[0])]
#actions[np.argmax(y_test[1])]

#Save Weights
#model.save('action.h5')
#model.load_weights('action.h5')

#Evaluation using Confusion Matrix and Accuracy
#yhat = model.predict(X_test)
#ytrue = np.argmax(y_test, axis=1).tolist()
#yhat = np.argmax(yhat, axis=1).tolist()
#multilabel_confusion_matrix(ytrue, yhat)
#accuracy_score(ytrue, yhat)




