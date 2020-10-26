# Pontificia Universidad Javeriana. Departamento de Electrónica
# Authors: Juan Henao, Marian Fuentes; Estudiantes de Ing. Electrónica.
# Procesamiento de Imagenes y video
# 25/10/2020

import cv2
import glob
import os
import json
from camera_model import *


if __name__ == '__main__':
    
    #Read and load calibration file with configuration fields: k, tilt, pan,     d, and h
    path = 'C:/Users/ACER/Desktop/Semestre10/Imagenes/Presentaciones/Semana 11'
    file_name = 'WebCam_Calibration.json'
    json_file = os.path.join(path, file_name)

    with open(json_file) as fp:
        json_data = json.load(fp)
        
    
    
    print('json Data: ')
    print(json_data)
    
    jsondata = tuple(json_data.values())[0]
    jsondata1 = tuple(json_data.values())[1]
    # intrinsics parameters
    fx = jsondata[0][0] #682.5709294664271 #176.9076277699917
    fy = jsondata[1][1] #681.7761163059901 #176.8987015313124
    cx = jsondata[0][2] #316.1976922031661 #83.50938889785682   #width / 2
    cy = jsondata[1][2] #247.18669845478573 #118.69072241965235   #height / 2
    width = int(cx*2)
    height = int(cy*2)
    K = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1.0]])
    tilt = tuple(json_data.values())[4]
    pan = tuple(json_data.values())[3]
    d = tuple(json_data.values())[1]
    #Extrinsics parameters
    h = tuple(json_data.values())[2] #Height of camera
    R = set_rotation(tilt, pan, 0)
    t = np.array([0, -d, h]) #Distance from object in x, y and z
    
    #Create camera
    camera = projective_camera(K, width, height, R, t)

    ####### PROJECT 3D CUBE to 2D CUBE
    
    square_3D = np.array([[0.5, 0.5, 0], [0.5, -0.5, 0], [-0.5, -0.5, 0], [-0.5, 0.5, 0],
                          [0.5, 0.5, 0.5],[0.5, -0.5, 0.5],[-0.5, -0.5, 0.5],[-0.5, 0.5, 0.5]])
    square_2D = projective_camera_project(square_3D, camera)
    image_projective = 255 * np.ones(shape=[camera.height, camera.width, 3], dtype=np.uint8)

    ############### DRAW CUBE #####################
    #Bottom square
    cv2.line(image_projective, (square_2D[0][0], square_2D[0][1]), (square_2D[1][0], square_2D[1][1]), (211, 0, 148), 3)
    cv2.line(image_projective, (square_2D[1][0], square_2D[1][1]), (square_2D[2][0], square_2D[2][1]), (211, 0, 148), 3)
    cv2.line(image_projective, (square_2D[2][0], square_2D[2][1]), (square_2D[3][0], square_2D[3][1]), (211, 0, 148), 3)
    cv2.line(image_projective, (square_2D[3][0], square_2D[3][1]), (square_2D[0][0], square_2D[0][1]), (211, 0, 148), 3)
    
    #Top square
    cv2.line(image_projective, (square_2D[4][0], square_2D[4][1]), (square_2D[5][0], square_2D[5][1]), (211, 0, 148), 3)
    cv2.line(image_projective, (square_2D[5][0], square_2D[5][1]), (square_2D[6][0], square_2D[6][1]), (211, 0, 148), 3)
    cv2.line(image_projective, (square_2D[6][0], square_2D[6][1]), (square_2D[7][0], square_2D[7][1]), (211, 0, 148), 3)
    cv2.line(image_projective, (square_2D[7][0], square_2D[7][1]), (square_2D[4][0], square_2D[4][1]), (211, 0, 148), 3)
    
    #Sides square
    cv2.line(image_projective, (square_2D[0][0], square_2D[0][1]), (square_2D[4][0], square_2D[4][1]), (211, 0, 148), 3)
    cv2.line(image_projective, (square_2D[1][0], square_2D[1][1]), (square_2D[5][0], square_2D[5][1]), (211, 0, 148), 3)
    cv2.line(image_projective, (square_2D[2][0], square_2D[2][1]), (square_2D[6][0], square_2D[6][1]), (211, 0, 148), 3)
    cv2.line(image_projective, (square_2D[3][0], square_2D[3][1]), (square_2D[7][0], square_2D[7][1]), (211, 0, 148), 3)
    
    cv2.imshow("Image", image_projective)
    cv2.waitKey(0)
##############################################################################################################
#### Pontificia Universidad Javeriana, Sede Bogota.                    #######################################
#### Authors: Juan Henao & Marian Fuentes. - Proc. de imagenes y video #######################################
#### Source(s): Cv2 Documentation, Julian Quiroga Phd                  #######################################
##############################################################################################################