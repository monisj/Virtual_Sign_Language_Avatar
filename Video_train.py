def train():
    # Set mediapipe model 
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    
    # NEW LOOP
    # Loop through actions
    for action in actions:
        if pathlib.Path(DATA_PATH).joinpath(action).is_dir():
            print(action)
            continue
        cap = cv2.VideoCapture(f'{action}.mp4')
        # Loop through sequences aka videos
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps    = cap.get(cv2.CAP_PROP_FPS)
        start=round(fps*1.5)
        end=round(length-fps*2)
        mid=(start+end)//2
        end=mid-fps
        cap.set(cv2.CAP_PROP_POS_FRAMES, start)
        loop=1
        frame_counter = start
        flip=False
        while loop <= no_sequences:
            # Loop through video length aka sequence length
            next=False
            f=0
            while next is not True:

                # Read feed
                ret, frame = cap.read()
                if flip:
                    frame=cv2.flip(frame,1)
                frame_counter+=1
                f+=1
                #print(frame_counter)
                if frame_counter == end:
                    #print(loop,end)
                    #print(loop//2)
                    if flip is False:
                        flip=True
                    else:
                        flip=False
                        if loop%2 == 0 and loop >= 2:
                            start=round(fps*1.5)
                            end=mid-fps
                        else:
                            start=mid+fps
                            end=round(length-fps*2)
                        loop+=1
                    next=True
                    frame_counter = start
                    cap.set(cv2.CAP_PROP_POS_FRAMES, start)
                    continue

                # Make detections
                image, results = mediapipe_detection(frame, holistic)

                # Draw landmarks
                draw_styled_landmarks(image, results)
                
                
                cv2.imshow('OpenCV Feed', image)
                # NEW Export keypoints
                keypoints = extract_keypoints(results)
                pathlib.Path(data_path).joinpath(action,str(loop)).mkdir(parents=True, exist_ok=True)
                npy_path = pathlib.Path(data_path).joinpath(action,str(loop),str(f))
                np.save(npy_path, keypoints)

                # Break gracefully
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
                    
    cap.release()
    cv2.destroyAllWindows()
