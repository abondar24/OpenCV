import cv2
import numpy as np
import time


class CaptureManager(object):
    def __init__(self, capture, preview_window_manager=None, should_mirror_preview = False):

        self.preview_window_manager = preview_window_manager
        self.should_mirror_preview = should_mirror_preview

        self._capture = capture
        self._channel = 0
        self._entered_frame = False
        self._frame = None
        self._frames_elapsed = long(0)
        self._fps_est = None

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self):
        return self._channel

    @property
    def frame(self):
        if self._entered_frame and self._frame is None:
            _, self._frame = self._capture.retrieve(channel=self.channel)
        return self._frame

    def enter_frame(self):
        # capture the next frame

        assert not self._entered_frame, 'previous enter_frame() had no matching exit_frame()'
        if self._capture is not None:
            self._entered_frame = self._capture.grab()

    def exit_frame(self):
        # draw to window, write to files, release the frame

        # frame is retrievable or not
        if self.frame is None:
            self._entered_frame = False
            return

        if self._frames_elapsed == 0:
            self._start_time = time.time()
        else:
            time_elapsed = time.time() - self._start_time
            self._fps_est = self._frames_elapsed / time_elapsed
        self._frames_elapsed += 1

        # draw
        if self.preview_window_manager is not None:
            if self.should_mirror_preview:
                mirrored_frame = np.fliplr(self._frame).copy()
                self.preview_window_manager.show(mirrored_frame)
            else:
                self.preview_window_manager.show(self._frame)

        # release the frame
        self._frame = None
        self._entered_frame = False



class WindowManager(object):

    def __init__(self, window_name, keypress_callback = None):
        self.keypress_callback = keypress_callback
        self._window_name = window_name
        self._is_window_created = False

    @property
    def is_window_created(self):
        return self._is_window_created

    def create_window(self):
        cv2.namedWindow(self._window_name)
        self._is_window_created = True

    def show(self, frame):
        cv2.imshow(self._window_name, frame)

    def destroy_window(self):
        cv2.destroyWindow(self._window_name)
        self._is_window_created = False

    def process_events(self):
        keykode = cv2.waitKey(1)
        if self.keypress_callback is not None and keykode != -1:
            keykode &= 0xFF
            self.keypress_callback(keykode)
