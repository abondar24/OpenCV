import cv2
from managers import WindowManager, CaptureManager
from trackers import FaceTracker

class Detect(object):

    def __init__(self):
        self._window_manager = WindowManager('Face Detector', self.on_key_press)
        self._capture_manager = CaptureManager(cv2.VideoCapture(0), self._window_manager, True)
        self._face_tracker = FaceTracker()

    def run(self):
        self._window_manager.create_window()
        while self._window_manager.is_window_created:

            self._capture_manager.enter_frame()
            frame = self._capture_manager.frame

            self._face_tracker.update(frame)
            self._face_tracker.draw_debug_rects(frame)

            self._capture_manager.exit_frame()
            self._window_manager.process_events()

    def on_key_press(self, keycode):

        """
        Keypress handler

        escape - quit
        :return:
        """

        if keycode == 27: # escape
            self._window_manager.destroy_window()


if __name__=="__main__":
    Detect().run()
