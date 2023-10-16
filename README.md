# HandGestureShortcuts
Hand gesture shortcuts for mac



Overview
This Python project demonstrates hand gesture recognition using the MediaPipe library. It allows you to control your Mac by performing specific hand gestures in front of your webcam. You can perform actions such as navigating between desktops, copying, pasting, selecting all, and triggering the Backspace action with various hand gestures.

Functionalities
Swipe to the next desktop by pointing your index and middle finger to the right.
Swipe to the previous desktop by moving your index and middle finger to the right.
Copy text or content by raising only your index finger.
Paste text or content by raising only your pinky finger.
Select all text or content by raising your index, middle, and ring fingers.

Prerequisites
Before running the project, ensure you have the following installed:

Python 3.x (download and install from python.org)
Required Python libraries:
OpenCV (cv2)
MediaPipe (mediapipe)
PyAutoGUI (pyautogui)
Pillow (PIL, for image processing)
tkinter (usually comes bundled with Python)
You can install these dependencies using pip with the following commands:
pip install opencv-python
pip install mediapipe
pip install pyautogui
pip install Pillow

Use your webcam to perform the specified hand gestures in front of your computer to trigger the corresponding actions.
Troubleshooting
If you encounter issues with permissions (e.g., on macOS) when running PyAutoGUI commands, grant necessary permissions to allow keyboard and mouse control.
License
This project is licensed under the MIT License.

Contributing
Feel free to contribute to this project. You can report issues, suggest improvements, or submit pull requests.

Author
Waleed Raza
Waleedraza1211@gmail.com
Acknowledgments
MediaPipe (https://mediapipe.dev/)
