import numpy as np
import math

vertices = []
simplices = []

def getP1Pn(bucket):
    p1 = bucket[0]
    pn = bucket[0]

    for i in range (len(bucket)):
        if(bucket[i] < p1):
            p1 = bucket[i]
        elif(bucket[i] > pn):
            pn = bucket[i]

    return p1,pn

def getLeftRightPoints(bucket,p1,pn):
    left = []
    right = []

    for i in range(len(bucket)):
            a = np.array([p1,pn,bucket[i]])
            b = np.array([[1], [1], [1]])
            m = np.append(a, b, axis=1)
            det = np.linalg.det(m)
            if (det > 0):
                left.append(bucket[i])
            if (det < 0):
                right.append(bucket[i])

    return left,right

def getFarthestPoint(bucket,p1,pn):
    dist = 0
    idx = 0

    for i in range(len(bucket)):
        p1dist = math.sqrt((bucket[i][0] - p1[0])**2 + (bucket[i][1] - p1[1])**2)
        pndist = math.sqrt((bucket[i][0] - pn[0])**2 + (bucket[i][1] - pn[1])**2)
      
        if ((p1dist + pndist) > dist):
            dist = p1dist + pndist
            idx = i

    return bucket[idx]

def recursiveLeft(bucket,p1,pn):
    if(len(bucket) == 0):
        return
    else:
        farthestPoint = getFarthestPoint(bucket,p1,pn)

        bucket.remove(farthestPoint)
        vertices.append(farthestPoint)

        left1, right1 = getLeftRightPoints(bucket,p1,farthestPoint)
        left2, right2 = getLeftRightPoints(bucket,farthestPoint,pn)

        recursiveLeft(left1,p1,farthestPoint)
        recursiveLeft(left2,farthestPoint,pn)

def recursiveRight(bucket,p1,pn):
    if(len(bucket) == 0):
        return
    else:
        farthestPoint = getFarthestPoint(bucket,p1,pn)

        bucket.remove(farthestPoint)
        vertices.append(farthestPoint)

        left1, right1 = getLeftRightPoints(bucket,p1,farthestPoint)
        left2, right2 = getLeftRightPoints(bucket,farthestPoint,pn)

        recursiveRight(right1,p1,farthestPoint)
        recursiveRight(right2,farthestPoint,pn)

def recursiveMain(bucket,p1,pn):
    vertices.clear()

    leftPoints, rightPoints = getLeftRightPoints(bucket,p1,pn)

    vertices.append(p1)
    vertices.append(pn)

    recursiveLeft(leftPoints,p1,pn)
    recursiveRight(rightPoints,p1,pn)

def getVertices(bucket):
    bucket = bucket.tolist()
    p1, pn = getP1Pn(bucket)

    recursiveMain(bucket,p1,pn)

    return vertices

def sortVertices(vertices):
    centerX = sum(point[0] for point in vertices) / len(vertices)
    centerY = sum(point[1] for point in vertices) / len(vertices)

    vertices.sort(key = lambda point: math.atan2(point[0] - centerX, point[1] - centerY))

    return vertices

def getSimplices(vertices):
    simplices.clear()

    for i in range(len(vertices)):
        if(i == len(vertices) - 1):
            simplices.append([vertices[i], vertices[0]])
        else:
            simplices.append([vertices[i], vertices[i+1]])

def myConvexHull(bucket):
    vertices = getVertices(bucket)
    SortedVertices = sortVertices(vertices)
    getSimplices(SortedVertices)

    return simplices
