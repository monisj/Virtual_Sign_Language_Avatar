from typing import List
import numpy as np
import mediapipe as mp
import csv
from pathlib import Path

class HandModel(object):
    """
    Params
        landmarks: List of positions
    Args
        connections: List of tuples containing the ids of the two landmarks representing a connection
        feature_vector: List of length 21 * 21 = 441 containing the angles between all connections
    """

    def __init__(self, landmarks: List[float],frame_index,which):

        # Define the connections
        self.connections = mp.solutions.holistic.HAND_CONNECTIONS
        
        self.frame_index=frame_index
        self.decide=which

        # Points Name
        self.points_name= ["Wrist","Thumb_CMC","Thumb_MCP","Thumb_IP","Thumb_Tip",
        "Index_Finger_MPC","Index_Finger_PIP","Index_Finger_DIP","Index_Finger_TIP",
        "Middle_Finger_MCP","Middle_Finger_PIP","Middle_Finger_DIP","Middle_Finger_TIP",
        "Ring_Finger_MCP","Ring_Finger_PIP","Ring_Finger_DIP","Ring_Finger_TIP","Pinky_MCP",
        "Pinky_PIP","Pinky_DIP","Pinky_TIP"]

        # Create feature vector (list of the angles between all the connections)
        landmarks = np.array(landmarks).reshape((21, 3))
        
        self.feature_vector,self.feature_vector_2 = self._get_feature_vector(landmarks)

    def _get_feature_vector(self, landmarks: np.ndarray) -> List[float]:
        """
        Params
            landmarks: numpy array of shape (21, 3)
        Return
            List of length nb_connections * nb_connections containing
            all the angles between the connections
        """
        connections = self._get_connections_from_landmarks(landmarks)
        
        
        # Write the data of angles of vectors either in "angle_between_vectors_left.csv" or "angle_between_vectors_right.csv"
        angles_list = []
        list_2=[]
        for connection_from,vector1 in zip(connections,self.connections):
            for connection_to,vector2 in zip(connections,self.connections):
                angle = self._get_angle_between_vectors(connection_from, connection_to)
                # If the angle is not NaN we store it else we store 0
                if angle == angle:
                    angles_list.append(angle)
                    list_2.append([self.frame_index,self.points_name[vector1[0]],self.points_name[vector1[1]],self.points_name[vector2[0]],self.points_name[vector2[1]],angle])
                else:
                    angles_list.append(0)
        return angles_list,list_2

    def _get_connections_from_landmarks(
        self, landmarks: np.ndarray
    ) -> List[np.ndarray]:
        """
        Params
            landmarks: numpy array of shape (21, 3)
        Return
            List of vectors representing hand connections
        """
        return list(
            map(
                lambda t: landmarks[t[1]] - landmarks[t[0]],
                self.connections,
            )
        )

    @staticmethod
    def _get_angle_between_vectors(u: np.ndarray, v: np.ndarray) -> float:
        """
        Args
            u, v: 3D vectors representing two connections
        Return
            Angle between the two vectors
        """
        if np.array_equal(u, v):
            return 0
        dot_product = np.dot(u, v)
        norm = np.linalg.norm(u) * np.linalg.norm(v)
        return np.arccos(dot_product / norm)
