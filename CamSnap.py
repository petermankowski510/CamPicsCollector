"""Module Documentation
   author: Peter Mankowski
   date: Nov, 14, 2019
   description:
   1. Automatically collect images with programmable intevals
   2. Safe all pictures in one folder
   3. Determine which pics are out of focus and remove them(Delete)
   4. Note: Each picture's name is the 'name' + counter format
   5. Name changes are allowed 
"""

import cv2
from imutils import paths
import argparse
import os 

def variance_of_laplacian(image):
    # compute the Laplacian of the image and then return the focus
    # measure, which is simply the variance of the Laplacian
    return cv2.Laplacian(image, cv2.CV_64F).var()

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True,
    help="path to input directory of images")
ap.add_argument("-t", "--threshold", type=float, default=90.0,
    help="focus measures that fall below this value will be considered 'blurry'")
args = vars(ap.parse_args())

# UI part
FileName = input("Enter a file name(no spaces allowed): ")
print("Echo =>", FileName)
print("Video recording: 'ON'")
print("Press 'q' to stop")

# 1.creating a video object
video = cv2.VideoCapture(0) 
# 2. Variable List
a = 0 # Counter used for image names
mydel = 1 # One second delay between eah image snap

while True:
    a = a + 1
    
    check, frame = video.read() #Create a frame object
    
    cv2.imshow("Capturing",frame)

    key = cv2.waitKey(mydel)
    if key == ord('q'):
        break
    # image saving
    FileNameNum = FileName+'_'+str(a)+'.png'
    showPic = cv2.imwrite('C:\\Users\\seeho\\CamPics\\'+FileNameNum,frame)

print(showPic)
# 8. shutdown the camera
video.release()
cv2.destroyAllWindows 

print(args)
#print(paths.list_images(args["C:\\Users\\seeho\\CamPics\\"]))
cnt=0
# loop over the input images
for imagePath in paths.list_images("C:\\Users\\seeho\\CamPics\\"):
    # load the image, convert it to grayscale, and compute the
    # focus measure of the image using the Variance of Laplacian
    # method
    print(imagePath)
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fm = variance_of_laplacian(gray)
    text = "Not Blurry"

    # if the focus measure is less than the supplied threshold,
    # then the image should be considered "blurry"
    if fm < args["threshold"]:
        os.remove(imagePath)
        cnt=cnt+1
        #text = "Blurry"

    # show the image
    cv2.putText(image, "{}: {:.2f}".format(text, fm), (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
    cv2.imshow("Image", image)
    #key = cv2.waitKey(0)

print("Image directory Summary:")
# Extract dir information
path, dirs, files = next(os.walk("C:\\Users\\seeho\\CamPics"))
# pics counter
pic_count = len(files)
print("Number of good pictures:", pic_count)
print("Deleted pictures:",cnt)


