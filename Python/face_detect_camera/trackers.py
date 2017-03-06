import cv2


class FaceTracker(object):
    """A tracker for facial features: face,eyes,nose,mouth"""

    def __init__(self, scale_factor=1.2, min_neighbors=2, flags=cv2.cv.CV_HAAR_SCALE_IMAGE):
        self.scale_factor = scale_factor
        self.min_neighbors = min_neighbors
        self.flags = flags

        self.face_rects = []
        self._face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
        self._eye_classifier = cv2.CascadeClassifier('haarcascade_eye.xml')
        self._nose_classifier = cv2.CascadeClassifier('haarcascade_mcs_nose.xml')
        self._mouth_classifier = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')

    def update(self, image):
        """Update the tracked facial features"""

        self.face_rects = []

        if is_gray(image):
            image = cv2.equalizeHist(image)

        else:
            image = cv2.cvtColor(image, cv2.cv.CV_BGR2GRAY)
            cv2.equalizeHist(image, image)

        min_size = width_height_divided_by(image, 8)
        face_rects = self._face_classifier.detectMultiScale(image,
                                                            self.scale_factor,
                                                            self.min_neighbors,
                                                            self.flags,
                                                            min_size)
        self.face_rects = face_rects

    def draw_debug_rects(self, image):
        """Draw rectangles around the tracked facial features"""

        if is_gray(image):
            face_color = 255

        else:
            face_color = (255, 255, 255)  # white

        for face in self.face_rects:
            outline_rect(image, face, face_color)


def outline_rect(image, rect, color):
    if rect is None:
        return

    x, y, w, h = rect
    cv2.rectangle(image, (x, y), (x+w, y+h), color)


def is_gray(image):
    """Return true if the image has one channel per pixel"""
    return image.ndim < 3


def width_height_divided_by(image, divisor):
    """Return an images dimensions, divided by a value"""
    h, w = image.shape[:2]
    return w / divisor, h / divisor