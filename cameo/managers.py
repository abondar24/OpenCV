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
        self._image_filename = None
        self._video_filename = None
        self._video_encoding = None
        self._video_writer = None
        self._start_time = None
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

    @property
    def is_writing_image(self):
        return self._image_filename is not None

    @property
    def is_writing_video(self):
        return self._video_filename is not None

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

        # write to img
        if self.is_writing_image:
            cv2.imwrite(self._image_filename, self._frame)
            self._image_filename = None

        # write to video
        self._write_video_frame()

        # release the frame
        self._frame = None
        self._entered_frame = False

    def write_image(self, filename):
        self._image_filename = filename

    def start_writing_video(self, filename, encoding = cv2.cv.CV_FOURCC('I', '4', '2', '0')):
        self._video_filename = filename
        self._video_encoding = encoding

    def stop_writing_video(self):
        self._video_filename = None
        self._video_encoding = None
        self._video_writer = None

    def _write_video_frame(self):
        if not self.is_writing_video:
            return

        if self._video_writer is None:
            fps = self._capture.get(cv2.cv.CV_CAP_PROP_FPS)
            if fps == 0.0:
                if self._frames_elapsed < 20:
                    return

                else:
                    fps = self._fps_est

            size = (int(self._capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),
                    int(self._capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))

            self._video_writer = cv2.VideoWriter(self._video_filename, self._video_encoding, fps, size)
            self._video_writer.write(self._frame)


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
