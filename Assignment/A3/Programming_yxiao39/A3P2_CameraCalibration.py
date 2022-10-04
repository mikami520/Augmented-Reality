import numpy as np
import cv2 as cv
import glob
import matplotlib.pyplot as plt
import argparse


def parse_command_line():
    parser = argparse.ArgumentParser(description="Camera Calibration Pipeline")
    parser.add_argument(
        "-ip",
        type=str,
        help="absolute path to the image directory"
    )
    args = parser.parse_args()
    return args

def Calibrate(image_path, grid_width, grid_height, edge):
    chessboard = (grid_height, grid_width)
    # termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((grid_width*grid_height,3), np.float32)
    objp[:,:2] = (np.mgrid[0:grid_height,0:grid_width]*edge).T.reshape(-1,2)
    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.
    for fname in glob.glob(image_path + '/*.png'):
        img = cv.imread(fname)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, chessboard, cv.CALIB_CB_ADAPTIVE_THRESH
                                                + cv.CALIB_CB_FAST_CHECK +
                                                cv.CALIB_CB_NORMALIZE_IMAGE)
        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)
            corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners)
            cv.drawChessboardCorners(img, chessboard, corners2, ret)
            cv.imshow('img', img)
            cv.waitKey(500)
    cv.destroyAllWindows()
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    mean_error = 0
    img_num = []
    img_error = []
    for i in range(len(objpoints)):
        imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = np.linalg.norm(np.subtract(imgpoints[i],imgpoints2)) / len(imgpoints2)
        img_num.append(i+1)
        img_error.append(error)
        mean_error += error

    plt.xlabel('Image Number')
    plt.ylabel('Re-projective Error')
    plt.title('Re-projective Error Before Elimination of Outliers')
    plt.plot(img_num,img_error)
    plt.show()
    MSE = mean_error/len(objpoints)
    print('---------------------Before Elimination of Outliers---------------------------------')
    print('camera matrix:')
    print(mtx)
    print('distortion coefficients:')
    print(dist)
    print (f"Mean Re-projective Error: {MSE}")
    
    
    image_copy = imgpoints.copy()
    pos = 0
    for i in range(len(img_error)):
        if abs(img_error[i] - MSE) / MSE > 0.25:
            objpoints.pop(0)
            image_copy.pop(i - pos)
            pos += 1
    
    imgpoints = image_copy
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    mean_error = 0
    img_num = []
    img_error = []
    for i in range(len(objpoints)):
        imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = np.linalg.norm(np.subtract(imgpoints[i],imgpoints2)) / len(imgpoints2)
        img_num.append(i+1)
        img_error.append(error)
        mean_error += error

    plt.xlabel('Image Number')
    plt.ylabel('Re-projective Error')
    plt.title('Re-projective Error After Elimination of Outliers')
    plt.plot(img_num,img_error)
    plt.show()
    MSE = mean_error/len(objpoints)
    print('---------------------After Elimination of Outliers---------------------------------')
    print('camera matrix:')
    print(mtx)
    print('distortion coefficients:')
    print(dist)
    print (f"Mean Re-projective Error: {MSE}")

def main():
    args = parse_command_line()
    image_path = args.ip
    width = 7
    height = 6
    edge_length = 0.03
    Calibrate(image_path, width, height, edge_length)


if __name__ == '__main__':
    main()