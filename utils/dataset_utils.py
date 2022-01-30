import os
import time

import pandas as pd
import pickle as pkl
from tqdm import tqdm

from models.sign_model import SignModel
from utils.landmark_utils import save_landmarks_from_video, load_array

def load_dataset():
    dataset = [
        file_name.replace(".pickle", "").replace("lh_", "")
        for root, dirs, files in os.walk(os.path.join("data", "dataset"))
        for file_name in files
        if file_name.endswith(".pickle") and file_name.startswith("lh_")
    ]
    return dataset
    
#load_dataset()

def new_videos_load_dataset():
    videos = [
        file_name.replace(".mp4", "")
        for root, dirs, files in os.walk(os.path.join("data", "videos"))
        for file_name in files
        if file_name.endswith(".mp4")
    ]
    dataset = [
        file_name.replace(".pickle", "").replace("lh_", "")
        for root, dirs, files in os.walk(os.path.join("data", "dataset"))
        for file_name in files
        if file_name.endswith(".pickle") and file_name.startswith("lh_")
    ]

    # Create the dataset from the reference videos
    videos_not_in_dataset = list(set(videos).difference(set(dataset)))
    n = len(videos_not_in_dataset)
    if n > 0:
        print(f"\nExtracting landmarks from new videos: {n} videos detected\n")

        for idx in tqdm(range(n)):
            save_landmarks_from_video(videos_not_in_dataset[idx])

    return videos

def save_embeds(arr, path):
    file = open(path, "wb")
    pkl.dump(arr, file)
    file.close()


def load_embeds(path):
    file = open(path, "rb")
    embed = pkl.load(file)
    file.close()
    return embed

def load_reference_signs(videos):
    print('loading references')
    reference_signs = pd.DataFrame(columns=["name", "sign_model", "distance"])
    #tstart=time.time()
    for video_name in videos:
        #vstart=time.time()
        sign_name = video_name.split("_")[0]
        path = os.path.join("data", "dataset", sign_name, video_name)
        # lstart=time.time()
        left_hand_list = load_array(os.path.join(path, f"lh_{video_name}.pickle"))
        # lend=time.time()
        # print(f'{video_name} left time=',(lend-lstart))
        # rstart=time.time()
        right_hand_list = load_array(os.path.join(path, f"rh_{video_name}.pickle"))
        # rend=time.time()
        # print(f'{video_name} left time=',(rend-rstart))

        reference_signs = reference_signs.append(
            {
                "name": sign_name,
                "sign_model": SignModel(left_hand_list, right_hand_list),
                "distance": 0,
            },
            ignore_index=True,
        )
        # vend=time.time()
    #     print(f'{video_name} time=',(vend-vstart))
    # tend=time.time()
    # print('total time=',(tend-tstart))
    print(
        f'Dictionary count: {reference_signs[["name", "sign_model"]].groupby(["name"]).count()}'
    )
    return reference_signs

def new_load_reference_signs(videos):
    print('loading references')
    reference_signs = pd.DataFrame(columns=["name", "sign_model", "distance"])
    #tstart=time.time()
    for video_name in videos:
        #vstart=time.time()
        sign_name = video_name.split("_")[0]
        path = os.path.join("data", "dataset", sign_name, video_name)
        #data_path = os.path.join(path, video_name)

        # lstart=time.time()
        left_hand_list = load_array(os.path.join(path, f"lh_{video_name}.pickle"))
        # lend=time.time()
        # print(f'{video_name} left time=',(lend-lstart))
        # rstart=time.time()
        right_hand_list = load_array(os.path.join(path, f"rh_{video_name}.pickle"))
        # rend=time.time()
        # print(f'{video_name} left time=',(rend-rstart))
        if not os.path.exists(os.path.join(path, f"embeddings_{video_name}.pickle")):
            embeddings=SignModel(left_hand_list, right_hand_list)
            save_embeds(embeddings,os.path.join(path, f"embeddings_{video_name}.pickle"))
        else :
            embeddings=load_embeds(os.path.join(path, f"embeddings_{video_name}.pickle"))

        reference_signs = reference_signs.append(
            {
                "name": sign_name,
                "sign_model": embeddings,
                "distance": 0,
            },
            ignore_index=True,
        )
        # vend=time.time()
    #     print(f'{video_name} time=',(vend-vstart))
    # tend=time.time()
    # print('total time=',(tend-tstart))
    print(
        f'Dictionary count: {reference_signs[["name", "sign_model"]].groupby(["name"]).count()}'
    )
    return reference_signs


