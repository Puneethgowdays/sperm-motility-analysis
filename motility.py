import math

def total_distance(points):

    dist = 0

    for i in range(1,len(points)):

        x1,y1 = points[i-1]
        x2,y2 = points[i]

        dist += math.hypot(x2-x1,y2-y1)

    return dist


def straight_distance(points):

    x1,y1 = points[0]
    x2,y2 = points[-1]

    return math.hypot(x2-x1,y2-y1)


def classify_motility(points,fps):

    if len(points) < 5:
        return "IMMOTILE"

    total = total_distance(points)
    straight = straight_distance(points)

    straightness = straight / total if total > 0 else 0

    time = len(points) / fps
    velocity = total / time if time > 0 else 0

    if straightness > 0.7:
        return "PROGRESSIVE"

    elif velocity > 2:
        return "NON_PROGRESSIVE"

    else:
        return "IMMOTILE"