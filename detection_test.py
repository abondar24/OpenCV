import cv2
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

scale_factor = 2.1
min_neighbors = 3
min_size = (30, 30)
flags = cv2.cv.CV_HAAR_SCALE_IMAGE


image = cv2.imread('hard.jpg')
faces = face_cascade.detectMultiScale(image, scaleFactor = scale_factor, minNeighbors = min_neighbors,
                                      minSize = min_size, flags = flags)



for( x, y, w, h ) in faces:
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 0), 2)
    cv2.imwrite('out.jpg', image)