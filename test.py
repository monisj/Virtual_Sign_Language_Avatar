import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
import time
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
import enum

mp_holistic = mp.solutions.holistic # Holistic model
mp_drawing = mp.solutions.drawing_utils # Drawing utilities


class HandLandmark(enum.IntEnum):
    """The 21 hand landmarks."""
    WRIST = 0
    THUMB_CMC = 1
    THUMB_MCP = 2
    THUMB_IP = 3
    THUMB_TIP = 4
    INDEX_FINGER_MCP = 5
    INDEX_FINGER_PIP = 6
    INDEX_FINGER_DIP = 7
    INDEX_FINGER_TIP = 8
    MIDDLE_FINGER_MCP = 9
    MIDDLE_FINGER_PIP = 10
    MIDDLE_FINGER_DIP = 11
    MIDDLE_FINGER_TIP = 12
    RING_FINGER_MCP = 13
    RING_FINGER_PIP = 14
    RING_FINGER_DIP = 15
    RING_FINGER_TIP = 16
    PINKY_MCP = 17
    PINKY_PIP = 18
    PINKY_DIP = 19
    PINKY_TIP = 20

def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # COLOR CONVERSION BGR 2 RGB
    image.flags.writeable = False                  # Image is no longer writeable
    results = model.process(image)                 # Make prediction
    image.flags.writeable = True                   # Image is now writeable 
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # COLOR COVERSION RGB 2 BGR
    return image, results

def draw_styled_landmarks(image, results):
    mp_drawing.draw_landmarks(
            image,
            landmark_list=results.left_hand_landmarks,
            connections=mp_holistic.HAND_CONNECTIONS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(
                color=(232, 254, 255), thickness=1, circle_radius=1
            ),
            connection_drawing_spec=mp_drawing.DrawingSpec(
                color=(255, 249, 161), thickness=2, circle_radius=2
            ),
        )
        # Draw right hand connections
#     landmark {
#   x: 0.26913756132125854
#   y: 0.3214127719402313
#   z: -0.045400459319353104
# }

    points_name= frozenset(["Wrist","Thumb_CMC","Thumb_MCP","Thumb_IP","Thumb_Tip",
        "Index_Finger_MPC","Index_Finger_PIP"])

    if results.right_hand_landmarks==None:
        pass
    else:
        landmark2 = [
          results.right_hand_landmarks.landmark[0],
          results.right_hand_landmarks.landmark[1], 
          results.right_hand_landmarks.landmark[2],
          results.right_hand_landmarks.landmark[3], 
          results.right_hand_landmarks.landmark[4],
          results.right_hand_landmarks.landmark[5],
          results.right_hand_landmarks.landmark[6],
          results.right_hand_landmarks.landmark[7]
      ]
        landmark_subset=landmark_pb2.NormalizedLandmarkList(
      landmark = landmark2
)

        HAND_CONNECTIONS = frozenset([(HandLandmark.WRIST, HandLandmark.THUMB_CMC),
            (HandLandmark.THUMB_CMC, HandLandmark.THUMB_MCP),
            (HandLandmark.THUMB_MCP, HandLandmark.THUMB_IP),
            (HandLandmark.THUMB_IP, HandLandmark.THUMB_TIP),
            (HandLandmark.WRIST, HandLandmark.INDEX_FINGER_MCP),
            (HandLandmark.INDEX_FINGER_MCP, HandLandmark.INDEX_FINGER_PIP),
            (HandLandmark.INDEX_FINGER_PIP, HandLandmark.INDEX_FINGER_DIP),
        ])

        mp_drawing.draw_landmarks(
                image,
                landmark_list=landmark_subset,
                connections=HAND_CONNECTIONS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(
                    color=(232, 254, 255), thickness=1, circle_radius=2
                ),
                connection_drawing_spec=mp_drawing.DrawingSpec(
                    color=(255, 249, 161), thickness=2, circle_radius=2
                ),
            )

cap = cv2.VideoCapture(0)
# Set mediapipe model 
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():

        # Read feed
        ret, frame = cap.read()

        # Make detections
        image, results = mediapipe_detection(frame, holistic)


        # Draw landmarks
        draw_styled_landmarks(image, results)

        # Show to screen
        cv2.imshow('OpenCV Feed', image)

        # Break gracefully
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()