import cv2
import threading

def play_video():
    global video_list
    video_path = None
    audio_path = None
    ret = None
    frame = None
    while True:
        if len(video_list) > 0:
            video_path = video_list[0].get("video")
            audio_path = video_list[0].get("audio")
            cap = cv2.VideoCapture(video_path)  # Open video file
            video_list.pop(0)
        else:
            audio_path = None
            cap = None
            _, frame = cv2.VideoCapture("data/pretrained/train.mp4").read()

        if audio_path:
            threading.Thread(target=play_audio, args=[audio_path]).start()  # play audio
        # Loop through video frames
        while True:
            if cap:
                ret, frame = cap.read()
            if frame is not None:
                cv2.imwrite('Fay-2d.jpg', frame)
                # Wait for 38 milliseconds - Can be adjusted or removed as needed
                # cv2.waitKey(38)
            if not ret:
                break
            # Additional break condition to prevent an infinite loop
            if not cap.isOpened():
                break

        # Release the video capture object when done
        if cap:
            cap.release()
