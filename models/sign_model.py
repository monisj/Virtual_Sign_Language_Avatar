from typing import List

import numpy as np
import csv
from pathlib import Path

from models.hand_model import HandModel


class SignModel(object):
    def __init__(
        self, left_hand_list: List[List[float]], right_hand_list: List[List[float]]
    ):
        """
        Params
            x_hand_list: List of all landmarks for each frame of a video
        Args
            has_x_hand: bool; True if x hand is detected in the video, otherwise False
            xh_embedding: ndarray; Array of shape (n_frame, nb_connections * nb_connections)
        """
        self.has_left_hand = np.sum(left_hand_list) != 0
        self.has_right_hand = np.sum(right_hand_list) != 0

        self.lh_embedding,self.lh_embedding_2 = self._get_embedding_from_landmark_list(left_hand_list,int(0))
        self.rh_embedding,self.rh_embedding_2 = self._get_embedding_from_landmark_list(right_hand_list,int(1))

    @staticmethod
    def _get_embedding_from_landmark_list(
        hand_list: List[List[float]],
    which) -> List[List[float]]:
        """
        Params
            hand_list: List of all landmarks for each frame of a video
        Return
            Array of shape (n_frame, nb_connections * nb_connections) containing
            the feature_vectors of the hand for each frame
        """
        embedding = []
        emb=[]
        for frame_idx in range(len(hand_list)):
            if np.sum(hand_list[frame_idx]) == 0:
                continue

            hand_gesture = HandModel(hand_list[frame_idx],frame_idx,which)
            embedding.append(hand_gesture.feature_vector)
            emb.append(hand_gesture.feature_vector_2)
        return embedding,emb
