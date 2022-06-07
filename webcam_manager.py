from asyncio.windows_events import INFINITE
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
import enum
from utils.drawing_utils import draw_landmarks
from utils.drawing_styles import get_default_hand_landmarks_style,get_default_hand_connections_style,DrawingSpec


WHITE_COLOR = (245, 242, 226)
RED_COLOR = (25, 35, 240)

HEIGHT = 600


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

class WebcamManager(object):
    """Object that displays the Webcam output, draws the landmarks detected and
    outputs the sign prediction
    """

    def __init__(self):
        self.sign_detected = ""
        self.sign=[" "]
        self.dist=[" "]
        self.val=""
        self.sentences_pass_on=False
        self.attempt=4
        self.temp=0

    def update(
        self, frame: np.ndarray, results, sign_detected, is_recording,sign,dist,val,sentences_pass_on,attempt
    ):
        self.sign_detected = sign_detected
        self.sign=sign
        self.dist=dist
        self.val=val
        self.sentences_pass_on=sentences_pass_on
        self.attempt=attempt
        # Draw landmarks

        self.draw_landmarks(frame, results)
        test_no=False
        WIDTH = int(HEIGHT * len(frame[0]) / len(frame))
        # Resize frame
        frame = cv2.resize(frame, (WIDTH, HEIGHT), interpolation=cv2.INTER_AREA)

        # Flip the image vertically for mirror effect
        frame = cv2.flip(frame, 1)
        # Write result if there is
        frame,acc = self.draw_text(frame)

        # Chose circle color
        color = WHITE_COLOR
        if is_recording:
            color = RED_COLOR
            self.temp=1    
        if is_recording==False and self.temp==1:
            test_no=True
            self.temp=0

        # Update the frame
        cv2.circle(frame, (30, 30), 20, color, -1)
        #cv2.imshow("OpenCV Feed", frame)
        return frame,acc,test_no

    def update2(self, frame: np.ndarray, results,frame_counter,leftlist,rightlist):
        
        # Draw landmarks

        self.draw_landmarks_2(frame, results,frame_counter,leftlist,rightlist)

        WIDTH = int(HEIGHT * len(frame[0]) / len(frame))
        # Resize frame
        frame = cv2.resize(frame, (WIDTH, HEIGHT), interpolation=cv2.INTER_AREA)

        # Flip the image vertically for mirror effect
        frame = cv2.flip(frame, 1)

        # Write result if there is


        # Chose circle color
        color = WHITE_COLOR
        
        #cv2.imshow("OpenCV Feed", frame)
        return frame

    def draw_text(
        self,
        frame,
        font=cv2.FONT_HERSHEY_COMPLEX,
        font_size=1,
        font_thickness=2,
        offset=int(HEIGHT * 0.02),
        bg_color=(245, 242, 176, 0.85),
    ):
        acc2=0
        window_w = int(HEIGHT * len(frame[0]) / len(frame))
        list1=[]
        if self.attempt<3:
            self.sign_detected=f"Attempt Number {str(self.attempt)}"
            if self.sign_detected==self.val:
                    for i in range(len(self.sign)):
                        if self.sign[i]==self.val:
                            list1.append(self.dist[i])
                            if len(list1)==2:
                                if list1[0] == float('inf') or list1[1] ==float('inf'):
                                    pass
                                else:
                                    acc1=int(list1[0])
                                    acc2=int(list1[1])
                                    acc1=((acc1-60)/60)*100
                                    acc2=((acc2-60)/60)*100
                                    if int(list1[0])<60 or int(list1[1])<60:
                                        acc2=98.5
                                        break
                                    else:
                                        if acc1>100 or acc2>100:
                                            acc=((acc1+acc2)/2)//100
                                            acc=round(acc,2)
                                            acc2=acc
                                            break
                                        else:
                                            acc=(acc1+acc2)/2
                                            acc=round(acc,2)

                                            acc2=100-acc
                                            break
            elif self.sign_detected !=self.val:
                    for i in range(len(self.sign)):
                        if self.sign[i]==self.val:
                            list1.append(self.dist[i])
                            if len(list1)==2:
                                if list1[0]==float('inf') and list1[1]==float('inf'):
                                    
                                    acc2=0
                                else:    
                                    acc1=int(list1[0])
                                    acc2=int(list1[1])
                                    acc1=((acc1-60)/60)*100
                                    acc2=((acc2-60)/60)*100
                                    if int(list1[0])<60 or int(list1[1])<60:
                                        acc2=98.5
                                        break
                                    else:
                                        if acc1>100 or acc2>100:
                                            acc=((acc1+acc2)/2)//100
                                            acc=round(acc,2)
                                            acc2=acc
                                            break
                                        else:
                                            acc=(acc1+acc2)//2
                                            acc=round(acc,2)
                                            acc2=100-acc
                                            break
        elif self.attempt==3:
            self.sign_detected=f"Test Complete Press Submit"
        else:
            if self.sentences_pass_on==True:
                self.sign_detected=f'Predicted Sign ={self.sign_detected}'
            else:
                if self.sign_detected==self.val:
                    self.sign_detected=f'Predicted Correctly With Accuracy ={self.dist[0]}'
                    for i in range(len(self.sign)):
                        if self.sign[i]==self.val:
                            list1.append(self.dist[i])
                            if len(list1)==2:
                                if list1[0] == float('inf') or list1[1] ==float('inf'):
                                    pass
                                else:
                                    acc1=int(list1[0])
                                    acc2=int(list1[1])
                                    acc1=((acc1-60)/60)*100
                                    acc2=((acc2-60)/60)*100
                                    if int(list1[0])<60 or int(list1[1])<60:
                                        self.sign_detected='Predicted correctly With Accuracy =98.5'
                                        acc2=98.5
                                        break
                                    else:
                                        if acc1>100 or acc2>100:
                                            acc=((acc1+acc2)/2)//100
                                            acc=round(acc,2)
                                            self.sign_detected=f'Predicted correctly With Accuracy ={acc}'
                                            acc2=acc
                                            break
                                        else:
                                            acc=(acc1+acc2)/2
                                            acc=round(acc,2)
                                            self.sign_detected=f'Predicted correctly With Accuracy ={100-acc}'
                                            acc2=100-acc
                                            break
                elif self.sign_detected !=self.val:
                    for i in range(len(self.sign)):
                        if self.sign[i]==self.val:
                            list1.append(self.dist[i])
                            if len(list1)==2:
                                if list1[0]==float('inf') and list1[1]==float('inf'):
                                    self.sign_detected='No Sign Detected'
                                    acc2=0
                                else:    
                                    acc1=int(list1[0])
                                    acc2=int(list1[1])
                                    acc1=((acc1-60)/60)*100
                                    acc2=((acc2-60)/60)*100
                                    if int(list1[0])<60 or int(list1[1])<60:
                                        self.sign_detected='Predicted Incorrectly With Accuracy =98.5'
                                        acc2=98.5
                                        break
                                    else:
                                        if acc1>100 or acc2>100:
                                            acc=((acc1+acc2)/2)//100
                                            acc=round(acc,2)
                                            self.sign_detected=f'Predicted Incorrectly With Accuracy ={acc}'
                                            acc2=acc
                                            break
                                        else:
                                            acc=(acc1+acc2)//2
                                            acc=round(acc,2)
                                            self.sign_detected=f'Predicted Incorrectly With Accuracy ={100-acc}'
                                            acc2=100-acc
                                            break

        (text_w, text_h), _ = cv2.getTextSize(
            self.sign_detected, font, font_size, font_thickness
        )

        text_x, text_y = int((window_w - text_w) / 2), HEIGHT - text_h - offset

        cv2.rectangle(frame, (0, text_y - offset), (window_w, HEIGHT), bg_color, -1)
        cv2.putText(
            frame,
            self.sign_detected,
            (text_x, text_y + text_h + font_size - 1),
            font,
            1,
            (200, 50, 37),
            font_thickness,
        )
        return frame,acc2

    @staticmethod
    def draw_landmarks_2(image, results,frame_counter,leftlist,rightlist):
        mp_holistic = mp.solutions.holistic  # Holistic model
        mp_drawing = mp.solutions.drawing_utils  # Drawing utilities

        landmark_list=[]
        sequence=0
        import re
        if rightlist!=[] and leftlist==[]:
            for i in rightlist:
                y=re.findall('\d',i)
                sequence=y[0]
                
                if int(sequence)==int(frame_counter):
                    x=re.findall('([a-zA-Z]+(_[a-zA-Z]+)+)',i)
                    for i in x:
                        landmark_list.append(i[0])
                    
                    if results.right_hand_landmarks==None:
                        pass
                    else:
                        
                        landmark2=[] #Stores landmarks
                        list3=[] #Stores landmarks lines used to connect the points
                        temp=["Wrist","Thumb_CMC","Thumb_MCP","Thumb_IP","Thumb_Tip",
                                "Index_Finger_MPC","Index_Finger_PIP","Index_Finger_DIP","Index_Finger_TIP",
                                "Middle_Finger_MCP","Middle_Finger_PIP","Middle_Finger_DIP","Middle_Finger_TIP",
                                "Ring_Finger_MCP","Ring_Finger_PIP","Ring_Finger_DIP","Ring_Finger_TIP","Pinky_MCP",
                                "Pinky_PIP","Pinky_DIP","Pinky_TIP"] 
                        for i in landmark_list:
                            temp1=temp.index(i)
                            landmark2.append(temp1)
                        for i in range(len(landmark_list)-1):
                            temp1=temp.index(landmark_list[i])
                            temp2=temp.index(landmark_list[i+1])
                            list3.append((temp1,temp2))
                        mp_drawing.draw_landmarks(
                            image,
                            landmark_list=results.right_hand_landmarks,
                            connections=mp_holistic.HAND_CONNECTIONS,
                            landmark_drawing_spec=get_default_hand_landmarks_style(landmark2),
                            connection_drawing_spec=get_default_hand_connections_style(list3),
                            )
                else:
                    landmark_list=[]

        if rightlist==[] and leftlist!=[]:
            for i in leftlist:
                y=re.findall('\d',i)
                sequence=y[0]
                
                if int(sequence)==int(frame_counter):
                    x=re.findall('([a-zA-Z]+(_[a-zA-Z]+)+)',i)
                    for i in x:
                        landmark_list.append(i[0])
                    
                    if results.left_hand_landmarks==None:
                        pass
                    else:
                        
                        landmark2=[] #Stores landmarks
                        list3=[] #Stores landmarks lines used to connect the points
                        temp=["Wrist","Thumb_CMC","Thumb_MCP","Thumb_IP","Thumb_Tip",
                                "Index_Finger_MPC","Index_Finger_PIP","Index_Finger_DIP","Index_Finger_TIP",
                                "Middle_Finger_MCP","Middle_Finger_PIP","Middle_Finger_DIP","Middle_Finger_TIP",
                                "Ring_Finger_MCP","Ring_Finger_PIP","Ring_Finger_DIP","Ring_Finger_TIP","Pinky_MCP",
                                "Pinky_PIP","Pinky_DIP","Pinky_TIP"] 
                        for i in landmark_list:
                            temp1=temp.index(i)
                            landmark2.append(temp1)
                        for i in range(len(landmark_list)-1):
                            temp1=temp.index(landmark_list[i])
                            temp2=temp.index(landmark_list[i+1])
                            list3.append((temp1,temp2))                          
                        mp_drawing.draw_landmarks(
                                image,
                                landmark_list=results.left_hand_landmarks,
                                connections=mp_holistic.HAND_CONNECTIONS,
                                landmark_drawing_spec=get_default_hand_landmarks_style(landmark2),
                                connection_drawing_spec=get_default_hand_connections_style(list3),
                        )
                else:
                    landmark_list=[]        
        elif rightlist!=[] and leftlist!=[]:
            landmark_list_2=[]
            for i,j in zip(leftlist,rightlist):
                y=re.findall('\d',i)
                sequence=y[0]
                z=re.findall('\d',j)
                sequence2=z[0]
                
                if int(sequence)==int(frame_counter):
                    x=re.findall('([a-zA-Z]+(_[a-zA-Z]+)+)',i)
                    y=re.findall('([a-zA-Z]+(_[a-zA-Z]+)+)',j)
                    for i in x:
                        landmark_list.append(i[0])
                    for k in x:
                        landmark_list_2.append(k[0])

                    
                    if results.left_hand_landmarks==None:
                        pass
                    else:
                        
                        landmark2=[] #Stores landmarks Left
                        list3=[] #Stores landmarks lines used to connect the points Left
                        landmark3=[] #Stores landmarks Right
                        list4=[] #Stores landmarks lines used to connect the points Right
                        temp=["Wrist","Thumb_CMC","Thumb_MCP","Thumb_IP","Thumb_Tip",
                                "Index_Finger_MPC","Index_Finger_PIP","Index_Finger_DIP","Index_Finger_TIP",
                                "Middle_Finger_MCP","Middle_Finger_PIP","Middle_Finger_DIP","Middle_Finger_TIP",
                                "Ring_Finger_MCP","Ring_Finger_PIP","Ring_Finger_DIP","Ring_Finger_TIP","Pinky_MCP",
                                "Pinky_PIP","Pinky_DIP","Pinky_TIP"] 
                        for i in landmark_list:
                            temp1=temp.index(i)
                            landmark2.append(temp1)
                        for i in range(len(landmark_list)-1):
                            temp1=temp.index(landmark_list[i])
                            temp2=temp.index(landmark_list[i+1])
                            list3.append((temp1,temp2))
                        

                        for i in landmark_list_2:
                            temp1=temp.index(i)
                            landmark3.append(temp1)
                        for i in range(len(landmark_list_2)-1):
                            temp1=temp.index(landmark_list_2[i])
                            temp2=temp.index(landmark_list_2[i+1])
                            list4.append((temp1,temp2))
        
                            
                        mp_drawing.draw_landmarks(
                        image,
                        landmark_list=results.left_hand_landmarks,
                        connections=mp_holistic.HAND_CONNECTIONS,
                        landmark_drawing_spec=get_default_hand_landmarks_style(landmark2),
                        connection_drawing_spec=get_default_hand_connections_style(list3),
                        )
                        mp_drawing.draw_landmarks(
                        image,
                        landmark_list=results.right_hand_landmarks,
                        connections=mp_holistic.HAND_CONNECTIONS,
                        landmark_drawing_spec=get_default_hand_landmarks_style(landmark3),
                        connection_drawing_spec=get_default_hand_connections_style(list4),
                        )
                else:
                    landmark_list=[]
                    landmark_list_2=[]
    @staticmethod
    def draw_landmarks(image, results):
        mp_holistic = mp.solutions.holistic  # Holistic model
        mp_drawing = mp.solutions.drawing_utils  # Drawing utilities
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
        mp_drawing.draw_landmarks(
            image,
            landmark_list=results.right_hand_landmarks,
            connections=mp_holistic.HAND_CONNECTIONS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(
                color=(232, 254, 255), thickness=1, circle_radius=2
            ),
            connection_drawing_spec=mp_drawing.DrawingSpec(
                color=(255, 249, 161), thickness=2, circle_radius=2
            ),
        )

    
