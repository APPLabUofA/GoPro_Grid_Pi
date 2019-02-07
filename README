# Pi/GoPro study
__Hardware__
Can I get a prototype box from the shop? 
Ready to build V1
Using a - 74AHCT125  level converter chip (allows for safe 3V and 5V connections)
Need two power sources - one for grid - AA batteries + power bank for running Pi
Still not sure how to work button into setup, playing with, but not sure how to align with video and eeg streams. 
Because normally we auto-run pi based on the booting as power is supplied. 
Should we have a condition where the experiment is run on the old system with embedded triggers?

Room lighting in the VR room?

Analysis
Challenging myself to have everything within python
Base Video Processing Components
Trim Start
Gaussian Blur
Thresholding 

__Outputs__
List of [frame + start event trigger] (where the max[index] = corresponds with the last EEG event)
List of [frame + end event trigger]
List of [frame + trigger state] (0 B + G channels below thresholds, 1 above B channel threshold, 2 above R channel threshold

Eventually will output an ~[-1,1] video epoch to be the raw input for deep learning

	Base EEG Processing Components
		Trial Rejections (blink + wrong response, noise)
		High/Low filtering
		Compression/Contraction
ERPs

V1-V4 
V1 Stationary Viewer + Stationary Light Grid (0, 0) (whole grid dimly lit) - GoPro + Pi (+ Button?)

Video Analysis
Basic Geometric classifiers (cv2.PolyApprox)
Once contour is identified - constructing RBG into separate channels - using dynamic thresholding of Blue and Green channels ratioed to background lighting (RBG Channeling)
EEG Analysis 
	
V2 Stationary Viewer + Moving grid  (0, xy) (one bright light) - GoPro + Pi 
			Video Analysis
Basic Object Contour Tracking (Motion Detection by Image Difference)
Basic Geometric classifiers (cv2.PolyApprox) within bounded contours (circles)
Or 
Hough Circle Detection
	RGB Channeling within circle detection
			EEG Analysis				

V3 Stationary Viewer + Moving grid (0, xz+rot.)  - GoPro + Pi (+Eye Tracking? + Button?)
Video Analysis 
Background/Foreground separation
Object Tracking
Perspective Transformation
Occlusion Procedure
EEG Analysis

V4 Moving Perspective + Moving Grid (xz+rot. + xz+rot.) GoPro + Pi + Eye Tracking (+ Button?)
	Video Analysis
		Preprocessing
Optic flow channels
Analysis
	Object specific YOLOv3 Classifications
			EEG Analysis 
Deep Learning with multimodal inputs of EEG and video YOLOv3 output 

Hardware
Problem of attaching so much hardware to the head? - Need a ergonomic solution, cushioned helmet on top of EEG? 
Camera array
Eye Tracking
2 Raspberry Pis (use zero Ws)
2 gopros
button
Laser Depth Camera?
Intel realsense camera - 2 RBG cameras + fisheye camera + infrared projector and infrared camera
Works on Windows as long as you have USB 3.0 
			
Software


Analysis
80% switched over to python already, some trouble experienced with uploading the default MP4 file format - been using avi. - looking into RAW files

Stills
Working on the next steps of YOLO opencv integration for classification + object tracking
Think at this point we should have eye tracking on hand - for the sake of developing a complete product
