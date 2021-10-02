"""
Main file to run the program.
Imports Processor and UserSetting.

Uses cv2 to open the first webcam avaliable. While the webcame is avaliable calls Processor to process individual frame and detected the hands. Processor also moves the mouse based on the hand gesture. You will need opencv version 4.0.1 and numpy version 1.20.3
"""

import cv2
import time

from image_processor import Processor
from user_setting import User

def main():
    # Tracks FPS
    previous_time = 0
    current_time = 0

    # Open the first avaliable webcam
    cap = cv2.VideoCapture(0)

    # Initializes the User object to get all the user settings
    user = User()
    
    # Check if the user wants to update anything and display right/left hand gestures
    show_setting = True
    if show_setting:
        user.setting()
    print("\nRunning the program")
    print(user)
    
    # User custom variables 
    user_width = user.cap_width
    user_height = user.cap_height
    detection_confidence = user.detection_confidence
    show = user.show

    # Set camera_width and camera_height
    if user_width:
        cap.set(3, user_width)
    if user_height:
        cap.set(4, user_height)
        
    # Initializes the image_processor
    image_processor = Processor(user, detection_confidence=detection_confidence)

    top_left_bound = 5
    bottom_right_bound = 4
    
    while cap.isOpened():
        
        success, image = cap.read()
        
        if not success:
            print("EMPTY FRAME")
            continue

        height, width, _ = image.shape

        upper_left = (width // top_left_bound, height // top_left_bound)
        bottom_right = (width * bottom_right_bound // top_left_bound, height * bottom_right_bound // top_left_bound)
        if show:
            cv2.rectangle(image, upper_left, bottom_right, (0, 255, 0), thickness=2)

        # Process the image and check if there is a hand. Move the mouse according to the hand
        #image = processor.image_processor(image, camera_width, camera_height)
        image = image_processor.process(image, upper_left, bottom_right)
        
        # Calculate and show the FPS
        current_time = time.time()
        fps = 1 / (current_time - previous_time)
        previous_time = current_time
        fps = str(int(fps))
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        if show:
            cv2.putText(image, fps, (10, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)
        
        # Show the image, and set 'q' to exit
        if show:
            cv2.imshow('Image', image)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Release and destory 
    cap.release()
    cv2.destroyAllWindows()
    image_processor.release()

if __name__ == '__main__':
    main()