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




def fdtw_distances(recorded_sign: SignModel, reference_signs: pd.DataFrame,acc_sign):
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
    b=0
    out_left=[] #Holds data for error of left hand sign
    out_right=[] #Holds data for error of right hand sign
    list1=[] #This Holds Embeddings of ref signs of right hand
    list2=[] #This Holds Embeddings of rec signs of right hand or left hand if individual hand gesture are performed
    list3=[] #This Temporarily Stores the data for List2
    list6=[] #This Holds Embeddings of ref signs of left hand
    list7=[] #This Holds Data of Rec signs of left Hand
    list8=[] #This Holds Data of Rec signs of Right
    list9=[] # This Temporaily Stores data for List 7

    
    for idx, row in reference_signs.iterrows():
        # Initialize the row variables
        ref_sign_name, ref_sign_model, _ = row

        # If the reference sign has the same number of hands compute fastdtw
        if (recorded_sign.has_left_hand == ref_sign_model.has_left_hand) and (
            recorded_sign.has_right_hand == ref_sign_model.has_right_hand
        ):
            ref_left_hand = np.array(ref_sign_model.lh_embedding,dtype=np.double)
            ref_right_hand = np.array(ref_sign_model.rh_embedding,dtype=np.double)
            if ref_sign_name==acc_sign:
                for i in ref_sign_model.rh_embedding:
                        list1.append(i)
            if ref_sign_name==acc_sign:
                for i in ref_sign_model.lh_embedding:
                        list6.append(i)    
               

                
            if recorded_sign.has_left_hand:
                row["distance"] += dtw_ndim.distance_fast(rec_left_hand, ref_left_hand)
                if ref_sign_name==acc_sign:
                    list4=[]
                    for i in recorded_sign.lh_embedding_2:
                        for j in i:
                            sequence=j[0]
                            vector1=(j[1]+','+j[2])
                            vector2=(j[3]+','+j[4])
                            angle=j[5]
                            list3.append([vector1,vector2,sequence])
                            if int(sequence)==b:
                                list4.append(angle)
                            else:
                                b=int(sequence)
                                list2.append(list4)
                                list4=[]
                    list5=[]
                    for i in range(len(list2)):
                        temp=len(list2[i])
                        temp3=list2[i]
                        temp4=list6[i]
                        for j in range(temp):
                            temp5=[temp3[j]]
                            temp6=[temp4[j]]
                            ab = np.array(temp5,dtype=np.double)
                            bc = np.array(temp6,dtype=np.double)
                            temp1=np.expand_dims(ab,axis=1)
                            temp2=np.expand_dims(bc,axis=1)
                            cd= dtw_ndim.distance_fast(temp1,temp2)
                            list5.append(cd)
                    c=''
                    for i in range(len(list5)):
                        temp_val=list5[i]
                        temp_val=float(temp_val)
                        if float(temp_val)<=2:
                            pass
                        elif int(temp_val)==0:
                            pass
                        else:
                            temp3=list3[i]
                            if c==temp3[0]:
                                pass
                            else:
                                c=temp3[0]
                                out_left.append(f"The Hand Position of {temp3[0]} At Sequence ={temp3[2]} Have Problem")
                    out_right=[]
                else:
                    pass
            elif recorded_sign.has_right_hand:
                row["distance"] += dtw_ndim.distance_fast(rec_right_hand, ref_right_hand)
                if ref_sign_name==acc_sign:
                    list4=[]
                    for i in recorded_sign.rh_embedding_2:
                        for j in i:
                            sequence=j[0]
                            vector1=(j[1]+','+j[2])
                            vector2=(j[3]+','+j[4])
                            angle=j[5]
                            list3.append([vector1,vector2,sequence])
                            if int(sequence)==b:
                                list4.append(angle)
                            else:
                                b=int(sequence)
                                list2.append(list4)
                                list4=[]
                    list5=[]
                    for i in range(len(list2)):
                        temp=len(list2[i])
                        temp3=list2[i]
                        temp4=list1[i]
                        for j in range(temp):
                            temp5=[temp3[j]]
                            temp6=[temp4[j]]
                            ab = np.array(temp5,dtype=np.double)
                            bc = np.array(temp6,dtype=np.double)
                            temp1=np.expand_dims(ab,axis=1)
                            temp2=np.expand_dims(bc,axis=1)
                            cd= dtw_ndim.distance_fast(temp1,temp2)
                            list5.append(cd)
                    c=[]
                    for i in range(len(list5)):
                        temp_val=list5[i]
                        temp_val=float(temp_val)
                        if float(temp_val)<=2:
                            pass
                        elif int(temp_val)==0:
                            pass
                        else:
                            temp3=list3[i]
                            if temp3[0]+str(temp3[2]) in c:
                                pass 
                            else:
                                c.append(temp3[0]+str(temp3[2]))
                                out_right.append(f"The Hand Position of {temp3[0]} At Sequence ={temp3[2]} Have Problem")
                    out_left=[]        
                else:
                    pass    
            elif recorded_sign.has_left_hand and recorded_sign.has_right_hand:
                row["distance"] += dtw_ndim.distance_fast(rec_left_hand, ref_left_hand)
                row["distance"] += dtw_ndim.distance_fast(rec_right_hand, ref_right_hand)
                if ref_sign_name==acc_sign:
                    #Left Hand
                    list_4=[]
                    for i in recorded_sign.lh_embedding_2:
                        for j in i:
                            sequence=j[0]
                            vector1=(j[1]+','+j[2])
                            vector2=(j[3]+','+j[4])
                            angle=j[5]
                            list9.append([vector1,vector2,sequence])
                            if int(sequence)==b:
                                list_4.append(angle)
                            else:
                                b=int(sequence)
                                list7.append(list4)
                                list_4=[]
                    list_5=[]
                    for i in range(len(list7)):
                        temp=len(list7[i])
                        temp3=list7[i]
                        temp4=list6[i]
                        for j in range(temp):
                            temp5=[temp3[j]]
                            temp6=[temp4[j]]
                            ab = np.array(temp5,dtype=np.double)
                            bc = np.array(temp6,dtype=np.double)
                            temp1=np.expand_dims(ab,axis=1)
                            temp2=np.expand_dims(bc,axis=1)
                            cd= dtw_ndim.distance_fast(temp1,temp2)
                            list_5.append(cd)
                    cd=''
                    for i in range(len(list_5)):
                        temp_val=list5[i]
                        temp_val=float(temp_val)
                        if float(temp_val)<=2:
                            pass
                        elif int(temp_val)==0:
                            pass
                        else:
                            temp3=list9[i]
                            if cd==temp3[0]:
                                pass
                            else:
                                cd=temp3[0]
                                out_left.append(f"The Hand Position of {temp3[0]} At Sequence ={temp3[2]} Have Problem")




                    #Right Hand
                    list4=[]
                    for i in recorded_sign.rh_embedding_2:
                        for j in i:
                            sequence=j[0]
                            vector1=(j[1]+','+j[2])
                            vector2=(j[3]+','+j[4])
                            angle=j[5]
                            list3.append([vector1,vector2,sequence])
                            if int(sequence)==b:
                                list4.append(angle)
                            else:
                                b=int(sequence)
                                list8.append(list4)
                                list4=[]
                    list5=[]
                    for i in range(len(list8)):
                        temp=len(list8[i])
                        temp3=list8[i]
                        temp4=list1[i]
                        for j in range(temp):
                            temp5=[temp3[j]]
                            temp6=[temp4[j]]
                            ab = np.array(temp5,dtype=np.double)
                            bc = np.array(temp6,dtype=np.double)
                            temp1=np.expand_dims(ab,axis=1)
                            temp2=np.expand_dims(bc,axis=1)
                            cd= dtw_ndim.distance_fast(temp1,temp2)
                            list5.append(cd)
                    c=''
                    for i in range(len(list5)):
                        temp_val=list5[i]
                        temp_val=float(temp_val)
                        if float(temp_val)<=2:
                            pass
                        elif int(temp_val)==0:
                            pass
                        else:
                            temp3=list3[i]
                            if c==temp3[0]:
                                pass
                            else:
                                c=temp3[0]
                                out_right.append(f"The Hand Position of {temp3[0]} At Sequence ={temp3[2]} Have Problem")
                else:
                    pass
        # If not, distance equals infinity
        else:
            row["distance"] = np.inf
    
    
    return reference_signs.sort_values(by=["distance"]),out_left,out_right


