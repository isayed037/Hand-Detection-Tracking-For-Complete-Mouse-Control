# Hand-Detection-Tracking-For-Complete-Mouse-Control

Right and left hand detection and tracking with Mediapipe to fully control mouse movements and clicks.

Full mouse control with one hand or two hands. Choose which fingers to include and choose what the mouse will do based on which fingers are opened or closed. You can change how fast the mouse moves, how fast to scroll up or down the screen, to see the detection and tracking, and much more.
This is a project that I worked on by myself to better understand opencv, numpy, and mediapipe.

## Running and Requirements

Run `main.py` to run the application. All file imports are in `main.py` and `image_processor`.
The requirements are:

- mediapipe version 0.8.7.1
- opencv version 4.0.1
- pyautogui version 0.9.48
- numpy version 1.20.3

**Mouse Movement and Click and Drag Demonstration**
![Video](./docs/mouse_movement_click_and_drag.gif)

## Features

- You can move the mouse with your hand and control how fast the mouse moves.
- You can left, right, middle click, or double click with your hand.
- You can scroll up or down the screen with your hand and set the speed of the scroll.
- You can click and drag with your hand by first having the mouse button down and then moving the mouse.
- Choose which finger to include for each hand.
- Choose which fingers being open or closed will perform what action for each hand.
- You can see which hand is detected and which hand is open/closed.
  - Right hand is denoted by a pink color.
  - Left hand is denoted by a white color.
  - Finger open is denoted by a green color.
  - Finger closed is denoted by a red color.
- You can change the angle at which the program will determine if your left or right hand’s fingers are open or closed.
- You can control how long the mouse pauses for after you do any type of a click.
- You can change the detection and tracking confidence
  The default setting is that the Index, Middle, Ring, and Pinky fingers are included. For example, to move the mouse use your right hand and have all 4 four fingers open. For left clicking, close all 4 four fingers on your right hand. For right clicking, use your left hand and have all four fingers closed. Run the program to see all the finger positions and the related mouse action.
  If you want to permanently change the default setting, you should go to the user_setting.py file and change any of the default values and then save the file and rerun the program. Any setting update by pressing S when the program is running will only apply to that run and will reset back to the default when you close the program.

**Left, Middle, Right, and Double Click Demonstration**
The FPS drop in the video is because of the pause after every click. The actual click with the hand is smooth and accurate.
![Video](./docs/clicks_demo.gif)

### Contributions

If you have any ideas or contributions, feel free to create a pull request.

**Full Video Demonstration**
![Video](./docs/full_video_demonstration.gif)
Websites used in the demonstration:
https://mousetester.com/
https://cps-check.com/mouse-buttons-test
https://google.github.io/mediapipe/solutions/hands.html
