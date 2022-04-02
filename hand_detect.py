# Importing Libraries
import cv2
import mediapipe as mp
 
# Used to convert protobuf message to a dictionary.
from google.protobuf.json_format import MessageToDict
 
# Initializing the Model
mp_holistic= mp.solutions.holistic
hands = mp_holistic.Holistic(
    static_image_mode=False,
    min_detection_confidence=0.3,
    min_tracking_confidence=0.3)
 
# Start capturing video from webcam
cap = cv2.VideoCapture(0)
a=0
while True:
    # Read video frame by frame
    success, img = cap.read()
 
    # Flip the image(frame)
    img = cv2.flip(img, 1)
 
    # Convert BGR image to RGB image
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
 
    # Process the RGB image
    results = hands.process(imgRGB)
    
    # If hands are present in image(frame)
    if results.left_hand_landmarks:
        a+=1
        print("LEFT HAND={}".format(a))
    elif results.right_hand_landmarks:
        a+=1
        print("RIGHT HAND={}".format(a))
    elif results.right_hand_landmarks==True and results.left_hand_landmarks==True:
        a+=1
        print("BOTH HANDS={}".format(a))
 
        # Both Hands are present in image(frame)
       
 
    # Display Video and when 'q'
    # is entered, destroy the window
    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break