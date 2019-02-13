
# This script is to preprocess gopro data - Version 1 - From visor/eeg prelim data -
# Will have to be adapted for the pixel-grid
# shape detection algorithms from 'https://www.pyimagesearch.com/2016/02/08/opencv-shape-detection/'

import numpy as np
import cv2
import time

def equalizeHistColor(frame):
    # equalize the histogram of color image
    img = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)  # convert to HSV
    img[:, :, 2] = cv2.equalizeHist(img[:, :, 2])  # equalize the histogram of the V channel
    return cv2.cvtColor(img, cv2.COLOR_HSV2RGB)  # convert the HSV image back to RGB format

Shape_Detect_Label = False # If True will detect and label shapes

# What file are we loading? Current webcam stream or old video file
Input_Here = False # True True if Webcam
if Input_Here == True:
    Input_File_Full_Name = 0
else:
    Input_V = '' # Version - example '001' or '054'
    Input_Base_Name = '003_camera_p3'
    Input_File_Name = Input_Base_Name + Input_V
    Input_Format = '.MP4'
    Input_File_Full_Name = Input_File_Name + Input_Format

# What are we saving the file as?
Output_V = '_001' # # Version - example '001' or '054'
Output_Base_Name = 'Testing'
Output_File_Name = Output_Base_Name + Output_V
Output_Format = '.avi'
Output_File_Full_Name = Output_File_Name + Output_Format # change the file name if needed

imgSize=(640,480)
frame_per_second=30.0

writer = cv2.VideoWriter(Output_File_Full_Name, cv2.VideoWriter_fourcc(*"MJPG"), frame_per_second,imgSize,False)

# Manipulation Variables,
kernelSize = 21 # default 21
GB_Kernel = 21 # default 21
# Edge Detection Parameter
parameter1=20
parameter2=60
intApertureSize=1
# Colours
custom_color_list = []
custom_color_list = \
    ["COLOR_BGR2RGB",
     "COLOR_RGB2BGR",
     "COLOR_BGR2GRAY",
     "COLOR_RGB2GRAY",
     "COLOR_BGR2HSV",
     "COLOR_RGB2HSV",
     "COLOR_RGB2HLS",
     "COLOR_BGR2HLS",
     "COLOR_BGR2XYZ",
     "COLOR_RGB2XYZ",
     "COLOR_BGR2Lab",
     "COLOR_RGB2Luv"]
custom_color_type = 1 # 1-12 - look at elements in custom_color_list
## frame dimensions (x,y) & img dimensions (2x,2y)
scaling_factorx=1
scaling_factory=1
scaling_factor2x=1
scaling_factor2y=1
# Thresholding
threshold1=100
threshold2=200
# Contours
color=(255,0,0)
thickness=2
count = 0

###################################################################
# First Pass
# List of [frame + start event trigger] (where the max[index] = corresponds with the last EEG event)
Trigger_Start = []
# List of [frame + end event trigger]
Trigger_Stop = []
# List of [frame + trigger state] (0 B + G channels below thresholds, 1 above B channel threshold, 2 above R channel threshold
Tigger_State = []

# Want a frame of each start trigger saved to a folder

# Second Pass for extracting epochs based off first pass - figure out later
# Eventually will output an ~[-1,1] video epoch to be the raw input for deep learning
Trigger_Epoch = []
###################################################################
###################################################################
gp_video_test = [];

#for video 0073%%%
start_eeg = 4274
off_flash = 5133
# gp_x = [280:310]
# gp_y = [290:320]

#for 003 (video 0079)%%%
#lights are off at frame 3999
#mean value of black circle is about 52.2006
start_eeg = 652
door_closed = 4800
start_flash = 8897
# gp_x = [320:500]
# gp_y = [280:380]

#for 004 (video 0080)%%%
#lights are off at frame 3999
#mean value of black circle is about 52.2006
start_eeg = 3041
door_closed = 6947
start_flash = 12159
# gp_x = [300:500]
# gp_y = [340:420]

#for 005 (video 0081)%%%
#lights are off at frame 3999
#mean value of black circle is about 52.2006
start_eeg = 3330
door_closed = 12240
start_flash = 3268+14400
# gp_x = [320:460]
# gp_y = [330:400]

#for 006 (video 0082?)%%%
#lights are off at frame 5280
#mean value of black circle is about 52.2006
start_eeg = 567
door_closed = 5040
start_flash = 10446
# gp_x = [360:500]
# gp_y = [340:385]

#for 007 (video 0083?)%%%
#lights are off at frame 5280
#mean value of black circle is about 52.2006
start_eeg = 1045
door_closed = 7440
start_flash = 12567
#off_flash =
# gp_x = [360:480]
# gp_y = [370:430]

#for 008 (video 0084?)%%%
#lights are off at frame 5280
#mean value of black circle is about 52.2006
start_eeg = 2053
door_closed = 7680
start_flash = 12673
#off_flash =
# gp_x = [380:500]
# gp_y = [385:420]

#for 009 (video 0084?)%%%
#lights are off at frame 5280
#mean value of black circle is about 52.2006
start_eeg = 616
door_closed = 6000
start_flash = 11040
# gp_x = [360:460]
# gp_y = [365:400]

#for 010 (video 0087)%%%
#lights are off at frame 5280
#mean value of black circle is about 52.2006
start_eeg = 1443
door_closed = 8640
start_flash = 13343
# gp_x = [380:500]
# gp_y = [385:420]

#for 011 (video 0088)%%%
#lights are off at frame 5280
#mean value of black circle is about 52.2006
start_eeg = 638
door_closed = 8400
start_flash = 13176
# gp_x = [390:520]
# gp_y = [330:380]

#############################################################################

cap = cv2.VideoCapture(Input_File_Full_Name)  # load the video

while (cap.isOpened()):  # play the video by reading frame by frame
    ret, frame = cap.read()
    if ret == True:
        # equalize the histogram of color image - contrast enhancement
        frame1 = equalizeHistColor(frame)

        # Smoothing
        gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (GB_Kernel, GB_Kernel), 0)

        # Thresholding
        # ret, mask = cv2.threshold(blur, threshold1, threshold2, cv2.THRESH_BINARY)
        # ret, mask = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # ret, mask = cv2.threshold(blur,threshold1, threshold2,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        mask = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
        # mask = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=7)  # morphology erosion
        mask = cv2.dilate(mask, kernel, iterations=5)  # morphology dilation

        mask_inv = cv2.bitwise_not(mask)
        img = cv2.bitwise_and(frame1, frame1, mask=mask_inv)
        img = cv2.addWeighted(frame1, 0.1, img, 0.9, 0)

        #Contouring - includes a bounding box - takes from previous gray box
        ret, thresh = cv2.threshold(gray, 75, 100, cv2.THRESH_BINARY_INV)
                                                            # RETR_EXTERNAL #cv2.CHAIN_APPROX_SIMPLE
        img1, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        if len(contours) != 0:
            c = max(contours, key=cv2.contourArea)  # find the largest contour
            x, y, w, h = cv2.boundingRect(c)  # get bounding box of largest contour
            img2=cv2.drawContours(img, c, -1, color, thickness) # draw largest contour
            # img2 = cv2.drawContours(frame, contours, -1, color, thickness)  # draw all contours
            img3 = cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 255), 2)  # draw red bounding box in img
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img3, "label", (x, h), font, 1,(255,255,255),2)
        ###################################################################


        if Shape_Detect_Label:
            shape = "unidentified"
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.04 * peri, True)

            # if the shape is a triangle, it will have 3 vertices
            if len(approx) == 3:
                shape = "triangle"

            # if the shape has 4 vertices, it is either a square or
            # a rectangle
            elif len(approx) == 4:
                # compute the bounding box of the contour and use the
                # bounding box to compute the aspect ratio
                (x, y, w, h) = cv2.boundingRect(approx)
                ar = w / float(h)

                # a square will have an aspect ratio that is approximately
                # equal to one, otherwise, the shape is a rectangle
                shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"

            # if the shape is a pentagon, it will have 5 vertices
            elif len(approx) == 5:
                shape = "pentagon"

            # otherwise, we assume the shape is a circle
            else:
                shape = "circle"

            for c in cnts:
                # compute the center of the contour, then detect the name of the
                # shape using only the contour
                M = cv2.moments(c)
                cX = int((M["m10"] / M["m00"]) * ratio)
                cY = int((M["m01"] / M["m00"]) * ratio)
                shape = sd.detect(c)

                # multiply the contour (x, y)-coordinates by the resize ratio,
                # then draw the contours and the name of the shape on the image
                c = c.astype("float")
                c *= ratio
                c = c.astype("int")
                cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
                cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 255, 255), 2)

                for c in cnts:
                    # compute the center of the contour, then detect the name of the
                    # shape using only the contour
                    M = cv2.moments(c)
                    cX = int((M["m10"] / M["m00"]) * ratio)
                    cY = int((M["m01"] / M["m00"]) * ratio)
                    shape = sd.detect(c)

                    # multiply the contour (x, y)-coordinates by the resize ratio,
                    # then draw the contours and the name of the shape on the image
                    c = c.astype("float")
                    c *= ratio
                    c = c.astype("int")
                    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
                    cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (255, 255, 255), 2)

        #####################################################################
        # List of [frame + start event trigger] (where the max[index] = corresponds with the last EEG event)
        if Trigger_Start = []
        # List of [frame + end event trigger]
        if Trigger_Stop = []
        # List of [frame + trigger state] (0 B + G channels below thresholds, 1 above B channel threshold, 2 above R channel threshold
        if Tigger_State = []
        else

        writer.write(img)  # save the frame into video file
        count += 1
        if count % 1 == 0:
            # cv2.imshow('Original', frame)  # show the original frame
            cv2.imshow('New', img) #show the new frame
        if cv2.waitKey(1)& 0xFF == ord('q'):
            break
    else:
        print("ref != True")
        break
    # When everything done, release the capture
writer.release()
cap.release()
cv2.destroyAllWindows()