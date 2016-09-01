import cv2
import numpy
import scipy.interpolate


def create_curve_func(points):
    if points is None:
        return None
    num_points = len(points)
    if num_points < 2:
        return None
    xs, ys = zip(*points)
    if num_points <4:
        kind = 'linear'
    else:
        kind = 'cubic'

    return scipy.interpolate.interp1d(xs, ys, kind, bounds_error=False)


def create_lookup_array(func, length=256):
    """Return lookup for a whole-number of inputs to a func"""

    if func is None:
        return None
    lookup_array = numpy.empty(length)
    i = 0
    while i < length:
        func_i = func(i)
        lookup_array[i] = min(max(0, func_i), length - 1)
        i += 1
    return lookup_array


def apply_lookup_array(lookup_array, src, dst):
    """Map a src to dst using lookup"""
    if lookup_array is None:
        return
    dst[:] = lookup_array[src]


def create_composite_func(func0, func1):
    """ return a composite of two funcs"""
    if func0 is None:
        return func1

    if func1 is None:
        return func0

    return lambda x: func0(func1(x))


def create_flat_view(array):
    """return 1d view of and n-dim array"""
    flat_view = array.view()
    flat_view.shape = array.size
    return flat_view


def is_gray(image):
    """Return true if the image has one channel per pixel"""
    return image.ndim < 3


def width_height_divided_by(image, divisor):
    """Return an images dimensions, divided by a value"""
    h, w = image.shape[:2]
    return w / divisor, h / divisor