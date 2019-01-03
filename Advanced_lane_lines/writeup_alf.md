## Advanced Lane Finding Project Writeup

---

**Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./output_images/calibration1.jpg "distorted"
[image2]: ./output_images/undistort.jpg "undistorted"
[image3]: ./output_images/test5.jpg "test image"
[image4]: ./output_images/undistorted_test5.jpg "undistorted test image"
[image5]: ./output_images/straight_lines1.jpg "before binary"
[image6]: ./output_images/binary_image.jpg "Binary Image"
[image7]: ./output_images/after_hough.jpg "After applying hough"
[image8]: ./output_images/warped_image.jpg "Perspective Transform"
[image9]: ./output_images/result.jpg "Video"
[video1]: ./project_output.mp4 "Video"


## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

### All the code and functions I defined, are located in the jupyter notebook ALF.ipynb.


### Camera Calibration

#### 1. Briefly state how I computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.


I use chessboard images from the camera_cal folder to do calibration.  The chessboard has a 9 x 6 dimension.  Firstly, I turn the image into grayscale.  Then, I use opencv's findChessboardCorners() function to find the corners for the images.  The corners are stored in the imgpoints array which I use to calibrate the camera.  From opencv's calibrateCamera function, I got the camera matrix and distortion coefficients that I can use to undistort the images.  Here I show one of the distorted image and it's corresponding undistorted image:  

![before undistortion][image1]
![after undistortion][image2]



### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.

To demonstrate this step, I will describe how I apply the distortion correction to one of the test images like this one:
![before undistortion][image3]


I use the opencv's undistort() function, with the camera matrix and distortion coefficients, to undistort the images, that are from the video I need to process.

Here I have the image from the test folder to show the distortion correction:
![after undistortion][image4]


#### 2. Describe how I used color transforms, gradients to create a thresholded binary image.  Provide an example of a binary image result.


I choose one of the image from the test folder to be the model for testing out the effectiveness of my pipeline.  In order to highlight the lanes of the road, I apply sobelx filter to the image.  It helps highlighting the vertical lines of the image.  I also change the image's color space to HLS and see the effects on each of the H, L and S channel.  The S channel highlights the lanes the best.  

I combined sobelx and S channel effects to produced the binary image as follows:
![before processing][image5]
![binary image][image6]


#### 3. Describe how I performed a perspective transform and provide an example of a transformed image.


In order to estimate the source points (the four points on the original image that denote the area to be tranformed) and destination points (the four points on the target image that denote the area the source points should occupy), I use some helper functions from project 1.  I hand pick the minimum and maximum y coordinates to be [435, 720]  Firstly, I use the region of interest function to show only the lane part of the image.  Then, I use hough lines function with the draw lines function, to try to show and connect the segmented lane lines.  As shown here:  
![after hough][image7]

From the draw lines function, I output some points and slopes of the lanes, so that I can calculate the source points coordinates.  Then, I hand pick the destination points coordinates.  

| Source        | Destination   | 
|:-------------:|:-------------:| 
| 624, 470      | 280, 0        | 
| 656, 470      | 1000, 0       |
| 1100, 719     | 1000, 720     |
| 203, 719      | 280, 720      |

I apply the perspective transform to the image:
![warped image][image8]


#### 4. Describe how I identified lane-line pixels and fit their positions with a polynomial


I draw histogram to identify the 2 lane lines' x coordinates.  I stack sliding windows from the bottom to cover the lanes.  Then, I identify the nonzero pixels in x and y within the window and save them in 2 lists.  I fit a second order polynomial to each list using `np.polyfit`.  The result is as follows:

Then, I test a function which search around the last successful fit with a margin, to produce a current fit.  The function's name is search_around_poly.  Given a binary image and the last successful fit, the function is able to produce the new fit with much shorter time because it mainly search around the past fit.  

If I found out that there is no lane pixels detected from the search_around_poly method for the left or the right lane, I discard the current frame and use the previous frame's information.

Moreover, I also check that if the lanes are in similar place compare to the lanes in the last frame.  If any of the lane's position different very much from the last frame's lanes, I also discard the image.

#### 5. Describe how I calculated the radius of curvature of the lane and the position of the vehicle with respect to center.


Firstly, I decide the y-value, which is the bottom of the image 719.  I can evaluate the formula of the radius of curvature at the y-value, with the polynomial I fitted above.  I get the radius in pixels.  But I need the real world radius of curvature.  Then, I scale the pixel to meters (3.7 meters per 700 x pixels, and 30 meters per 720 y pixels), refit it with respect to center position.  I substitute it to the radius formula again and get the real world radius of curvatures.

If I detected any lane's curvature smaller than 600 meters, I discard the current frame and use the previous frame's information.


#### 6. Provide an example image of my result plotted back down onto the road such that the lane area is identified clearly.


I create an image to draw the green plane of road area.  I use opencv's fillPoly() to draw according to the fit points.  Then, I use the inverse perspective matrix to convert the image to the perspective of the original image as follows:

![final result][image9]

---

### Pipeline (video)

#### 1. Provide a link to my final video output.  

Here's a [link to my video result](./project_output.mp4)


---

### Discussion

#### 1. Briefly discuss any problems / issues I faced in my implementation of this project.  Where will my pipeline likely fail?  What could I do to make it more robust?


The major problem of my pipeline is that I hardcore the y coordinate of the upper end of the lanes (that is the middle of the image).  If the car is driving uphill or downhill, that y coordinate will be changed.  The program will not worked as expected.  This y coordinate should be automically detected, instead of hardcored.  

The other major problem is that I also hardcore the source points for the perspective transform.  I use one of the test image to calculate t the source points.  If the width of the road change later, the lanes detection won't be accurate too.  Ideally, the source points should be automatically detected once in awhile.

Besides, in my lanes detection, the green area is not very accurate at the end of the lanes.  I think if I average the results calculate from several images, it will make the detection more stable and fluent.

On the other hand, changing lanes are common in car driving.  However, my pipeline didn't consider that.  It will probably detect the new lanes "after" the changing lane action is completed.  But it won't detect the lanes "during" the changing lane action.  

Finally, the pipeline is not tested on videos if there are cars in the front.  I don't know it the pipeline still work in this condition.  The pipeline probably has problems in this case.  I need to consider that too.
