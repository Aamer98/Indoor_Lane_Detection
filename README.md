# Indoor_Lane_Detection

The lanes will be marked tape of desired colour. As different parts of the tape may be lit with different light, different shades of the colour will be captured by the camera. Selecting these shades of colour in the RGB colour space is possible but will be difficult since all three parameters, i.e. red, green and blue, will change for different shades of one colour. It is extremely difficult to arbitrarily dictate how much of each primary colour composes it when looking at a particular colour. In the HSV color space, the colours (hue or tint) are described in terms of their brightness value and shade (saturation or amount of gray). The HSV color wheel always consists of these components but sometimes appears as a cylinder or cone.

![image](https://user-images.githubusercontent.com/60957986/74598521-68ac7e80-508c-11ea-86be-1b1e08b0a943.png)

In the HSV color space, the colours (hue or tint) are described in terms of their brightness value and shade (saturation or amount of gray). The HSV color wheel always consists of these components but sometimes appears as a cylinder or cone.

# HUE
Hue is one of the components of the HSV colour space and indicates the colour part of the space. It is indicated by a number in between 0 and 360 degrees.
• Between 0 and 60 degrees: Red .
• Between 61 and 120 degrees: YeIIow.
• Between 121-180 degrees: Green.
• Between 181-240 degrees: Cyan.
• Between 241-300 degrees: Blue.
• Between 301-360 degrees: Magenta.

# SATURATION

The amount of gray in a particular colour is described by the Saturation. It ranges from 0 to 100 percent. A faded effect is produced upon reducing this component towards zero as more gray is introduced. In certain cases, the saturation may be ranged from 0-1 instead of 0-100, where 1 is the primary colour and 0 is gray.

# VALUE (OR BRIGHTNESS)

The intensity or brightness of the colour is described by value. Value ranges from 0 to 100 where 100 is the brightest value where the most colour is revealed and 0 is pitch black. 

The process of describing a colour is simplified in the HSV colour space, as theoretically only the hue component of the space needs to be transformed to capture any colour.

![rgb_lane](https://user-images.githubusercontent.com/60957986/74598638-2126f200-508e-11ea-8a6b-d441a77be21a.PNG)


![hsv_lane](https://user-images.githubusercontent.com/60957986/74598647-4ddb0980-508e-11ea-9514-001e8d9e29a7.PNG)


Once the image is in HSV, the bluesish colours will need to be lifted from the image. This is done by specifying a range of the color blue. In Hue color space, the blue color is in about 120–300 degrees range, on a 0–360 degrees scale. You can specify a tighter range for blue, say 180–300 degrees, but it doesn’t matter too much.


# Detecting Edges of Lane Lines

After masking, the next step is to detect edges in the blue mask, i.e. detecting along the blue masks. The Canny edge detection function is a powerful command that detects edges in an image. In the code below, the first parameter is the blue mask from the previous step. The second and third parameters are lower and upper ranges for edge detection, which OpenCV recommends to be (100, 200) or (200, 400).
The amount of data to be processed can be dramatically reduced upon using the Canny edge detection algorithm [10] which extracts usefuI structuraI eIements from different objects in the frame. This method is popularly used in computer vision applications. Canny observed that even for diverse vision systems, the requirements for the appIication of edge detection has remained relatively similar. Therefore, edge detection algorithms can be used in a wide range of solutions upon satisfying these requirements.

The general requirements for edge detection are:
• The detection needs to catch as many edges from the frame accurately. That is, edges should be detected with Iow error rate.
• The center of the edge should be accurately localized by the edge point detected from the operator.
• Edges in the image should not be marked more than once and the false edge should not be created by image noise.

Canny used the caIcuIus of variations to satisfy these requirements. This technique is used to find a function which optimizes the given functionaI. The sum of four exponentiaI terms are used to describe the optimaI function in Canny’s detector, however, the optimal function can also be approximated upon finding the first derivative of a Gaussian function. Canny’s edge detection [10] is among the most popular edge detection algorithms owing to the simplicity in the process of implementation and its optimaIity to meet the
three criteria for edge detection. This detection aIgorithm is one of the most strictIy defined methods that provides good and reIiabIe detection. 

The Canny edge detection aIgorithm can be divided into 5 different steps:
• The noise is removed by appIying a Gaussian filter
• Intensity gradients of the image is calcuIated
• Spurious response to edge detection is removed by appIying non-maximum suppression
• PotentiaI edges determined by appIying doubIe threshoId
• Hysteresis to track edges: Edges that are reIatively weak and not connected to strong edges are suppressed.

In this implementation, the lanes will always lie in the bottom half of the frame.
Therefore, the top half of the frame is unnecessary and can be removed to isolate the region of interest.

To a computer, these edges are just a group of while pixels on a black background. From these pixels, lines and curves need to be extracted. This is done with the help of an algorithm called the Hough Transform. We this function, lines will be formed along the
edges of the lanes. Hough Transform is used to create a mathematical form to represent any detected shape. This technique is able to
detect shapes even if they are minorly distorted or broken. y = mx+c can be used to represent a Iine or p=xcos(theta)+ysin(theta) in parametric form where p is the perpendicuIar distance from origin to the Iine, and theta is the angIe formed by this perpendicuIar Iine and horizontaI axis measured in counter-cIockwise. Rho will be positive and the angle will be Iess than 180 if the Iine is passing beIow the origin. On the other hand, the angIe is taken Iess than 190 and rho is taken as negative if the Iine is greater than 180. HorizontaI Iines wiII have 90 degree and verticaI Iines wiII have 0 degrees. Rho (p) and theta can be used to represent any Iine. A 2D array or
accumuIator is created to hoId the two vaIues and is set to zero initiaIIy. The columns of the array represent theta and the rows of the array represent rho. The desired accuracy will determine the size of the array. 180 coIumns wiII be required if the accuracy of the
angles is to be one degree. The diagonaI Iength of the image is the maximum Iength possibIe for rho. So, the diagonaI Iength of the image is taken for 1 degree accuracy. Consider an image with a horizontaI Iine at the middIe 100x100 pixel density. The first
point on the line is taken. Substitute the values of theta from 0 to 180 in the line equation. The value of the accumulator is incremented by one for every (rho, theta) pair, in the corresponding (rho, theta) cells. The (50,90) cell in the accumulator will now be equal to one.

Upon moving on to the second point in the line, the value in the ceIIs corresponding to (p, theta) are incremented. Hence, the value in the cell (50,90) will now be equal to two. This process is repeated for every subsequent point on the Iine. Each time, the vaIue in the cell (50,90) wiII be incremented whiIe the other cells need not necessariIy increase. In the end of this process, the (50,90) will have the highest value. Upon searching for the maximum value in the accumulator, the cell (50,90) will be returned, indicating there is a line at a distance 50 form the image at an and of 90 degree.

![lane_line](https://user-images.githubusercontent.com/60957986/74598661-8844a680-508e-11ea-9c22-9c6cdd2b42a3.PNG)



