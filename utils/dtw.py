import pandas as pd
from fastdtw import fastdtw
import numpy as np
from models.sign_model import SignModel
import pathlib
from scipy.spatial.distance import euclidean

def dtw_distances(recorded_sign: SignModel, reference_signs: pd.DataFrame):
    
    # Embeddings of the recorded sign
    rec_left_hand = recorded_sign.lh_embedding
    rec_right_hand = recorded_sign.rh_embedding
    data_path=pathlib.Path.cwd().joinpath('utils\Acc')
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
                #print("matrix=",ref_left_hand)
                acc=((int(row["distance"])-500)/500)*100
                if acc>100:
                    f=open(f'{data_path}\{ref_sign_name}.txt','w')
                    print("Accuracy of {} = {}".format(ref_sign_name,acc//100))
                    a=str(acc//100)
                    f.write(a)
                    f.close()
                else:
                    if int(row["distance"])<500:
                        f=open(f'{data_path}\{ref_sign_name}.txt','w')
                        print("Accuracy of {} = {}".format(ref_sign_name,95))
                        a=str(95)
                        f.write(a)
                        f.close()
                    else:
                        f=open(f'{data_path}\{ref_sign_name}.txt','w')
                        print("Accuracy of {} = {}".format(ref_sign_name,100-acc))
                        a=str(100-acc)
                        f.write(a)
                        f.close()
            if recorded_sign.has_right_hand:
                row["distance"] += list(fastdtw(rec_right_hand, ref_right_hand,dist=euclidean))[0]
                #print("matrix=",ref_right_hand)
                han=list(fastdtw(rec_right_hand, ref_right_hand))[0]
                acc1=((int(row["distance"])-500)/500)*100
        
                if acc1>100:
                    f=open(f'{data_path}\{ref_sign_name}.txt','w')
                    print("Accuracy of {} = {}".format(ref_sign_name,acc1//100))
                    a=str(acc1//100)
                    f.write(a)
                    f.close()
                else:
                    if int(row["distance"])<500:
                        f=open(f'{data_path}\{ref_sign_name}.txt','w')
                        print("Accuracy of {} = {}".format(ref_sign_name,95))
                        a=str(95)
                        f.write(a)
                        f.close()
                    else:
                        f=open(f'{data_path}\{ref_sign_name}.txt','w')
                        print("Accuracy of {} = {}".format(ref_sign_name,100-acc1))
                        a=str(100-acc1)
                        f.write(a)
                        f.close()
        # If not, distance equals infinity
        else:
            print("Accuracy of {} = {}".format(ref_sign_name,"Not in Range"))
            row["distance"] = np.inf
            f=open(f'{data_path}\{ref_sign_name}.txt','w')
            a=str(0)
            f.write(a)
            f.close()
    return reference_signs.sort_values(by=["distance"])
