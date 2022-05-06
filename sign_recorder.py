import pandas as pd
import numpy as np
from collections import Counter

from utils.dtw import dtw_distances,fdtw_distances
from models.sign_model import SignModel
from utils.landmark_utils import extract_landmarks


class SignRecorder(object):
    def __init__(self, reference_signs: pd.DataFrame, acc_sign,seq_len=False):
        # Variables for recording
        self.is_recording = False
        self.seq_len = seq_len
        self.temp=False
        self.num_temp=0
        self.acc_sign=acc_sign
        self.out_left=[]
        self.out_right=[]
        # List of results stored each frame
        self.recorded_results = []

        # DataFrame storing the distances between the recorded sign & all the reference signs from the dataset
        self.reference_signs = reference_signs

    def record(self,record):
        """
        Initialize sign_distances & start recording
        """
        if not record:
            self.seq_len=False
            #self.seq_len=False
        else:
            self.reference_signs["distance"].values[:] = 0
            self.is_recording = True
            if record:
                self.seq_len=True
            else:
                self.seq_len=False
    def process_results(self, results):
        """
        If the SignRecorder is in the recording state:
            it stores the landmarks during seq_len frames and then computes the sign distances
        :param results: mediapipe output
        :return: Return the word predicted (blank text if there is no distances)
                & the recording state
        """
        
        
        if self.is_recording:
            if self.seq_len:
                self.recorded_results.append(results)
                self.temp=True
            else:
                if self.num_temp<5 and self.temp==True:
                    self.num_temp+=1
                    self.recorded_results.append(results)
                else:
                    self.num_temp=0 #For Safe Measures 
                    self.temp=False
                    self.compute_distances()
                    #print(self.reference_signs) #Uncomment to reveal distances

        if np.sum(self.reference_signs["distance"].values) == 0:
            return "", self.is_recording,[" "],[" "],self.out_left,self.out_right
        sign=self.reference_signs.iloc[::]["name"].values
        dist=self.reference_signs.iloc[::]["distance"].values
        return self._get_sign_predicted(), self.is_recording,sign,dist,self.out_left,self.out_right

    def compute_distances(self):
        """
        Updates the distance column of the reference_signs
        and resets recording variables
        """
        left_hand_list, right_hand_list = [], []
        for results in self.recorded_results:
            left_hand, right_hand = extract_landmarks(results)
            left_hand_list.append(left_hand)
            right_hand_list.append(right_hand)

        # Create a SignModel object with the landmarks gathered during recording
        recorded_sign = SignModel(left_hand_list, right_hand_list)

        # Compute sign similarity with DTW (ascending order)
        #self.reference_signs = dtw_distances(recorded_sign, self.reference_signs) #Old Algorithm
        self.reference_signs,self.out_left,self.out_right = fdtw_distances(recorded_sign, self.reference_signs,self.acc_sign)

        # Reset variables
        self.recorded_results = []
        self.is_recording = False

    def _get_sign_predicted(self, batch_size=5, threshold=0.3):
        """
        Method that outputs the sign that appears the most in the list of closest
        reference signs, only if its proportion within the batch is greater than the threshold

        :param batch_size: Size of the batch of reference signs that will be compared to the recorded sign
        :param threshold: If the proportion of the most represented sign in the batch is greater than threshold,
                        we output the sign_name
                          If not,
                        we output "Sign not found"
        :return: The name of the predicted sign
        """
        # Get the list (of size batch_size) of the most similar reference signs
        sign_names = self.reference_signs.iloc[:batch_size]["name"].values

        # Count the occurrences of each sign and sort them by descending order
        sign_counter = Counter(sign_names).most_common()

        predicted_sign, count = sign_counter[0]
        #if count / batch_size < threshold:
            #return "Invalid Sign"
        return predicted_sign
