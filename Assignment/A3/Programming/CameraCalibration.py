import numpy as np
import cv2 as cv
import os
import matplotlib.pyplot as plt

def CameraCalibration(path, width, height, size):
    # termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    objp = np.zeros((width*height, 3), np.float32)
    objp[:, :2] = (np.mgrid[0:height, 0:width]*size).T.reshape(-1, 2)
    gray = []
    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.
    for fname in os.listdir(path):

        img = cv.imread(path+'/'+fname)

        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        # Find the chess board corners

        ret, corners = cv.findChessboardCorners(gray, (height, width), None)
        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)
            corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)
    #         Draw and display the corners
            cv.drawChessboardCorners(img, (height, width), corners2, ret)
            cv.imshow('img', img)
            cv.waitKey(500)
    cv.destroyAllWindows()
    print(len(objpoints))
    # calibrate the camera
    ret, K, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    # calculate mean square error
    square_error = 0
    error = []
    for i in range(len(objpoints)):
        # print(objpoints[i])
        imgpoints2, par = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], K, dist)
        e = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
        error.append(e)
        square_error += error[i]
    # print(len(error))
    plt.plot(error)
    plt.xlabel('Image Number')
    plt.ylabel('Re-projection Error')
    plt.title('Re-projection Error before Elimination of Outliners')

    plt.show()

    rms = square_error / len(objpoints)


    # eliminate the points whose relative error is greater than 0.2
    imgtemp = imgpoints.copy()
    flag = -1
    for i in range(len(imgtemp)):
        if abs((error[i] - rms))/rms > 0.2:
            flag += 1
            objpoints.pop()
            imgpoints.pop(i-flag)

    # calibrate the camera
    ret, K, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    # calculate mean square error
    square_error = 0
    error = []
    for i in range(len(objpoints)):
        # print(objpoints[i])
        imgpoints2, par = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], K, dist)
        e = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2) / len(imgpoints2)
        error.append(e)
        square_error += error[i]
    # print(len(error))
    # print(error)

    plt.plot(error)
    plt.xlabel('Image Number')
    plt.ylabel('Re-projection Error')
    plt.title('Re-projection Error after Elimination of Outliners')

    plt.show()
    rms = square_error / len(objpoints)

    return rms, K, dist

# for debugging
path = '/Users/sakuraxiao/Desktop/Augmented-Reality/Assignment/A3/Programming/RGB'

rms, K, dist = CameraCalibration(path, 7, 6, 0.03)

print(rms)
print(K)
print(dist)