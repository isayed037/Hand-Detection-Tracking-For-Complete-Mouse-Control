""" 
The User class is used to get the default/custom setting from the user input. 
If you want to permanently change the setting, change the default values.


0 represents when the finger is closed
1 represents when the finger is open
The fingers Thumb, Index, Middle, Ring, and Pinky, 
"""
import pprint

#* ALL DEFAULT VALUES

# The landmark poisition on the hand that the mouse will track. Default is the bottom of the middle finger. FOr example, 8 would be the tip of the index finger and 12 would be the tip of the middle finger.
# Check mediapipe hands website to find all landmarks and their postions. https://google.github.io/mediapipe/solutions/hands.html
mouse_point = 9

# Controls how fast the screen scrolls up or down
#! TODO: Have different speed for moving up and down
scroll_speed = 20

# This is the angle at which we consider a finger to be open. Range 0-180
right_angle = 100
left_angle = 100

# This set the width and height of the camera
cap_width = 1280
cap_height = 720

# Controls how fast the mouse moves compared to the hand
movement_speed = 4

# Controls how long to pause after a left/right click
pause = 0.3

# Shows the video with drawings.
show = True

# Sets the detection_confidence which goes from 0-1
detection_confidence = 0.8

# Sets the tracking confidence which goes from 0-1
tracking_confidence = 0.5

# JOINT_LANDMARK represents the landmarks mediapipe uses to identify each finger
JOINT_LANDMARK = {
    'Thumb': (4,2,0),
    'Index': (8,6,0),
    'Middle': (12,10,0),
    'Ring': (16,14,0),
    'Pinky': (20,18,0),
}

JOINT_LANDMARK_REVERSE = {
    (4,2,0): 'Thumb',
    (8,6,0): 'Index',
    (12,10,0): 'Middle',
    (16,14,0): 'Ring',
    (20,18,0): 'Pinky',
}

# All the actions the mouse can perform
MOUSE_ACTIONS = ["MOVE", "CLICK", "RIGHT_CLICK", "DOUBLE_CLICK", "MIDDLE_CLICK", "SCROLL_UP", "SCROLL_DOWN", "MOUSE_DOWN", "MOUSE_UP",]

# Default number of fingers included. I would recommend not to use the Thumb finger. 
# If you want to update the default, I would recommend updating it in setting on the command prompt first and then copying and pasting onto here.
IMRP = ((8, 6, 0), (12, 10, 0), (16, 14, 0), (20, 18, 0))

# The key represents which finger to be included. The key is a tuple of JOINT_LANDMARK. 
#   - A key of ((JOINT_LANDMARK[Index]), (JOINT_LANDMARK[Middle])) -> Includes index and middle finger for right hand
# The values are another dictionary. 
# The keys of the second dictionary represent which fingers going from left to right in the same order is open or closed
#   - 0 means that finger is closed and 1 mean that finger is open
#   - (1,1,1,1) -> Represent Index, Middle, Ring, Pinky(IMRP) fingers are open
# The values of the second dictionary is an mouse actions from the MOUSE_ACTIONS list
right_default_positions = {
    IMRP: {
        (1,1,1,1): "MOVE",
        (0,0,0,0): "CLICK",
        (1,1,0,0): "SCROLL_DOWN",
        (1,0,0,0): "SCROLL_UP",
    }
}

# Same format as right_default_positions
left_default_positions = {
    IMRP: {
        (0,0,0,0): "RIGHT_CLICK",
        (0,1,1,1): "DOUBLE_CLICK",
        (1,0,0,1): "MIDDLE_CLICK",
        (1,1,1,0): "MOUSE_DOWN",
        (1,1,0,0): "MOUSE_UP",
    }
}

pp = pprint.PrettyPrinter()

#! TODO: REFACTOR THIS ENTIRE CLASS
class User:
    def __init__(self, right_positions=right_default_positions, left_positions=left_default_positions, mouse_point=mouse_point, scroll_speed=scroll_speed, right_angle=right_angle, left_angle=left_angle, cap_width=cap_width, cap_height=cap_height, movement_speed=movement_speed, show = show, pause=pause, detection_confidence=detection_confidence, tracking_confidence=tracking_confidence) -> None:
        
        # Key for right and left hand gestures
        self.right_positions = right_positions
        self.left_positions = left_positions

        # Mouse point
        self.mouse_point = mouse_point
        # Scroll speed
        self.scroll_speed = scroll_speed
        # This is the angle at which we consider a finger to be open. Range 0-180
        self.right_angle = right_angle
        self.left_angle = left_angle
        
        # This set the width and height of the camera
        self.cap_width = cap_width
        self.cap_height = cap_height
        
        # # Controls how fast the mouse moves compared to the hand
        self.movement_speed = movement_speed
                
        # Controls how long to pause after a left/right click
        self.pause = pause
        
        # Show the image
        self.show = show
        
        # Sets the detection_confidence
        self.detection_confidence = detection_confidence
        
        # Sets the tracking confidence
        self.tracking_confidence = tracking_confidence
        
    def __repr__(self) -> str:
        print("\n------------------------------------")
        print("Right hand controls: ")
        for key in self.right_positions.keys():
            pp.pprint(self.right_positions[(key)])
        print("\nLeft hand controls: ")
        for key in self.left_positions.keys():
            pp.pprint(self.left_positions[key])
        print("--------------------------------------")
        
        return ''
            
    def setting(self):        
        setting_input = input(" - Press R to run. \n - Press S for settings. \n - Type(R/S): ")
        if setting_input == 'S' or setting_input == 's':
            self.update_setting()
    
    #! TODO: Let user change all of the settings
    def update_setting(self):
        print("\nType the number next to the value to update it.")
        print("Or press R to run the program")
        print("\n   Value:     Current default")
        print("1. Show: ", self.show)
        
        print("\n2. Update right hand: ")
        for key in self.right_positions.keys():
            pp.pprint(self.right_positions[(key)])
        print("\n3. Update left hand: ")
        for key in self.left_positions.keys():
            pp.pprint(self.left_positions[key])
        
        update_input = input("\n- Type(#/R): ")
        if update_input == 'R' or update_input == 'r':
            return
        elif update_input == '1':
            self.update_show()
        elif update_input == '2':
            self.update_right()
        elif update_input == '3':
            self.update_left()
        
        self.update_setting()
    
    def update_show(self):
        print("\nDo you want to see the video? Type (T/F)")
        show_input = input("- Show? (T/F): ")
        
        if show_input == 'T' or show_input == 't':
            self.show = True 
        elif show_input == 'F' or show_input == 'f':
            self.show = False
        else:
            print("Enter valid input")
            self.update_show()
        
        return
    
    def update_right(self):
        print("\nPress S at any input to return to settings page and keep the default")
        print("First chose which finger you want to include for your right hand.")
        update_right_finger = []
        for key in JOINT_LANDMARK.keys():
            if self.add_finger(update_right_finger, key):
                return
        
        if len(update_right_finger) < 2:
            print("\nHave to include at least 2 finger.")
            print("Keeping the default and returning to settings page.")
            return
        
        print("\nNow chose an action you want perform with your right hand and then chose the fingers that will perform the action.")
        action_list = {}
        for action in MOUSE_ACTIONS:
            if self.add_action(action_list, update_right_finger, action, "Right"):
                return
        
        self.right_positions.clear()
        self.right_positions[tuple(update_right_finger)] = action_list
        return
    
    def update_left(self):
        print("\nPress S at any input to return to settings page and keep the default.")
        print("First chose which finger you want to include for your left hand.")
        print(" - You should avoid using the Thumb finger, since it is not as accurate as other fingers.")
        update_left_finger = []
        for key in JOINT_LANDMARK.keys():
            if self.add_finger(update_left_finger, key):
                return
        
        if len(update_left_finger) < 2:
            print("\nHave to include at least 2 finger.")
            print("Keeping the default and returning to settings page.")
            return
        
        print("\nNow chose an action you want perform with your left hand and then chose the fingers that will perform the action.")
        action_list = {}
        for action in MOUSE_ACTIONS:
            if self.add_action(action_list, update_left_finger, action, "Left"):
                return
        
        self.left_positions.clear()
        self.left_positions[tuple(update_left_finger)] = action_list
        return
        
    def add_finger(self, finger_list, key):
        print(f"Do you want to include the {key} finger? Press Y or N")
        
        finger = input("- Type(Y/N): ")
        if finger == 'Y' or finger == 'y':
            finger_list.append(JOINT_LANDMARK[key]) 
        elif finger == 'N' or finger == 'n':
            return False
        elif finger == 'S' or finger == 's':
            print("Keeping the default and returning to settings page")
            return True
        else:
            print("Invalid input, thumb won't be included")
        
        return False
        
        
    def add_action(self, action_list, finger_list, action, hand):
        finger_pos = []
        
        print(f'\n Do you want to {action} with the {hand} hand? (Y/N)')
        a = input("- Type(Y/N): ")
        if a == 'Y' or a == 'y':            
            for finger in finger_list:
                print(f"Do you want {JOINT_LANDMARK_REVERSE[finger]} finger to be open or closed to {action}?")
                p = input("- Type(O/C): ")
                if p == 'O' or p == 'o':
                    finger_pos.append(1)
                elif p == 'C' or p == 'c':
                    finger_pos.append(0)
                elif p == 'S' or p == 's':
                    print("Keeping the default and returning to settings page")
                    return True
                else:
                    print("Invalid input, Keeping the default and returning to settings page")
                    return True
        elif a == 'N' or a == 'n':
            return False
        elif a == 'S' or a == 's':
            print("Keeping the default and returning to settings page")
            return True
        else:
            print("Invalid input, Keeping the default and returning to settings page")
            return True
                
        action_list[tuple(finger_pos)] = action
                
                
                    
                
        