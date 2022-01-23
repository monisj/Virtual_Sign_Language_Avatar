import pandas as pd
from fastdtw import fastdtw
import numpy as np
from models.sign_model import SignModel
from scipy.spatial.distance import euclidean
import pathlib
def dtw_distances(recorded_sign: SignModel, reference_signs: pd.DataFrame,rec_acc):
    """
    Use DTW to compute similarity between the recorded sign & the reference signs

    :param recorded_sign: a SignModel object containing the data gathered during record
    :param reference_signs: pd.DataFrame
                            columns : name, dtype: str
                                      sign_model, dtype: SignModel
                                      distance, dtype: float64
    :return: Return a sign dictionary sorted by the distances from the recorded sign
    """
    path_video=data_path=str(pathlib.Path.cwd())+'\\'+'utils'+'\\'+'Base_G_Acc'
    if rec_acc == False:
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

            
            #print("Right_Hand ={}".format(row))

                if recorded_sign.has_left_hand:
                    f=open(f'{path_video}\{ref_sign_name}.txt',"r")
                    f=f.read()
                    row["distance"] += list(fastdtw(rec_left_hand, ref_left_hand))[0]
                    acc=((int(row["distance"])-int(f))/int(f))*100
                    if acc>100:
                        print("Accuracy of {} = {}".format(ref_sign_name,acc/100))
                    else:
                        print("Accuracy of {} = {}".format(ref_sign_name,acc))
                if recorded_sign.has_right_hand:
                    f=open(f'{path_video}\{ref_sign_name}.txt',"r")
                    f=f.read()
                    row["distance"] += list(fastdtw(rec_right_hand, ref_right_hand))[0]
                    acc1=((int(row["distance"])-int(f))/int(f))*100
        
                    if acc1>100:
                        print("Accuracy of {} = {}".format(ref_sign_name,acc1/100))
                    else:
                        print("Accuracy of {} = {}".format(ref_sign_name,acc1))

        # If not, distance equals infinity
            else:
                print("Accuracy of {} = {}".format(ref_sign_name,"Not in Range"))
                row["distance"] = np.inf
        return reference_signs.sort_values(by=["distance"])
    elif rec_acc == True:
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

            
            #print("Right_Hand ={}".format(row))

                if recorded_sign.has_left_hand:
                    f=open(f'{path_video}\{ref_sign_name}.txt',"w")
                    row["distance"] += list(fastdtw(rec_left_hand, ref_left_hand))[0]
                    acc=list(fastdtw(rec_left_hand, ref_left_hand,dist=euclidean))
                    f.write(row["Distance"])
                    f.close()
                if recorded_sign.has_right_hand:
                    f=open(f'{path_video}\{ref_sign_name}.txt',"w")
                    row["distance"] += list(fastdtw(rec_right_hand, ref_right_hand))[0]
                    acc1=list(fastdtw(rec_right_hand, ref_right_hand,dist=euclidean))
                    f.write(row["Distance"])
                    f.close()

        # If not, distance equals infinity
            else:
                print("Accuracy of {} = {}".format(ref_sign_name,"Not in Range"))
                row["distance"] = np.inf
        return reference_signs.sort_values(by=["distance"])
