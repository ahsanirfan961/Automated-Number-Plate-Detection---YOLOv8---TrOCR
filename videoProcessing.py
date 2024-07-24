import cv2 as cv
import os
from singleFrameComplete import process_frame

def process_video(video_path, output_path):
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


    frame_height, frame_width = processed_frames[0].shape[:2]

    video = cv.VideoWriter(output_path, cv.VideoWriter_fourcc(*'XVID'), 20, (frame_width, frame_height))

    for img in processed_frames:
        video.write(img)

    # Release resources
    cv.destroyAllWindows()
    video.release()
    cap.release()


