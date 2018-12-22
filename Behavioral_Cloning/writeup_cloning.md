# **Behavioral Cloning** 

## Writeup Template

---

**Behavioral Cloning Project**

The goals / steps of this project are the following:
* Use the simulator to collect data of good driving behavior
* Build, a convolution neural network in Keras that predicts steering angles from images
* Train and validate the model with a training and validation set
* Test that the model successfully drives around track one without leaving the road
* Summarize the results with a written report


[//]: # (Image References)

[image1]: ./center.jpg "Center lane driving"
[image2]: ./off_side.jpg "Driving off side"
[image3]: ./recovery1.jpg "Recovery Image"
[image4]: ./recovery2.jpg "Recovery Image"
[image5]: ./before_flip.jpg "Image before flipping"
[image6]: ./after_flip.jpg "Image after flipping"



## Rubric Points
### Here I will consider the [rubric points](https://review.udacity.com/#!/rubrics/432/view) individually and describe how I addressed each point in my implementation.  

---
### Files Submitted & Code Quality

#### 1. Submission includes all required files and can be used to run the simulator in autonomous mode

My project includes the following files:
* model.py containing the script to create and train the model
* drive.py for driving the car in autonomous mode
* model.h5 containing a trained convolution neural network 
* writeup_report.md summarizing the results

#### 2. Submission includes functional code
Using the Udacity provided simulator and my drive.py file, the car can be driven autonomously around the track by executing 
```sh
python drive.py model.h5
```

#### 3. Submission code is usable and readable

The model.py file contains the code for training and saving the convolution neural network. The file shows the pipeline I used for training and validating the model, and it contains comments to explain how the code works.

### Model Architecture and Training Strategy

#### 1. An appropriate model architecture has been employed

My model consists of one convolution layer, followed by one maxpooling layer, another convolution layer, followed by another maxpooling layer, and then it has two fully connected layers.

The two convolution layers has 5x5 filter sizes and depths between 15 and 50.  I used RELU layers after the convolution layers and fully connected layers, to introduce nonlinearity.

The images were cropped from the top for 50 pixels and the bottom for 20 pixels.  The sky and the bottom blur area are not relevant to the task.  The data was also normalized in the model using a Keras lambda layer.  

#### 2. Attempts to reduce overfitting in the model

The model has two maxpooling layers to reduce overfitting.  It also has one dropout layer after the first fully connected layer to reduce overfitting. 

The model was trained and validated on track one and track two data sets to ensure that the model was not overfitting. The model was tested by running it through the simulator and ensuring that the vehicle could stay on the track.

#### 3. Model parameter tuning

The model used an adam optimizer, with a learning rate of 0.00003 and a batch size of 64 for 1 epochs.

#### 4. Appropriate training data

Training data was chosen to keep the vehicle driving on the road. I used a combination of center lane driving, recovering from the left and right sides of the road.

I also used the left and right camera's images, adjusted the steering measurement because of different angles.  So, the model has more data for training and estimate curved lanes more accurately.  The steering measurement adjustments were estimated through training experiments.

For details about how I created the training data, see the next section. 

### Model Architecture and Training Strategy

#### 1. Solution Design Approach

The overall strategy for deriving a model architecture was to use deep learning to clone the human driving behaviour to drive a car.  That involved providing images of road conditions and steering measurements of a human driving a car, to the model.  The idea of the how the model learns would be, seeing an image (the input X) and a corresponding steering measurement (the label).  After training a number of images, the model should be able to predict the steering measurement given an image.  

My first step was to use a convolution neural network model similar to the LeNet model.  I thought this model might be appropriate because it deals with images with high accuracy.  I tried to use three convolution layers and three fully connected layers.  For the details architecture of the model, please refer to the above section, point 1.

In order to gauge how well the model was working, I split my image and steering angle data into a training and validation set. I found that my first model has a low mean square training error but a relatively higher validation error.  Both the training and validation accuracies were around 0.05.  But I decided that I wouldn't focus on accuracies because the nature of the task was not to produce an number matching steering angle.  Instead, I would focus on the low mean square error because we need close approximates.  

Since the validation error is relatively high.  This implied that the model was overfitting.  Then, I remove one convolution layer and one fully connected layer.  I also add a dropout layer in the first fully connected layer.  

The final step was to run the simulator to see how well the car was driving around track one. There were a few spots where the vehicle fell off the track.  Then, I recorded some images of the car recovering to the center from the left side and right side, from both tracks.  I ran the simulator again.  It's behavior improved.

At the end of the process, the vehicle is able to drive autonomously around the track without leaving the road.  I included recordings of both tracks.

#### 2. Final Model Architecture


Here is a visualization of the architecture 

My final model consisted of the following layers:

| Layer         		|     Description	        					| 
|:---------------------:|:---------------------------------------------:| 
| Input 				| 160x320x3 RGB image  							| 
| Cropping 				| 90x320x3 RGB image  							| 
| Convolution 5x5     	| 1x1 stride, same padding, outputs 90x320x15 	|
| RELU					| Activation									|
| Max pooling	      	| 2x2 stride,  outputs 45x160x15 				|
| Convolution 5x5	    | 1x1 stride, same padding, outputs 45x160x50 	|
| RELU					| Activation									|
| Max pooling	      	| 2x2 stride,  outputs 22x80x50   				|
| Fully connected		| input = 500, output = 50   					|
| RELU					| Activation									|
| Fully connected		| input = 50, output = 1						|
|						|												|
|						|												|


#### 3. Creation of the Training Set & Training Process

To capture good driving behavior, I used the provided images on track one using center lane driving. Here is an example image of center lane driving:

![center lane driving][image1]

I then recorded the vehicle recovering from the left side and right sides of the road back to center so that the vehicle would learn to recover to the center if it gets to the side.  These images show what a recovery looks like.

![got off side][image2]
![recovering 1][image3]
![recovering 2][image4]

Then I repeated this process on track two in order to get more data points.

To augment the data sat, I also flipped images and angles thinking that this would remove the left lane driving bias because it is a round track.  For example, here is an image that has then been flipped:

![image before flipping][image5]
![flipped image][image6]

I also used the left and right camera's images.  I adjusted the steering angles by a correction of 0.05 and -0.05 for left and right images.  Then, the model has more images for training.


After the collection and augumentation, I had 67872 number of data points.    

I finally randomly shuffled the data set and put 25% of the data into a validation set. 

I used this training data for training the model.  The validation set helped determine if the model was over or under fitting. The ideal number of epochs was 1 as evidenced by a small training and validation number 0.01 and 0.0248.  I used an adam optimizer with a small learning rate of 0.00003, with a small batch size of 64.
