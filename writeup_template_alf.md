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
[image2]: ./output_images/undistorted.jpg "undistorted"
[image3]: ./output_images/test5.jpg "test image"
[image4]: ./output_images/undistorted_test5.jpg "undistorted test image"
[image5]: ./output_images/straight_lines1.jpg "before binary"
[image6]: ./output_images/binary_image.jpg "Binary Image"
[image7]: ./output_images/after_hough.jpg "After applying hough"
[image8]: ./output_images/warped_image.jpg "Perspective Transform"
[image9]: ./output_images/result.jpg "Video"
[image10]: ./project_video.mp4 "Video"

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

### All the code and functions I defined, are located in the jupyter notebook ALF.ipynb.


### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.


I start by preparing "object points", which will be the (x, y, z) coordinates of the chessboard corners in the world. Here I am assuming the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image.  Thus, `objp` is just a replicated array of coordinates, and `objpoints` will be appended with a copy of it every time I successfully detect all chessboard corners in a test image.  `imgpoints` will be appended with the (x, y) pixel position of each of the corners in the image plane with each successful chessboard detection.  

I then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  I applied this distortion correction to the test image using the `cv2.undistort()` function and obtained this result: 


![alt text][image1]

MY ANSWER:

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


#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

I used a combination of color and gradient thresholds to generate a binary image (thresholding steps at lines # through # in `another_file.py`).  Here's an example of my output for this step.  (note: this is not actually from one of the test images)

![alt text][image3]

I choose one of the image from the test folder to be the model for testing out the effectiveness of my pipeline.  In order to highlight the lanes of the road, I apply sobelx filter to the image.  It helps highlighting the vertical lines of the image.  I also change the image's color space to HLS and see the effects on each of the H, L and S channel.  The S channel highlights the lanes the best.  

I combined sobelx and S channel effects to produced the binary image as follows:
![before processing][image5]
![binary image][image6]


#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The code for my perspective transform includes a function called `warper()`, which appears in lines 1 through 8 in the file `example.py` (output_images/examples/example.py) (or, for example, in the 3rd code cell of the IPython notebook).  The `warper()` function takes as inputs an image (`img`), as well as source (`src`) and destination (`dst`) points.  I chose the hardcode the source and destination points in the following manner:

```python
src = np.float32(
    [[(img_size[0] / 2) - 55, img_size[1] / 2 + 100],
    [((img_size[0] / 6) - 10), img_size[1]],
    [(img_size[0] * 5 / 6) + 60, img_size[1]],
    [(img_size[0] / 2 + 55), img_size[1] / 2 + 100]])
dst = np.float32(
    [[(img_size[0] / 4), 0],
    [(img_size[0] / 4), img_size[1]],
    [(img_size[0] * 3 / 4), img_size[1]],
    [(img_size[0] * 3 / 4), 0]])
```

This resulted in the following source and destination points:

| Source        | Destination   | 
|:-------------:|:-------------:| 
| 585, 460      | 320, 0        | 
| 203, 720      | 320, 720      |
| 1127, 720     | 960, 720      |
| 695, 460      | 960, 0        |

I verified that my perspective transform was working as expected by drawing the `src` and `dst` points onto a test image and its warped counterpart to verify that the lines appear parallel in the warped image.

![alt text][image4]

In order to estimate the source points (the four points on the original image that denote the area to be tranformed) and destination points (the four points on the target image that denote the area the source points should occupy), I use some helper functions from project 1.  I hand pick the minimum and maximum y coordinates to be [435, 720]  Firstly, I use the region of interest function to show only the lane part of the image.  Then, I use hough lines function with the draw lines function, to try to show and connect the segmented lane lines.  As shown here:  
![after hough][image7]

From the draw lines function, I output some points and slopes of the lanes, so that I can calculate the source points coordinates.  Then, I hand pick the destination points coordinates.  

| Source        | Destination   | 
|:-------------:|:-------------:| 
| 624, 435      | 280, 0        | 
| 656, 435      | 1000, 0       |
| 1100, 719     | 1000, 720     |
| 203, 719      | 280, 720      |

I apply the perspective transform to the image:
![warped image][image8]


#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

Then I did some other stuff and fit my lane lines with a 2nd order polynomial kinda like :

![alt text][image5]

I draw histogram to identify the 2 lane lines' x coordinates.  I stack sliding windows from the bottom to cover the lanes.  Then, I identify the nonzero pixels in x and y within the window and save them in 2 lists.  I fit a second order polynomial to each list using `np.polyfit`.  The result is as follows:

Then, I test a function which search around the last successful fit with a margin, to produce a current fit.  The function's name is search_around_poly.  Given a binary image and the last successful fit, the function is able to produce the new fit with much shorter time because it mainly search around the past fit.  

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

I did this in lines # through # in my code in `my_other_file.py`

Firstly, I decide the y-value, which is the bottom of the image 719.  I can evaluate the formula of the radius of curvature at the y-value, with the polynomial I fitted above.  I get the radius in pixels.  But I need the real world radius of curvature.  Then, I scale the pixel to meters (3.7 meters per 700 x pixels, and 30 meters per 720 y pixels), refit it with respect to center position.  I substitute it to the radius formular again and get the real world radius of curvatures.

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

I implemented this step in lines # through # in my code in `yet_another_file.py` in the function `map_lane()`.  Here is an example of my result on a test image:

![alt text][image6]

I create an image to draw the green plane of road area.  I use opencv's fillPoly() to draw according to the fit points.  Then, I use the inverse perspective matrix to convert the image to the perspective of the original image as follows:

![final result][image9]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](./project_video.mp4)


---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

Here I'll talk about the approach I took, what techniques I used, what worked and why, where the pipeline might fail and how I might improve it if I were going to pursue this project further.  
