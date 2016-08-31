import cv2

clicked = False

def onMouse(event, x, y, flags, param):
    global clicked
    if event == cv2.cv.CV_EVENT_LBUTTONUP:
        clicked = True


video_capture = cv2.VideoCapture(0)
cv2.namedWindow('Video Window')
cv2.setMouseCallback('Video Window', onMouse)

success, frame = video_capture.read()

# waitKey - number of ms to wait for keyboard key
while success and cv2.waitKey(1) == -1 and not clicked:
    cv2.imshow('Video Window', frame)
    success,frame = video_capture.read()

cv2.destroyWindow('Video Window')
