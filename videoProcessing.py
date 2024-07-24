import cv2 as cv
import os
from singleFrameComplete import process_frame
import pickle

def process_video(video_path, output_path='output.avi'):
    cap = cv.VideoCapture(video_path)
    processed_frames = []
    length = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    processed = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        processed += 1
        processed_frames.append(process_frame(frame))
        print(f"Processed {processed}/{length} frames processed")


    with open('list.pkl', 'wb') as file:
     pickle.dump(processed_frames, file)

    video = cv.VideoWriter('output.avi', 0, 1, (processed_frames[0].shape[1],processed_frames[0].shape[0]))

    for img in processed_frames:
        video.write(img)

    # Release resources
    cv.destroyAllWindows()
    video.release()
    cap.release()


