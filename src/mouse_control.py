"""
The Mouse() class controls all mouse function with pyautogui version 0.9.48

The Mouse() class takes optional arguments: movement_speed, scroll_speed, pause, and position. The argument movement_speed controls how fast the mouse moves. The argument scroll_speed controls how much the screen scrolls up and down. The argument pause controls how long the mouse pauses for after every click. The argument position controls where in your hand the mouse is attached to. A position can be a number from 1-20 representing a mediapipe landmark. 
"""

import pyautogui
import numpy as np
import time

class Mouse:
    """Controls all mouse function."""
    def __init__(self, movement_speed=5, scroll_speed=20, pause=0.2, position=9) -> None:
        # Class variables
        self.movement_speed = movement_speed
        self.up = scroll_speed
        self.down = scroll_speed * -1
        self.pause = pause
        self.position = position
        
        self.previous_mouse_x, self.previous_mouse_y = 0, 0
        self.current_mouse_x, self.current_mouse_y = 0, 0
        
        self.upper_left, self.bottom_right = None, None
        
        # pyautogui setup
        pyautogui.PAUSE = 0
        pyautogui.FAILSAFE = False
        
        self.screen_width, self.screen_height = pyautogui.size()
        
    def set_tracking_size(self, upper_left, bottom_right): 
        """Sets the camera width and height"""
        self.upper_left = upper_left
        self.bottom_right = bottom_right
        
    def perform_action(self, action, landmark):
        """Check what the action is and then performs that action"""
        #print("Clicked: ", action, " At: ", int(self.cur_mouse_x), int(self.cur_mouse_y))
        
        if action == "MOVE":
            self.move_mouse(landmark)
        elif action == "CLICK":
            self.left_mouse_click()
        elif action == "RIGHT_CLICK":
            self.right_mouse_click()
        elif action == "DOUBLE_CLICK":
            self.double_click()
        elif action == "MIDDLE_CLICK":
            self.middle_click()
        elif action == "SCROLL_DOWN":
            self.scroll_down()
        elif action == "SCROLL_UP":
            self.scroll_up()
        elif action == "MOUSE_DOWN":
            self.mouse_down()
        elif action == "MOUSE_UP":
            self.mouse_up()
    
    def move_mouse(self, landmark):
        """Moves the moves based on the landmark and the specified postion"""
        pos_1, pos_2 = landmark[self.position]

        relative_x_pos = np.interp(pos_1, (self.upper_left[0], self.bottom_right[0]), (0, self.screen_width))
        relative_y_pos = np.interp(pos_2, (self.upper_left[1], self.bottom_right[1]), (0, self.screen_height))
                            
        self.current_mouse_x = self.previous_mouse_x + (relative_x_pos - self.previous_mouse_x) / self.movement_speed
        self.current_mouse_y = self.previous_mouse_y + (relative_y_pos - self.previous_mouse_y) / self.movement_speed
        
        if pyautogui.onScreen(self.current_mouse_x, self.current_mouse_y):
            pyautogui.moveTo(self.current_mouse_x, self.current_mouse_y)
            self.previous_mouse_x, self.previous_mouse_y = self.current_mouse_x, self.current_mouse_y
    
    def left_mouse_click(self):
        """Left clicks with the mouse where the mouse is at that time"""
        pyautogui.click(pyautogui.position())
        time.sleep(self.pause)

    def right_mouse_click(self):
        """Right clicks where the mouse is currently"""
        pyautogui.rightClick(pyautogui.position())
        time.sleep(self.pause)
        
    def double_click(self):
        """Double clicks where the mouse is currently"""
        pyautogui.doubleClick(pyautogui.position())
        time.sleep(self.pause)
    
    def middle_click(self):
        """Middle clicks where the mouse is currently"""
        pyautogui.middleClick(pyautogui.position())
        time.sleep(self.pause)
    
    def scroll_down(self):
        """Scrolls down the screen based on the speed specified"""
        pyautogui.scroll(self.down)
        
    def scroll_up(self):
        """Scrolls up the screen based on the speed specified"""
        pyautogui.scroll(self.up)
        
    def mouse_down(self):
        """Put the mouse down where it is currently, allows to drag"""
        pyautogui.mouseDown(pyautogui.position())
        time.sleep(self.pause)
    
    def mouse_up(self):
        """Put the mouse up where it is currently"""
        pyautogui.mouseUp(pyautogui.position()) 
        time.sleep(self.pause)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        