"""
The Processor class takes the arguments: user and optionally detection_confidence. The argument user, is a instance of the UserSetting class.
We need to import Hands from hands.py and import Mouse from mouse_control

The process() method takes a single image. It first detects the hands and then controls the mouse according to the hands gesture.
"""

from hands import Hands
from mouse_control import Mouse

class Processor:
    def __init__(self, user, detection_confidence=0.5) -> None:
        # Initialize Hands object to detect and track hands.
        self.hands = Hands(detection_confidence=detection_confidence)
        
        # Uses User object and gets all it's values
        self.movement_speed = user.movement_speed
        self.pause = user.pause
        self.right = user.right_positions
        self.left = user.left_positions
        self.position = user.mouse_point
        self.scroll_speed = user.scroll_speed
        self.right_angle = user.right_angle
        self.left_angle = user.left_angle
        self.show = user.show
        
        # Initialize Mouse object to control the mouse functions 
        self.mouse_control = Mouse(self.movement_speed, scroll_speed=self.scroll_speed, pause=self.pause, position=self.position)
        #self.mouse_control.set_camera_size(camera_width=camera_width, camera_height=camera_height)
        
        # Class variables
        self.hand_info = None
        self.right_finger_position = ()
        self.left_finger_position = ()
        self.right_action = {}
        self.right_landmark = []
        self.left_action = {}
        self.left_landmark = []
        
    def reset(self):
        """Resets the class variables"""
        self.hand_info = None
        self.right_finger_position = ()
        self.left_finger_position = ()
        self.right_action = {}
        self.right_landmark = []
        self.left_action = {}
        self.left_landmark = []
    
    def process(self, image, upper_left, bottom_right):   
        """Detects hands and then controls the mouse according to the hands gesture"""     
        # Detect the hand in the image
        image = self.hands.detect_and_track(image, draw=self.show, find_relative_pos=True)
        
        # Get the landmarks of the joints relative to our image
        self.hand_info = self.hands.get_hands_info()
        
        if self.hand_info:     
            self.mouse_control.set_tracking_size(upper_left=upper_left, bottom_right=bottom_right)
                   
            image = self.finger_info(image=image, hand_info=self.hand_info)
        else:
            self.reset()

        return image
            
    def finger_info(self, image, hand_info):
        """Gets which finger is open with finger_angles() method from the Hands class and the calls the perform_action() method from the Mouse class. """
        self.right_finger_position = ()
        self.left_finger_position = ()
        self.right_action = {}
        self.right_landmark = []
        self.left_action = {}
        self.left_landmark = []
        
        # Finds which finger are open or close from the fingers the user specified for both left and right hand
        for handedness, landmark in hand_info.values():
            self.set_finger_position(image, handedness, landmark)
        
        # Perform the action based on the finger postion
        self.perform_action_based_on_fingers()
        
        return image
    
    def set_finger_position(self, image, handedness, landmark):
        if handedness == 'Right':
            self.right_landmark = landmark
            for all_fingers, action_list in self.right.items():
                self.right_action = action_list
    
                self.right_finger_position = self.hands.finger_angles(all_fingers, landmark, find_finger_position=True, image=image, show=self.show, finger_open=self.right_angle)

        elif handedness == 'Left':
            self.left_landmark = landmark
            for all_fingers, action_list in self.left.items():
                self.left_action = action_list
                
                self.left_finger_position = self.hands.finger_angles(all_fingers, landmark, find_finger_position=True, image=image, show=self.show, finger_open=self.left_angle)

    
    def perform_action_based_on_fingers(self):
        if self.right_finger_position in self.right_action:
            action = self.right_action[self.right_finger_position]
            
            self.mouse_control.perform_action(action=action, landmark=self.right_landmark)
            
        if self.left_finger_position in self.left_action:
            action = self.left_action[self.left_finger_position]
            
            self.mouse_control.perform_action(action=action, landmark=self.left_landmark)
        
    def release(self):
        self.hands.reset()
        self.hands = None 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    