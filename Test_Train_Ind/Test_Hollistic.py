#Dependencies
#!pip install tensorflow==2.4.1 tensorflow-gpu==2.4.1 opencv-python mediapipe sklearn matplotlib

import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
import time
import mediapipe as mp

mp_holistic = mp.solutions.holistic # Holistic model
mp_drawing = mp.solutions.drawing_utils # Drawing utilities
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # COLOR CONVERSION BGR 2 RGB
    image.flags.writeable = False                  # Image is no longer writeable
    results = model.process(image)                 # Make prediction using Mediapipe
    image.flags.writeable = True                   # Image is now writeable 
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # COLOR COVERSION RGB 2 BGR
    return image, results

#For more Reformed Landmarks
def draw_styled_landmarks(image, results):
    # Draw face connections
    mp_drawing.draw_landmarks(image,results.left_hand_landmarks,mp_hands.HAND_CONNECTIONS,mp_drawing_styles.get_default_hand_landmarks_style(),mp_drawing_styles.get_default_hand_connections_style())
    mp_drawing.draw_landmarks(image,results.right_hand_landmarks,mp_hands.HAND_CONNECTIONS,mp_drawing_styles.get_default_hand_landmarks_style(),mp_drawing_styles.get_default_hand_connections_style())


#Camera Feed for Initial Setup Run for Test
#Setting Mediapipe Model
sequence=[]
sentence=[]
threshold =0.4

cap= cv2.VideoCapture(0) #Change for a virtual video feed might need to trial and error
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    
    while cap.isOpened():
        ret, frame = cap.read()
        
        image,results=mediapipe_detection(frame, holistic)
        print(results) #printing results
        
        
        #Draw landmarks
        draw_styled_landmarks(frame, results)
        
        #Prediction Logic
        #keypoints = extract_keypoints(results) #Uncomment to verify the model
        #sequence.insert(0,keypoints)
        #sequence=sequence[:15]
        
        #if len(sequence)==15:
            #res=model.predict(np.expand_dims(sequence,axis=0))[0]
            #print(actions[np.argmax(res)])
            
        cv2.imshow('OpenCv Cam Feed',frame)
        
        if cv2.waitKey(10) & 0xFF == ord('q'):  #Press q to quit 
            break
    cap.release()
    cv2.destroyAllWindows()
