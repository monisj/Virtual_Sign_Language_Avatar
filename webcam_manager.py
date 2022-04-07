from asyncio.windows_events import INFINITE
import cv2
import numpy as np
import mediapipe as mp


WHITE_COLOR = (245, 242, 226)
RED_COLOR = (25, 35, 240)

HEIGHT = 600


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

    def update(
        self, frame: np.ndarray, results, sign_detected, is_recording,sign,dist,val,sentences_pass_on
    ):
        self.sign_detected = sign_detected
        self.sign=sign
        self.dist=dist
        self.val=val
        self.sentences_pass_on=sentences_pass_on
        # Draw landmarks
        self.draw_landmarks(frame, results)

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

        # Update the frame
        cv2.circle(frame, (30, 30), 20, color, -1)
        #cv2.imshow("OpenCV Feed", frame)
        return frame,acc

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
                                acc1=((acc1-500)/500)*100
                                acc2=((acc2-500)/500)*100
                                if int(list1[0])<500 or int(list1[1])<500:
                                    self.sign_detected='Predicted correctly With Accuracy =95'
                                    acc2=95
                                    break
                                else:
                                    if acc1>100 or acc2>100:
                                        acc=((acc1+acc2)/2)//100
                                        self.sign_detected=f'Predicted correctly With Accuracy ={acc}'
                                        acc2=acc
                                        break
                                    else:
                                        acc=(acc1+acc2)/2
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
                                acc1=((acc1-500)/500)*100
                                acc2=((acc2-500)/500)*100
                                if int(list1[0])<500 or int(list1[1])<500:
                                    self.sign_detected='Predicted Incorrectly With Accuracy =95'
                                    acc2=95
                                    break
                                else:
                                    if acc1>100 or acc2>100:
                                        acc=((acc1+acc2)/2)//100
                                        self.sign_detected=f'Predicted Incorrectly With Accuracy ={acc}'
                                        acc2=acc
                                        break
                                    else:
                                        acc=(acc1+acc2)//2
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
    def draw_landmarks(image, results):
        mp_holistic = mp.solutions.holistic  # Holistic model
        mp_drawing = mp.solutions.drawing_utils  # Drawing utilities

        # Draw left hand connections
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
