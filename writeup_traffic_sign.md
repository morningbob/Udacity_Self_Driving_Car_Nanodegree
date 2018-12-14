# **Traffic Sign Recognition** 

## Writeup

---

**Build a Traffic Sign Recognition Project**

The goals / steps of this project are the following:
* Load the data set (see below for links to the project data set)
* Explore, summarize and visualize the data set
* Design, train and test a model architecture
* Use the model to make predictions on new images
* Analyze the softmax probabilities of the new images
* Summarize the results with a written report


[//]: # (Image References)

[image1]: ./signs_chart.jpg "Visualization"
[image4]: ./stop3.jpg "Traffic Sign 1"
[image5]: ./uneven_road.jpg "Traffic Sign 2"
[image6]: ./turn_right3.jpg "Traffic Sign 3"
[image7]: ./stright.jpg "Traffic Sign 4"
[image8]: ./yield.jpg "Traffic Sign 5"

## Rubric Points
### Here I will consider the [rubric points](https://review.udacity.com/#!/rubrics/481/view) individually and describe how I addressed each point in my implementation.  

---
### Writeup / README


### Data Set Summary & Exploration

#### 1. Provide a basic summary of the data set. In the code, the analysis should be done using python, numpy and/or pandas methods rather than hardcoding results manually.

I used the numpy library to calculate summary statistics of the traffic
signs data set:

* The size of training set is 34799
* The size of the validation set is 4410
* The size of test set is 12630
* The shape of a traffic sign image is (32, 32, 3)
* The number of unique classes/labels in the data set is 43

#### 2. Include an exploratory visualization of the dataset.

Here is an exploratory visualization of the data set. It is a bar chart showing the number of images for each sign in the training set.

![Signs distribution][image1]


### Design and Test a Model Architecture

#### 1. Describe how you preprocessed the image data. What techniques were chosen and why did you choose these techniques? Consider including images showing the output of each preprocessing technique. Pre-processing refers to techniques such as converting to grayscale, normalization, etc. (OPTIONAL: As described in the "Stand Out Suggestions" part of the rubric, if you generated additional data for training, describe why you decided to generate additional data, how you generated the data, and provide example images of the additional data. Then describe the characteristics of the augmented training set like number of images in the set, number of images for each class, etc.)


I don't grayscale the images because I think color is important information for the model to recognize traffic signs. 

For preprocessing, I choose to normalize and augment the images.  I normalize the images by subtracting 128 and then dividing by 128.

I choose to use keras' preprocessing image data generator to augment the images, by zooming the images up to 10 degrees.  You might think I augment the images just in one way is not enough.  But by doing experiments, I found out that if I augment the images in too many ways, the validation loss increases more than the training loss.  In the other words, if I augment the images too much, the model tends to overfit too much.  


#### 2. Describe what your final model architecture looks like including model type, layers, layer sizes, connectivity, etc.) Consider including a diagram and/or table describing the final model.

My final model consisted of the following layers:

| Layer         		|     Description	        					| 
|:---------------------:|:---------------------------------------------:| 
| Input         		| 32x32x3 RGB image   							| 
| Convolution 5x5     	| 1x1 stride, valid padding, outputs 28x28x8 	|
| RELU					| Activation									|
| Max pooling	      	| 2x2 stride,  outputs 14x14x8 					|
| Convolution 5x5	    | 1x1 stride, valid padding, outputs 10x10x16 	|
| RELU					| Activation									|
| Max pooling	      	| 2x2 stride,  outputs 5x5x16   				|
| Fully connected		| input = 400, output = 100   					|
| RELU					| Activation									|
| Fully connected		| input = 100, output = 43						|
| Softmax				| turn to 0 - 1      							|
|						|												|
|						|												|
 


#### 3. Describe how you trained your model. The discussion can include the type of optimizer, the batch size, number of epochs and any hyperparameters such as learning rate.

I use Adam Optimizer.  It is good at image type classification.  I use a moderate learning rate of 0.001 with 17 epochs.  
Since I use 0.001 learning rate, I also choose a moderate batch size of 64.  

#### 4. Describe the approach taken for finding a solution and getting the validation set accuracy to be at least 0.93. Include in the discussion the results on the training, validation and test sets and where in the code these were calculated. Your approach may have been an iterative process, in which case, outline the steps you took to get to the final solution and why you chose those steps. Perhaps your solution involved an already well known implementation or architecture. In this case, discuss why you think the architecture is suitable for the current problem.

My final model results were:
* training set accuracy of 99.9%
* validation set accuracy of 96.8%
* test set accuracy of 95.7%


I choose to use LeNet model architecture to solve this problem.  It applies convolution layers, maxpooling, and fully connected layers.
It is good for the task because convolution layers is good at capturing images features.  Maxpooling layers reduce the complexity and
improve regularization.

At first, I apply 2 layers convolution layers and three fully connected layers, with 18 filters in the first layer and 54 filters in 
the second layer.  The training accuracy increases a lot, and very fast, but the validation accuracy increase very slowly and further
from the training accuracy.  Obviously, the model is overfitted.  

Then, I remove 1 fully connected layer and reduce my number of parameters, to 8 filters in the first layer and 16 filters in the 
second layer.  I also apply dropout to the fully connected layer 1.  The spread between training accuracy and validation accuracy improves but still wide.  Then, I cut almost all the augmentation of images except for zooming.  The spread between training accuracy and 
validation accuracy narrows and become acceptable.  The spread is around 3%.  The final testing accuracy is 95.7%.

### Test a Model on New Images

#### 1. Choose five German traffic signs found on the web and provide them in the report. For each image, discuss what quality or qualities might be difficult to classify.%

Here are five German traffic signs that I found on the web:

![Stop][image4] ![Bumpy road][image5] ![Turn right][image6] 
![Go straight or right][image7] ![Yield][image8]


#### 2. Discuss the model's predictions on these new traffic signs and compare the results to predicting on the test set. At a minimum, discuss what the predictions were, the accuracy on these new predictions, and compare the accuracy to the accuracy on the test set (OPTIONAL: Discuss the results in more detail as described in the "Stand Out Suggestions" part of the rubric).
					
Here are the results of the prediction:

| Image					|     Prediction								| 
|:---------------------:|:---------------------------------------------:| 
| Stop   				| Stop 											| 
| Bumpy road     		| Traffic signals 								|
| Turn right			| Ahead only									|
| Go straight or right	| Go straight or right			 				|
| Yield					| Yield										 	|


The model was able to correctly guess 3 out of the 5 traffic signs, which gives an accuracy of 60%.  The test accuracy is better than 
the web images' accuracy.  

Maybe it is because the web images has varied resolutions and shapes.  My scaling might not well transformed the images.  For example, the 
bumpy road image (image 2) has a rectangle shape, but I rescale it to square shape of (32,32,3).  So, it is more difficult for the 
model to classify this image.  

On the other hand, the images I found in the web may be a little different from actual German's traffic signs.

It might be particularly difficult to classify bumpy road sign, since the top 5 proabilities the model shows, doesn't include the
correct sign at all.  I think it is because the bumpy road sign is so not obvious in nature relative to the other signs.  
I might need more images of the bumpy road sign and one more convolution layer to capture the features.

The model is very certain about the first image, is a stop sign, with a very high softmax probability.

The second image is a bumpy road sign.  The model cannot predict the correct class, the correct class is not in the five top
probabilities.  Even worse, it is 96.4% sure that it is a traffic signals sign.

The third image is a turn right sign.  It has the same problem as the bumpy sign because it is rectanglar, and was rescaled to square.
However, the model predicts the correct sign in the second high probability, with a relatively low confidence (low probability).

The fourth image is a go straight or right sign.  The model is pretty certain about the prediction, with a 99.73 probability.  

The fifth image is a yield sign.  The model is very certain of it's prediction, with a probability of 1.






