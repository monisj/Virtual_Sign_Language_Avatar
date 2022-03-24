import pandas as pd
from fastdtw import fastdtw
import numpy as np
from models.sign_model import SignModel
from scipy.spatial.distance import euclidean
from dtaidistance import dtw, dtw_ndim



def dtw_distances(recorded_sign: SignModel, reference_signs: pd.DataFrame):
    """
    Use DTW to compute similarity between the recorded sign & the reference signs

    :param recorded_sign: a SignModel object containing the data gathered during record
    :param reference_signs: pd.DataFrame
                            columns : name, dtype: str
                                      sign_model, dtype: SignModel
                                      distance, dtype: float64
    :return: Return a sign dictionary sorted by the distances from the recorded sign
    """
    # Embeddings of the recorded sign
    rec_left_hand = recorded_sign.lh_embedding
    rec_right_hand = recorded_sign.rh_embedding

    for idx, row in reference_signs.iterrows():
        # Initialize the row variables
        ref_sign_name, ref_sign_model, _ = row

        # If the reference sign has the same number of hands compute fastdtw
        if (recorded_sign.has_left_hand == ref_sign_model.has_left_hand) and (
            recorded_sign.has_right_hand == ref_sign_model.has_right_hand
        ):
            ref_left_hand = ref_sign_model.lh_embedding
            ref_right_hand = ref_sign_model.rh_embedding

            if recorded_sign.has_left_hand:
                row["distance"] += list(fastdtw(rec_left_hand, ref_left_hand,dist=euclidean))[0]
            elif recorded_sign.has_right_hand:
                row["distance"] += list(fastdtw(rec_right_hand, ref_right_hand,dist=euclidean))[0]

            elif recorded_sign.has_left_hand and recorded_sign.has_right_hand:
                row["distance"] += list(fastdtw(rec_left_hand, ref_left_hand,dist=euclidean))[0]
                row["distance"] += list(fastdtw(rec_right_hand, ref_right_hand,dist=euclidean))[0]
                
        # If not, distance equals infinity
        else:
            row["distance"] = np.inf
    return reference_signs.sort_values(by=["distance"])

def fdtw_distances(recorded_sign: SignModel, reference_signs: pd.DataFrame):
    """
    Use DTW to compute similarity between the recorded sign & the reference signs

    :param recorded_sign: a SignModel object containing the data gathered during record
    :param reference_signs: pd.DataFrame
                            columns : name, dtype: str
                                      sign_model, dtype: SignModel
                                      distance, dtype: float64
    :return: Return a sign dictionary sorted by the distances from the recorded sign
    """
    # Embeddings of the recorded sign
    # rec_left_hand = recorded_sign.lh_embedding
    # rec_right_hand = recorded_sign.rh_embedding
    # print(len(recorded_sign.lh_embedding))
    # print(len(recorded_sign.rh_embedding))
    rec_left_hand = np.array(recorded_sign.lh_embedding,dtype=np.double)
    rec_right_hand = np.array(recorded_sign.rh_embedding,dtype=np.double)

    for idx, row in reference_signs.iterrows():
        # Initialize the row variables
        ref_sign_name, ref_sign_model, _ = row

        # If the reference sign has the same number of hands compute fastdtw
        if (recorded_sign.has_left_hand == ref_sign_model.has_left_hand) and (
            recorded_sign.has_right_hand == ref_sign_model.has_right_hand
        ):
            ref_left_hand = np.array(ref_sign_model.lh_embedding,dtype=np.double)
            ref_right_hand = np.array(ref_sign_model.rh_embedding,dtype=np.double)

            if recorded_sign.has_left_hand:
                row["distance"] += dtw_ndim.distance_fast(rec_left_hand, ref_left_hand)
            elif recorded_sign.has_right_hand:
                row["distance"] += dtw_ndim.distance_fast(rec_right_hand, ref_right_hand)
            elif recorded_sign.has_left_hand and recorded_sign.has_right_hand:
                row["distance"] += dtw_ndim.distance_fast(rec_left_hand, ref_left_hand)
                row["distance"] += dtw_ndim.distance_fast(rec_right_hand, ref_right_hand)

        # If not, distance equals infinity
        else:
            row["distance"] = np.inf
    return reference_signs.sort_values(by=["distance"])
