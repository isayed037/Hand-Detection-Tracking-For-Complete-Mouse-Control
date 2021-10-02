"""
The Hand() class is used to detect and track either 1 or 2 hands.
Detection and tracking is done with mediapipe version 0.8.7.1

The Hand() class takes optional arguments: detection_confidence and tracking_confidence, which are values from 0 - 1. It creates a mediapipe object that can detect/track any number of continuous images(a video).

The detect_and_track() method takes an image, and finds up to 2 hands and returns the image. 
Has 2 optionally arguments: draw and find_relative_pos. Both are defaulted to True. The draw argument draws the left or right hand. The find_relative_pos argument finds the location of the joints of the hands relative to our image.

The draw_left_or_right() method is used to draw a left or right hand. It takes an image and returns an updated image. Won't work by itself, detect_and_track() needs to be called first.

The find_handedness() method finds if the detected hand is a left or right hand, based on the current hand instance. Won't work by itself, detect_and_track() needs to be called first.

The relative_pos() method finds the relative position based on the image width and height and stores the handedness and position in hand_info. Won't work by itself, detect_and_track() needs to be called first.

The finger_angles() method takes a tuple of joints and landmarks for that hand and returns a list of the angles. Joints is a tuple with tuples containing 3 hand landmarks. The optional find_finger_position returns a tuple instead with 0 and 1 indicating if the finger was open or closed. The optional finger_open is used to check if the angle of the finger should be considered open or closed.

The class variable self.hand_info  is a hashmap. The keys of hashmap are hand_id, which is either 0 or 1 representing that there is 1 hand or 2 hands. The value is a tuple(handedness, landmarks). handedness indicates if this hand is a left or right hand. landmarks is a list of tuple(relative_x, relative_y), where relative_x and relative_y represent the relative x and y position of that landmark relative to the image. 
"""

import mediapipe as mp
import numpy as np
import cv2


class Hands:
    """Detects and tracks up to 2 hands from a video/webcam."""
    def __init__(self, detection_confidence=0.5, tracking_confidence=0.5) -> None:
        # Used to initialize the MediaPipe Hand object
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence
        
        # Initializes the Mediapipe drawing utils
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Initializes the MediaPipe Hand object
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(False, 2, self.detection_confidence, self.tracking_confidence)
        
        # Class variables
        self.hand_info = {}
        self.results = None
        self.image_height  = None 
        self.image_width = None
        
        #! TODO: Let user change the landmark and connection colors
        self.right_landmark_color = (121, 22, 76)
        self.right_connection_color = (250, 44, 250)
        
    def reset(self):
        """Resets the class variables."""
        self.hand_info = {}
        self.results = None
        self.image_height  = None 
        self.image_width = None
    
    def detect_and_track(self, image, draw=True, find_relative_pos=True):
        """Detect up to 2 hands from a image and starts to track them"""
        
        # Coverts the img to RGB from BGR
        # Mark image as not writeable(Improves performance)
        # Process the image to find the hands
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        
        self.results = self.hands.process(image)
        
        # Reset the flag and recovert the color
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # If there is a hand, find handedness. Draw or find relative postion for whichever is True
        if self.results.multi_hand_landmarks:
            self.image_height, self.image_width, _ = image.shape
            
            # Finds if its left or right hand and update self.hand_info
            self.find_handedness()
            
            if draw and find_relative_pos:
                image = self.draw_and_find(image)
            elif draw:
                image = self.draw_left_or_right(image)
            elif find_relative_pos:
                self.relative_pos()
        else:
            self.reset()
        
        return image
    
    def find_handedness(self):
        """Finds if the detected hands is either a left or right hand."""
        if not self.results.multi_hand_landmarks: return
        
        self.hand_info = {}

        for hand_id, hand_handedness in enumerate(self.results.multi_handedness):
            handedness = hand_handedness.classification[0].label
            
            self.hand_info[hand_id] = [handedness, None]
              
    def draw_and_find(self, image):
        """Does exactly the same thing as the methods draw_left_or_right() and relative_pos(), except it does both in one loop so it’s slightly faster."""
        # If there is no hands or handedness we just return. If there is no image we also return.
        if not self.results.multi_hand_landmarks: return
        if not self.hand_info[0][0]: return
        if not self.image_width or not self.image_height: return
        
        for hand_id, hand_landmarks in enumerate(self.results.multi_hand_landmarks):
            # Draws based on if it's the right or left hand
            self.draw(image=image, hand_id=hand_id, hand_landmarks=hand_landmarks)
            
            # Find all the landmark postion relative to our image
            relative_landmark = self.calculate_relative_landmark(hand_landmarks=hand_landmarks)
            
            self.hand_info[hand_id][1] = relative_landmark
    
        return image
        
    def draw_left_or_right(self, image):
        """Draws left or right hand for up to 2 hands"""
        if not self.results.multi_hand_landmarks: return
        if not self.hand_info[0][0]: return
        
        for hand_id, hand_landmarks in enumerate(self.results.multi_hand_landmarks): 
            # Draws based on if it's the right or left hand
            self.draw(image=image, hand_id=hand_id, hand_landmarks=hand_landmarks)
    
        return image
    
    def relative_pos(self):
        """Finds the landmarks postion relative to our image. Mediapipe landmark are a percentage."""
        if not self.results.multi_hand_landmarks: return
        if not self.image_width or not self.image_height: return
        if not self.hand_info[0][0]: return
         
        # Find all the landmark postion relative to our image    
        for hand_id, hand_landmarks in enumerate(self.results.multi_hand_landmarks):
            relative_landmark = self.calculate_relative_landmark(hand_landmarks=hand_landmarks)
            
            self.hand_info[hand_id][1] = relative_landmark
        
        return self.hand_info
    
    def draw(self, image, hand_id, hand_landmarks):
        """Helper function to draw based on hand_id and hand_landmarks"""
        if self.hand_info[hand_id][0] == 'Right':
                self.mp_drawing.draw_landmarks(
                    image, 
                    hand_landmarks, 
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing.DrawingSpec(color=self.right_landmark_color, thickness=2, circle_radius=2),
                    self.mp_drawing.DrawingSpec(color=self.right_connection_color, thickness=2, circle_radius=2),
                ) 
        else:
            self.mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                self.mp_hands.HAND_CONNECTIONS
            )
        
        return
    
    def calculate_relative_landmark(self, hand_landmarks):
        """Helper function to find to calculate relative landmark postions based on hand_landmarks"""
        relative_landmark = []
            
        for landmark in hand_landmarks.landmark:      
            relative_x, relative_y = int(landmark.x * self.image_width), int(landmark.y * self.image_height)
            relative_landmark.append((relative_x, relative_y))
        
        return relative_landmark
        
    #! TODO: Use cv2 contour to draw the line all the lines. Individually drawing each is too slow
    def finger_angles(self, joints, landmark, find_finger_position=False, image=None, show=False, finger_open=100):
        if not self.results: return
        if not self.results.multi_hand_landmarks: return
        if not self.hand_info: return
        
        finger_angle = []
        finger_pos = []
        # Loop through joints, and gets 3 landmark postions
        for joint in joints:
            joint_1 = np.array([landmark[joint[0]][0], landmark[joint[0]][1]])
            joint_2 = np.array([landmark[joint[1]][0], landmark[joint[1]][1]])
            joint_3 = np.array([landmark[joint[2]][0], landmark[joint[2]][1]])
                
            radians = np.arctan2(joint_3[1] - joint_2[1], joint_3[0]-joint_2[0]) - np.arctan2(joint_1[1]-joint_2[1], joint_1[0]-joint_2[0])
            angle = np.abs(radians*180.0/np.pi) 
            
            if angle > 180.0:
                angle = 360-angle
            
            if find_finger_position:
                if angle > finger_open:
                    finger_pos.append(1)
                    if show:
                        cv2.line(image, joint_1, joint_2, [0, 255, 0], 2)
                else:
                    finger_pos.append(0)
                    if show:
                        cv2.line(image, joint_1, joint_2, [0, 0, 255], 2)
            else:
                finger_angle.append(angle)
            
        if find_finger_position:
            return tuple(finger_pos) 
        else:           
            return finger_angle
    
    def get_hands_info(self):
        """Returns all the information for both left and right hand"""
        return self.hand_info
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    