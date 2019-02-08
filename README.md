# GoPro_Eye_Pi study
## Pressing Questions
VR room lighting characteristics?
Should we have a condition where the experiment is run on the old system with embedded triggers?
Heat Sinks (2-4) GPU/CPU

## Hardware
**What we will need short-term**
- At this point we may want to have a cheap eye tracking system on hand - for the sake of developing a complete product

**What we will need long-term**
- USB to MicroUSB
- Microusb to AUX (3.5mm)
- Eye Tracking - mountable
- 2 Raspberry Pis (use zero Ws)
- 2 gopros or some alternative small high FPS/high resolution
- button
- Infrared emitter & Infrared Depth Camera for scene construction?

Possibility of using the following hardware in lieu of GoPros + Infrared hardware
	Intel realsense camera - 2 RBG cameras + fisheye camera + infrared projector and infrared camera
		Works on Windows as long as you have USB 3.0 (surface)

Problem of attaching so much hardware to the head? - Need a ergonomic solution, cushioned helmet to mount instruments on top of EEG? 
	for reproducibility we should have rig be constructed and stay the same (i.e. distance between GoPros (or other cameras) + eye 		tracking
	 
## Builds
- [ ] **V1.0** (as of Feb. 11th)
Currently using a - 74AHCT125  level converter chip (allows for safe 3V and 5V connections)
	- Neopixel python library is now CircuitPython
Two power sources - one for grid Pi + one for button Pi

Replace the 74AHCT125 IC with a diode?

To work a response button into setup the setup and allow for continued disconnection of recorder and stim, we will be using Precision Time Protocol (PCP) 

## Analysis 
(Challenging myself to have everything within python)
**Base Video Processing Components** (OpenCV)
- Trim Start
- Gaussian Blur
- Thresholding 
*Outputs*
- List of [frame + start event trigger] (where the max[index] = corresponds with the last EEG event)
- List of [frame + end event trigger]
- List of [frame + trigger state] (0 B + G channels below thresholds, 1 above B channel threshold, 2 above R channel threshold
	- Eventually will output an ~[-1,1] video epoch to be the raw input for deep learning

**Base EEG Processing Components**
- Trial Rejections (blink + wrong response, noise)
- High/Low filtering
- Compression/Contraction

*Outputs*
- ERPs

## Versions

## V1 
Stationary Viewer + Stationary Light Grid (0, 0) (whole grid dimly lit) - GoPro + Pi (+ Button?)

### Video Analysis
- Basic Geometric classifiers (cv2.PolyApprox)
	- Once contour is identified --> constructing into separate channels RGB
	- using dynamic thresholding of Blue and Green channels ratioed to background lighting (RBG Channeling)

### EEG Analysis 
	
	
## V2 
Stationary Viewer + Moving grid  (0, xy) (one bright light) - GoPro + Pi 

### Video Analysis
- Basic Object Contour Tracking (Motion Detection by Image Difference)
**and**
- Basic Geometric classifiers (cv2.PolyApprox) within bounded contours (circles)
**or**
- Hough Circle Detection

### EEG Analysis				

## V3
Stationary Viewer + Moving grid (0, xz+rot.)  - GoPro + Pi (+Eye Tracking? + Button?)
	
### Video Analysis 
- Background/Foreground separation
- Object Tracking
- Perspective Transformation
- Occlusion Procedure

### EEG Analysis

## V4
Moving Perspective + Moving Grid (xz+rot. + xz+rot.) GoPro + Pi + Eye Tracking (+ Button?)

### Video Preprocessing
- Optic flow channels
- Analysis
### Video Analysis
 - Object specific YOLOv3 Classifications

### EEG Analysis 
- Deep Learning with multimodal inputs of EEG and video YOLOv3 outputs 

		
## Software


## Analysis
80% switched over to python already, some trouble experienced with uploading the default MP4 file format - been using avi. - looking into RAW file conversion via mmfpeg-python 

## Stills
Working in my spare time the next steps of YOLO opencv integration for classification + object tracking

Test123456