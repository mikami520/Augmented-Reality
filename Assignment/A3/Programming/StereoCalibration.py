import numpy as np
import cv2 as cv
import os
import matplotlib.pyplot as plt

def StereoCalibration(path1, path2, width, height, size):
    # termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    objp = np.zeros((width * height, 3), np.float32)
    objp[:, :2] = (np.mgrid[0:height, 0:width] * size).T.reshape(-1, 2)
    gray1 = []
    gray2 = []
    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints1 = []  # 2d points in image plane.
    imgpoints2 = []
    for fname in os.listdir(path1):

        img1 = cv.imread(path1 + '/' + fname)
        img2 = cv.imread(path2 + '/' + fname)
        gray1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
        gray2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)

        # Find the chess board corners

        ret1, corners1 = cv.findChessboardCorners(gray1, (height, width), None)
        ret2, corners2 = cv.findChessboardCorners(gray2, (height, width), None)
        # If found, add object points, image points (after refining them)
        if (ret1 & ret2) == True:
            objpoints.append(objp)
            corners1 = cv.cornerSubPix(gray1, corners1, (11, 11), (-1, -1), criteria)
            corners2 = cv.cornerSubPix(gray2, corners2, (11, 11), (-1, -1), criteria)
            imgpoints1.append(corners1)
            imgpoints2.append(corners2)

            #         Draw and display the corners
            cv.drawChessboardCorners(img1, (height, width), corners1, ret1)
            cv.imshow('img1', img1)
            cv.waitKey(500)
            cv.drawChessboardCorners(img2, (height, width), corners2, ret2)
            cv.imshow('img2', img2)
            cv.waitKey(500)
    cv.destroyAllWindows()

    # calibrate the camera
    ret1, K1, D1, rvecs1, tvecs1 = cv.calibrateCamera(objpoints, imgpoints1, gray1.shape[::-1], None, None)
    ret2, K2, D2, rvecs2, tvecs2 = cv.calibrateCamera(objpoints, imgpoints2, gray2.shape[::-1], None, None)

    # get rid of outliners
    square_error1 = 0
    square_error2 = 0
    error1 = []
    error2 = []
    for i in range(len(objpoints)):
        imgpts_rep1, par = cv.projectPoints(objpoints[i], rvecs1[i], tvecs1[i], K1, D1)
        e = cv.norm(imgpoints1[i], imgpts_rep1, cv.NORM_L2) / len(imgpts_rep1)
        error1.append(e)
        square_error1 += error1[i]
    rms1 = square_error1 / len(objpoints)

    plt.plot(error1)
    plt.xlabel('Image Number')
    plt.ylabel('Re-projection Error')
    plt.title('Re-projection Error for the first Camera before Elimination of Outliners')

    plt.show()

    for i in range(len(objpoints)):
        imgpts_rep2, par = cv.projectPoints(objpoints[i], rvecs2[i], tvecs2[i], K2, D2)
        e = cv.norm(imgpoints2[i], imgpts_rep2, cv.NORM_L2) / len(imgpts_rep2)
        error2.append(e)
        square_error2 += error2[i]
    rms2 = square_error2 / len(objpoints)

    plt.plot(error2)
    plt.xlabel('Image Number')
    plt.ylabel('Re-projection Error')
    plt.title('Re-projection Error for the second Camera before Elimination of Outliners')

    plt.show()

    # eliminate the points whose relative error is greater than 0.2
    imgtemp1 = imgpoints1.copy()

    flag = -1
    for i in range(len(imgtemp1)):
        rel1 = abs((error1[i] - rms1)) / rms1
        rel2 = abs((error2[i] - rms2)) / rms2
        if rel1 > 0.25 or rel2 > 0.25:
            flag += 1
            objpoints.pop()
            imgpoints1.pop(i - flag)
            imgpoints2.pop(i - flag)


    # re-calibrate two cameras
    ret1, K1, D1, rvecs1, tvecs1 = cv.calibrateCamera(objpoints, imgpoints1, gray1.shape[::-1], None, None)
    ret2, K2, D2, rvecs2, tvecs2 = cv.calibrateCamera(objpoints, imgpoints2, gray2.shape[::-1], None, None)

    square_error1 = 0
    square_error2 = 0
    error1 = []
    error2 = []
    for i in range(len(objpoints)):
        imgpts_rep1, par = cv.projectPoints(objpoints[i], rvecs1[i], tvecs1[i], K1, D1)
        e = cv.norm(imgpoints1[i], imgpts_rep1, cv.NORM_L2) / len(imgpts_rep1)
        error1.append(e)
        square_error1 += error1[i]

    plt.plot(error1)
    plt.xlabel('Image Number')
    plt.ylabel('Re-projection Error')
    plt.title('Re-projection Error for the first Camera after Elimination of Outliners')

    plt.show()

    for i in range(len(objpoints)):
        imgpts_rep2, par = cv.projectPoints(objpoints[i], rvecs2[i], tvecs2[i], K2, D2)
        e = cv.norm(imgpoints2[i], imgpts_rep2, cv.NORM_L2) / len(imgpts_rep2)
        error2.append(e)
        square_error2 += error2[i]

    plt.plot(error2)
    plt.xlabel('Image Number')
    plt.ylabel('Re-projection Error')
    plt.title('Re-projection Error for the second Camera after Elimination of Outliners')

    plt.show()

    # calibrate the stereo camera
    rms, K1, D1, K2, D2, R, T, E, F = cv.stereoCalibrate(objpoints, imgpoints1, imgpoints2, K1, D1, K2, D2, gray1.shape[::-1])

    R1, R2, P1, P2, Q, roi_left, roi_right = cv.stereoRectify(K1, D1, K2, D2, (width, height), R, T,
                                                              flags=cv.CALIB_ZERO_DISPARITY, alpha=0.9)

    return rms, K1, D1, K2, D2, R1, R2, P1, P2, Q, roi_left, roi_right

# for debugging
path1 = '/Users/sakuraxiao/Desktop/Augmented-Reality/Assignment/A3/Programming/2-Intel/IR'
path2 = '/Users/sakuraxiao/Desktop/Augmented-Reality/Assignment/A3/Programming/2-Intel/RGB'

rms, K1, D1, K2, D2, R1, R2, P1, P2, Q, roi_left, roi_right = StereoCalibration(path1, path2, 7, 6, 0.03)
print(rms)
print(K1)
print(K2)
print(D1)
print(D2)
print(R1)
print(R2)
print(P1)
print(P2)
print(Q)


