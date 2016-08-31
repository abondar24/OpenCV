import cv2

# for non camera replace 0 with file_name and read fps from video using videoCapture.get(cv2.cv.CV_CAP_PROP_FPS)
video_capture = cv2.VideoCapture(0)
fps = 30
size = (int(video_capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),
        int(video_capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))


video_writer = cv2.VideoWriter('output.avi', cv2.cv.CV_FOURCC('I', '4', '2', '0'), fps, size)
success, frame = video_capture.read()
num_frames_remaining = 10 * fps - 1
print success
while success and num_frames_remaining > 0:
    video_writer.write(frame)
    success, frame = video_capture.read()
    num_frames_remaining -= 1
