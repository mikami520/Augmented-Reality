# EN.601.454/654 Augmented Reality

## Assignment 3

**Name: Yuliang Xiao**
**JHED: yxiao39**
**Date: 10/02/2022**
**Programming Platform: Python v3.8.13**

### Contents

1. ```A3P2_CameraCalibration.py``` - main program to run the single camera calibration
2. ```A3P2_StereoCamera.py``` - main program to run the stereo camera calibration
3. ```A3P2_Bonus``` - main program to run the bonus part
4. ```Problem2_Report.pdf``` - report of camera calibration on each dataset

### Dependencies
1. OpenCV - v4.6.0.66
2. Matplotlib - v3.5.2

### Procedure to compile and run the code
1. Open **Terminal**
2. Create **python3 virtual environment**
    ```conda create -n your_env_name``` or ```python3 -m venv /path/to/your_env_name/bin/activate```
3. Activate the virtual environment
    ```conda activate your_env_name``` or ```source /path/to/your_env_name/bin/activate```
4. Install dependencies listed above using 
    ```pip install PackageName```
5. Change directory to the scripts folder
   ```cd /path/to/script_folder```
6. To test single camera calibration, run
    ```python3 A3P2_CameraCalibration.py -ip /path/to/camera_dataset```
    **You can also use ```-h``` to get help list**
7. To test stereo camera calibration, run
    ```python3 A3P2_StereoCamera.py -fip /path/to/first_camera_dataset -sip /path/to second_camera_dataset```
    **You can also use ```-h``` to get help list**
8. To test Bonus part, run
    ```python3 A3P2_Bonus.py -fip /path/to/first_camera_dataset -sip /path/to second_camera_dataset```
    **You can also use ```-h``` to get help list**

### Outputs
The calibration results (Camera Matrix, Distortion Coefficients, etc) are shown on the terminal and re-projective plots are also displayed. (Remember to close the plot every time to continue the program)
