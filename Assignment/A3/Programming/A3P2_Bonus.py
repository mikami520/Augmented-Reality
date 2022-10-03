import numpy as np
import cv2 as cv
import glob
import matplotlib.pyplot as plt
import argparse
import os


def parse_command_line():
    parser = argparse.ArgumentParser(description="Camera Calibration Pipeline")
    parser.add_argument(
        "-fip",
        type=str,
        help="absolute path to the first camera directory"
    )
    parser.add_argument(
        "-sip",
        type=str,
        help="absolute path to the second camera directory"
    )
    args = parser.parse_args()
    return args

def Calibrate(image_camera1_path, image_camera2_path, grid_width, grid_height, edge):
    chessboard = (grid_height, grid_width)
    # termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((grid_width*grid_height, 3), np.float32)
    objp[:,:2] = (np.mgrid[0:grid_height, 0:grid_width]*edge).T.reshape(-1,2)
    # Arrays to store object points and image points from all the images.
    objpoints1 = [] # 3d point in real world space
    imgpoints1 = [] # 2d points in image plane.
    objpoints2 = [] # 3d point in real world space
    imgpoints2 = [] # 2d points in image plane.
    for fname in glob.glob(image_camera1_path + '/*.png'):
        filename = os.path.basename(fname).split('.')[0]
        img1 = cv.imread(fname)
        img2 = cv.imread(os.path.join(image_camera2_path, filename + '.png'))
        gray1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
        gray2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
        # Find the chess board corners
        ret1, corners1 = cv.findChessboardCorners(gray1, chessboard, cv.CALIB_CB_ADAPTIVE_THRESH
                                                + cv.CALIB_CB_FAST_CHECK +
                                                cv.CALIB_CB_NORMALIZE_IMAGE)
        ret2, corners2 = cv.findChessboardCorners(gray2, chessboard, cv.CALIB_CB_ADAPTIVE_THRESH
                                                + cv.CALIB_CB_FAST_CHECK +
                                                cv.CALIB_CB_NORMALIZE_IMAGE)
        # If found, add object points, image points (after refining them)
        if ret1 == True and ret2 == True:
            objpoints1.append(objp)
            objpoints2.append(objp)
            corners11 = cv.cornerSubPix(gray1, corners1, (11,11), (-1,-1), criteria)
            corners22 = cv.cornerSubPix(gray2, corners2, (11,11), (-1,-1), criteria)
            imgpoints1.append(corners11)
            imgpoints2.append(corners22)
            cv.drawChessboardCorners(img1, chessboard, corners11, ret1)
            cv.imshow('img', img1)
            cv.waitKey(500)
            cv.drawChessboardCorners(img2, chessboard, corners22, ret2)
            cv.imshow('img', img2)
            cv.waitKey(500)
    cv.destroyAllWindows()
    ret1, mtx1, dist1, rvecs1, tvecs1 = cv.calibrateCamera(objpoints1, imgpoints1, gray1.shape[::-1], None, None)
    ret2, mtx2, dist2, rvecs2, tvecs2 = cv.calibrateCamera(objpoints2, imgpoints2, gray2.shape[::-1], None, None)

    mean_error1 = 0
    img_num1 = []
    img_error1 = []
    for i in range(len(objpoints1)):
        imgpoints11, _ = cv.projectPoints(objpoints1[i], rvecs1[i], tvecs1[i], mtx1, dist1)
        error = np.linalg.norm(np.subtract(imgpoints1[i],imgpoints11)) / len(imgpoints11)
        img_num1.append(i+1)
        img_error1.append(error)
        mean_error1 += error

    plt.xlabel('Image Number')
    plt.ylabel('Re-projective Error')
    plt.title('Re-projective Error of Camera 1 Before Elimination of Outliers')
    plt.plot(img_num1, img_error1)
    plt.show()
    MSE1 = mean_error1/len(objpoints1)
    
    mean_error2 = 0
    img_num2 = []
    img_error2 = []
    for i in range(len(objpoints2)):
        imgpoints22, _ = cv.projectPoints(objpoints2[i], rvecs2[i], tvecs2[i], mtx2, dist2)
        error = np.linalg.norm(np.subtract(imgpoints2[i],imgpoints22)) / len(imgpoints22)
        img_num2.append(i+1)
        img_error2.append(error)
        mean_error2 += error

    plt.xlabel('Image Number')
    plt.ylabel('Re-projective Error')
    plt.title('Re-projective Error of Camera 2 Before Elimination of Outliers')
    plt.plot(img_num2, img_error2)
    plt.show()
    MSE2 = mean_error2/len(objpoints2)
    print('---------------------Camera 1 Before Elimination of Outliers---------------------------------')
    print('camera matrix:')
    print(mtx1)
    print('distortion coefficients:')
    print(dist1)
    print (f"Mean Re-projective Error: {MSE1}")
    print('---------------------Camera 2 Before Elimination of Outliers---------------------------------')
    print('camera matrix:')
    print(mtx2)
    print('distortion coefficients:')
    print(dist2)
    print (f"Mean Re-projective Error: {MSE2}")
    
    
    image_copy1 = imgpoints1.copy()
    image_copy2 = imgpoints2.copy()
    pos = 0
    for i in range(len(img_error1)):
        if abs(img_error1[i] - MSE1) / MSE1 > 0.25 or abs(img_error2[i] - MSE2) / MSE2 > 0.25:
            objpoints1.pop(0)
            objpoints2.pop(0)
            image_copy1.pop(i - pos)
            image_copy2.pop(i - pos)
            pos += 1
    
    imgpoints1 = image_copy1 
    imgpoints2 = image_copy2
    ret1, mtx1, dist1, rvecs1, tvecs1 = cv.calibrateCamera(objpoints1, imgpoints1, gray1.shape[::-1], None, None)
    ret2, mtx2, dist2, rvecs2, tvecs2 = cv.calibrateCamera(objpoints2, imgpoints2, gray2.shape[::-1], None, None)
    mean_error1 = 0
    img_num1 = []
    img_error1 = []
    for i in range(len(objpoints1)):
        imgpoints11, _ = cv.projectPoints(objpoints1[i], rvecs1[i], tvecs1[i], mtx1, dist1)
        error = np.linalg.norm(np.subtract(imgpoints1[i], imgpoints11)) / len(imgpoints11)
        img_num1.append(i+1)
        img_error1.append(error)
        mean_error1 += error

    plt.xlabel('Image Number')
    plt.ylabel('Re-projective Error')
    plt.title('Re-projective Error of Camera 1 After Elimination of Outliers')
    plt.plot(img_num1,img_error1)
    plt.show()
    MSE1 = mean_error1/len(objpoints1)
    print('---------------------Camera 1 After Elimination of Outliers---------------------------------')
    print('camera matrix:')
    print(mtx1)
    print('distortion coefficients:')
    print(dist1)
    print (f"Mean Re-projective Error: {MSE1}")
    
    mean_error2 = 0
    img_num2 = []
    img_error2 = []
    for i in range(len(objpoints2)):
        imgpoints22, _ = cv.projectPoints(objpoints2[i], rvecs2[i], tvecs2[i], mtx2, dist2)
        error = np.linalg.norm(np.subtract(imgpoints2[i], imgpoints22)) / len(imgpoints22)
        img_num2.append(i+1)
        img_error2.append(error)
        mean_error2 += error

    plt.xlabel('Image Number')
    plt.ylabel('Re-projective Error')
    plt.title('Re-projective Error of Camera 2 After Elimination of Outliers')
    plt.plot(img_num2, img_error2)
    plt.show()
    MSE2 = mean_error2/len(objpoints2)
    print('---------------------Camera 2 After Elimination of Outliers---------------------------------')
    print('camera matrix:')
    print(mtx2)
    print('distortion coefficients:')
    print(dist2)
    print (f"Mean Re-projective Error: {MSE2}")
    
    print('---------------------Stereo Camera Calibration After Elimination of Outliers---------------------------------')
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.0001)
    stereocalibration_flags = cv.CALIB_FIX_INTRINSIC
    rms, mtx1, dist1, mtx2, dist2, rvecs, tvecs, E, F = cv.stereoCalibrate(objpoints1, imgpoints1, imgpoints2, mtx1, 
                                                                           dist1, mtx2, dist2, gray1.shape[::-1], criteria = criteria, flags = stereocalibration_flags)
    R1, R2, P1, P2, Q, roi_left, roi_right = cv.stereoRectify(mtx1, dist1, mtx2, dist2, chessboard, rvecs, tvecs,
                                                              flags=cv.CALIB_ZERO_DISPARITY, alpha=0.9)
    print(f'Root Mean Square Error:{rms}')
    print('camera 1 matrix:')
    print(mtx1)
    print('camera 1 distortion coefficients:')
    print(dist1)
    print('camera 2 matrix: ')
    print(mtx2)
    print('camera 2 distortion coefficients:')
    print(dist2)
    print('Projective matrix:')
    print(Q)


def main():
    args = parse_command_line()
    image_camera1_path = args.fip
    image_camera2_path = args.sip
    width = 7
    height = 6
    edge_length = 0.03
    Calibrate(image_camera1_path, image_camera2_path, width, height, edge_length)
    


if __name__ == '__main__':
    main()