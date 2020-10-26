# Pontificia Universidad Javeriana. Departamento de Electrónica
# Authors: Juan Henao, Marian Fuentes; Estudiantes de Ing. Electrónica.
# Procesamiento de Imagenes y video
# 25/10/2020

# Import Librarys
import numpy as np
import cv2
import glob
import os
import json

# Control the number of vertices findChessBoardCorner is going to find.
row = 6
col = 7

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((col * row, 3), np.float32)
objp[:, :2] = np.mgrid[0:row, 0:col].T.reshape(-1, 2)

# Arrays to store object points and image points from all the images.
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.

# We calibrated two cameras one from a pc and another from a cell
Cell_Phone_Path = 'C:/Users/ACER/Desktop/Semestre10/Imagenes/Presentaciones/Semana 11/ChessPhotos'
Web_Cam_Path = 'C:/Users/ACER/Desktop/Semestre10/Imagenes/Presentaciones/Semana 11/WebCam Chess'

path = Web_Cam_Path #Change path if you want to change to another library of photos

#Name of the images  glob is going to search for, we used images named Chess (1), Chess (2) etc...
Cell_img_name = 'Chess*.jpeg'
WebCam_img_name = 'Chess*.jpg'

imgName = WebCam_img_name # Change the name of the Images you are going to look for
path_file = os.path.join(path, imgName)

images = glob.glob(path_file)
i = 0

#We had to resize one of our image librarys in order to recognize it with the open cv function, kinda weird
#But it works so it´s possible you may have to do this as well, control the scale factor:
scale = 1
for fname in images:
    img = cv2.imread(fname)
    #You can comment the next line if you are NOT going to resize our images.
    img = cv2.resize(img, (int(img.shape[1] * scale), int(img.shape[0] * scale)), interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (row, col), None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (row, col), corners2, ret)
        cv2.imshow('img ', img)
        cv2.waitKey(0)
        i = i + 1

cv2.destroyAllWindows()
print('Images Aproved: ',i) #Number of images open cv function approved.

# get your specs.
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# Just to take a look, this is the info we wanted to get from the images.
print('Camera Matrix: ')
print(mtx)
print('Distortion Parameters: ')
print(dist)

# reprojection error
mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
    mean_error += error

# If projection error is low it means the calibration Data you extracted is trustworthy
print("total error: {}".format(mean_error / len(objpoints)))

# Compare distorted and undistroted images using open cv methods
# undistortion
Cell_name = 'Chess (2).jpeg'
Web_name  = 'Chess (2).jpg'

path_file = os.path.join(path, Web_name) #If you are using different image name´s make sure to change them
img = cv2.imread(path_file)
#Again if you are NOT resizing your images comment the next line
img = cv2.resize(img, (int(img.shape[1] * scale), int(img.shape[0] * scale)), interpolation=cv2.INTER_AREA)
h, w = img.shape[:2]
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

# There are two different methods to undistort the image, suit yourself.
if True:
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
else:
    mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w, h), 5)
    dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)

# crop the image
x, y, w, h = roi
dst = dst[y:y + h, x:x + w]
cv2.imshow('distorted', img)
cv2.imshow('calibresult', dst)
cv2.waitKey(0)

# Finally we are saving important info + some other info (tilt, pan, d and h) into a JSON file.
path = 'C:/Users/ACER/Desktop/Semestre10/Imagenes/Presentaciones/Semana 11' #Change the path

# You can change the names as well
file_Cell = 'Cell_Calibration.json'
file_WebCam = 'WebCam_Calibration.json'

json_file = os.path.join(path, file_WebCam)# Here

data = {
    'K': mtx.tolist(),
    'tilt': 30,
    'pan': 0,
    'd': 3,
    'h': 2
}

with open(json_file, 'w') as fp:
    json.dump(data, fp, sort_keys=True, indent=1, ensure_ascii=False)

##############################################################################################################
#### Pontificia Universidad Javeriana, Sede Bogota.                    #######################################
#### Authors: Juan Henao & Marian Fuentes. - Proc. de imagenes y video #######################################
#### Source(s): Cv2 Documentation, Julian Quiroga Phd                  #######################################
##############################################################################################################