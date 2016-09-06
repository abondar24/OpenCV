import cv2


def outline_rect(image, rect, color):
    if rect is None:
        return

    x, y, w, h = rect
    cv2.rectangle(image, (x, y), (x+w, y+h), color)


def copy_rect(src, dst, src_rect, dst_rect, interpolation=cv2.INTER_LINEAR):
    """Copy part of the src to part of the dest"""

    x0, y0, w0, h0 = src_rect
    x1, y1, w1, h1 = dst_rect

    # Resize the contents of the source sub-rect
    # Put the result in the destination sub-rect
    dst[y1:y1+h1, x1:x1+w1] = cv2.resize(src[y0:y0+h0, x0:x0+w0], (w1, h1), interpolation=interpolation)


def swap_rects(src, dst, rects, interpolation=cv2.INTER_LINEAR):
    """Copy src with two or more sub-rects swapped"""
    if dst is not src:
        dst[:] = src

    num_rects = len(rects)

    if num_rects < 2:
        return

    # Copy the contents of the last rect into temp storage
    x, y, w, h = rects[num_rects - 1]
    temp = src[y:y+h, x:x+w].copy()

    # Copy the contents of each rect into the next
    i = num_rects - 2
    while i >= 0:
        copy_rect(src, dst, rects[i], rects[i+1], interpolation)
        i -= 1

    # Copy the temp stored content into the first rect
    copy_rect(temp, dst, (0, 0, w, h), rects[0], interpolation)

