# **Finding Lane Lines on the Road** 

## Finding Lane Lines Project Writeup

### You can use this file as a template for your writeup if you want to submit it as a markdown file. But feel free to use some other method and submit a pdf if you prefer.

---

**Finding Lane Lines on the Road**

The goal of this project is to Make a pipeline that finds lane lines on the road.


[//]: # (Image References)

[image1]: ./examples/grayscale.jpg "Grayscale"

---

### Reflection

### 1. Describe my pipeline. 


My pipeline consisted of 5 steps. First, I converted the images to grayscale, then, I applied Gaussian Blur to 

get rid of insignificant details.  I applied Canny function to detect edges.  After that, I define the region 

of interest to get rid of irrelevant edges.  Finally, I applied Hough transform to make the lane lines clear
 
and draw them.


In order to draw a single line on the left and right lanes, I modified the draw_lines() function.  

I calculated each line's slope and classified them to left lane lines if the slope is positive and 

to right lane lines if the slope is negative.  Then, I averaged the lanes' slopes in order to get the 

accurate slope of each lane.  I randomly chose a point on the left lane and extrapolated it with the left

lane's average slope, to draw the left lane line from an estimated height denote the begining of the lane to 

the bottom edge of the image.  I did the same to the right lane.     



![alt text][image1]


### 2. Identify potential shortcomings with my current pipeline


One potential shortcoming would be what would happen when the estimated begining of the lane lines changed.

For example, if the car is climbing a hill, the estimated begining point will be lower.  The pipeline has

this estimated height fixed.  That will result in inaccurate lane line detection.


By assuming the lane lines straight, I only extrapolated the lines by using one average slope.  If the lanes 

are curved, not straight, the lines drawn would be very inaccurate.


Besides, sometimes there might be no lane lines in a segment of the road.  I didn't provide an estimated 

lane lines for the reference of the car.  The car might get lost. 


Finally, the pipeline was not tested by a night time video.  Maybe grayscaling the image won't work at 

night.





### 3. Possible improvements to my pipeline


A possible improvement would be to replace the fixed estimated begining height of the lanes by the minimum y

coordinates from the points of both lines.  That would fix the point one shortcoming I mentioned above.


Another potential improvement could be to extrapolate several segments of different slopes of the lane lines.

This would make the lines drawn fit more to the actual lane lines when they are curved, not straight.


Moreover, I could keep the history of the lane lines drawn.  When the lane lines were not detected in

the image, I could use the recent few lane lines coordinates to provide an estimate of the current lane lines.

This was because, the lane lines wouldn't change a lot suddenly.



