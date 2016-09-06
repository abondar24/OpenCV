import cv2
import numpy as np
import utils


def recolor_rc(src, dst):
    # conversion simulation BGR to RC
    b, g, r = cv2.split(src)

    # replace b with avg of b and g
    cv2.addWeighted(b, 0.5, g, 0.5, 0, b)
    cv2.merge((b, g, r), dst)


def recolor_cmv(src, dst):
    # bgr to cmv with yellow disaturate
    b, g, r = cv2.split(src)
    cv2.max(b, g, b)
    cv2.max(b, r, b)
    cv2.merge((b, g, r), dst)


class VfuncFilter(object):
    """Filter that applies a function to  V or all BGR"""

    def __init__(self, vfunc=None, dtype=np.uint8):
        len = np.iinfo(dtype).max + 1
        self._vlookup_array = utils.create_lookup_array(vfunc, len)

    def apply(self, src, dst):
        src_flat_view = utils.create_flat_view(src)
        dst_flat_view = utils.create_flat_view(dst)
        utils.apply_lookup_array(self._vlookup_array, src_flat_view, dst_flat_view)


class VCurveFilter(VfuncFilter):
    """Filter applied to curve V or all BGR"""
    def __init__(self, vPoints, dtype = np.uint8):
        VfuncFilter.__init__(self, utils.create_curve_func(vPoints), dtype)

class BGRFuncFilter(object):
    """Filter applied to different functions to each of BGR"""
    def __init__(self, vfunc=None, bfunc = None, gfunc = None, rfunc=None, dtype = np.uint8):
        len = np.iinfo(dtype).max + 1

        self._blookup_array = utils.create_lookup_array(utils.create_composite_func(bfunc, vfunc), len)
        self._glookup_array = utils.create_lookup_array(utils.create_composite_func(gfunc, vfunc), len)
        self._rlookup_array = utils.create_lookup_array(utils.create_composite_func(rfunc, vfunc), len)

    def apply(self, src, dst):
        b, g, r = cv2.split(src)

        utils.apply_lookup_array(self._blookup_array, b, b)
        utils.apply_lookup_array(self._glookup_array, g, g)
        utils.apply_lookup_array(self._rlookup_array, r, r)

        cv2.merge([b, g, r], dst)


class BGRCurveFilter(BGRFuncFilter):
    """Filter applied to different curves to each of BGR"""

    def __init__(self, vpoints=None, bpoints=None, gpoints=None, rpoints=None, dtype=np.uint8):
        BGRFuncFilter.__init__(self,
                               utils.create_curve_func(vpoints),
                               utils.create_curve_func(bpoints),
                               utils.create_curve_func(gpoints),
                               utils.create_curve_func(rpoints),
                               dtype)


class BGRPortaCurveFilter(BGRCurveFilter):
    """Filter applies Porta-like curves to each of BGR"""

    def __init__(self, dtype=np.uint8):
        BGRCurveFilter.__init__(self,
                               vpoints=[(0, 0),(23, 20), (157, 173), (255, 255)],
                               bpoints=[(0, 0), (41, 46), (231, 228), (255, 255)],
                               gpoints=[(0, 0), (52, 47), (189, 196), (255, 255)],
                               rpoints=[(0, 0), (69, 69), (213, 218), (255, 255)],
                               dtype = dtype)


class BGRProviaCurveFilter(BGRCurveFilter):
    """Filter applies Provia-like curves to each of BGR"""

    def __init__(self, dtype=np.uint8):
        BGRCurveFilter.__init__(self,
                               bpoints=[(0, 0), (35, 25), (205, 227), (255, 255)],
                               gpoints=[(0, 0), (27, 21), (196, 207), (255, 255)],
                               rpoints=[(0, 0), (59, 54), (202, 210), (255, 255)],
                               dtype = dtype)


class BGRVelviaCurveFilter(BGRCurveFilter):
    """Filter applies Velvia-like curves to each of BGR"""

    def __init__(self, dtype=np.uint8):
        BGRCurveFilter.__init__(self,
                               vpoints=[(0, 0), (128, 118), (221, 215), (255, 255)],
                               bpoints=[(0, 0), (25, 21), (122, 153), (255, 255)],
                               gpoints=[(0, 0), (25, 21), (95, 202), (255, 255)],
                               rpoints=[(0, 0), (41, 28), (183, 209), (255, 255)],
                               dtype = dtype)


class BGRCrossProcessCurveFilter(BGRCurveFilter):
    """Filter applies cross-process-like curves to each of BGR"""

    def __init__(self, dtype=np.uint8):
        BGRCurveFilter.__init__(self,
                               bpoints=[(0, 20), (255, 255)],
                               gpoints=[(0, 0), (56, 39), (208, 226), (255, 255)],
                               rpoints=[(0, 0), (56, 22), (211, 255), (255, 255)],
                               dtype = dtype)


def stroke_edges(src, dst, blur_ksize = 7, edge_ksize = 5):
    if blur_ksize == 3:
        blurred_src = cv2.medianBlur(src, blur_ksize)
        gray_src = cv2.cvtColor(blurred_src, cv2.COLOR_BGR2GRAY)
    else:
        gray_src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    cv2.Laplacian(gray_src, cv2.cv.CV_8U, gray_src, ksize=edge_ksize)
    normalized_inverse_alpha = (1.0 / 255) * (255 - gray_src)
    channels = cv2.split(src)
    for channel in channels:
        channel[:] = channel * normalized_inverse_alpha
    cv2.merge(channels, dst)


class VConvolutionFilter(object):
    """A filter that applies a convolution to V (or all of BGR)"""

    def __init__(self, kernel):
        self._kernel = kernel

    def apply(self, src, dst):
        """Apply the filter with a BGR or gray src/dst"""
        cv2.filter2D(src, -1, self._kernel, dst)


class SharpenFilter(VConvolutionFilter):
    """A sharpen filter with a 1-pixel radius."""

    def __init__(self):
        kernel = np.array([-1, -1, -1],
                          [-1, 9, -1],
                          [-1, -1, -1])
        VConvolutionFilter.__init__(self, kernel)


class FindEdgesFilter(VConvolutionFilter):
    """An edge-finding filter with a 1-pixel radius."""

    def __init__(self):
        kernel = np.array([-1, -1, -1],
                          [-1, 8, -1],
                          [-1, -1, -1])
        VConvolutionFilter.__init__(self, kernel)


class BlurFilter(VConvolutionFilter):
    """A blur filter with a 2-pixel radius."""

    def __init__(self):
        kernel = np.array([[0.04, 0.04, 0.04, 0.04, 0.04],
                          [0.04, 0.04, 0.04, 0.04, 0.04],
                          [0.04, 0.04, 0.04, 0.04, 0.04],
                          [0.04, 0.04, 0.04, 0.04, 0.04],
                          [0.04, 0.04, 0.04, 0.04, 0.04]])
        VConvolutionFilter.__init__(self, kernel)


class EmbossFilter(VConvolutionFilter):
    """An emboss filter with a 1-pixel radius."""

    def __init__(self):
        kernel = np.array([[-2, -1, 0],
                          [-1, 1, 1],
                          [0, 1, 2]])
        VConvolutionFilter.__init__(self, kernel)

