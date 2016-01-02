def point_in_rect(point, rect):
    return point[0] >= rect[0][0] and \
            point[0] <= rect[1][0] and \
            point[1] >= rect[0][1] and \
            point[1] <= rect[2][1]


def sign(x):
    return x / abs(x) if x != 0 else 0
