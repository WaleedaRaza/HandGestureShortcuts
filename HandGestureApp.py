import cv2
import mediapipe as mp
import pyautogui
import tkinter as tk
from PIL import Image, ImageTk

class HandGestureApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.video_source = 0
        self.vid = cv2.VideoCapture(self.video_source)
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.canvas = tk.Canvas(window, width=640, height=480)
        self.canvas.pack()

        self.btn_start = tk.Button(window, text="Start", width=10, command=self.start_gesture_recognition)
        self.btn_start.pack(padx=20, pady=20)

        self.btn_stop = tk.Button(window, text="Stop", width=10, command=self.stop_gesture_recognition)
        self.btn_stop.pack(padx=20, pady=20)

        self.btn_exit = tk.Button(window, text="Exit", width=10, command=self.window.quit)
        self.btn_exit.pack(padx=20, pady=20)

        # MediaPipe Hands setup
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.6)
        
        self.cooldown_frames = 0

        self.window.mainloop()

    def start_gesture_recognition(self):
        self.update()

    def stop_gesture_recognition(self):
        self.vid.release()

    def update(self):
        ret, frame = self.vid.read()
        if not ret:
            return

        frame = cv2.flip(frame, 1)  # Mirror the frame

        self.detect_gestures(frame)
        
        # Display the frame in the tkinter canvas
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        
        # If cooldown is active, reduce counter
        if self.cooldown_frames > 0:
            self.cooldown_frames -= 1

        self.window.after(10, self.update)
        
    def detect_gestures(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)

        if results.multi_hand_landmarks and self.cooldown_frames == 0:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                
                # Extracting hand landmarks
                index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                pinky_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP]
                index_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP]
                pinky_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_MCP]
                middle_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                middle_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
                ring_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP]
                ring_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_MCP]
                thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]

                # Swipe functionalities
                if (index_tip.x - thumb_tip.x > 0.1) and abs(index_tip.y - index_mcp.y) < 0.05:
                    pyautogui.hotkey('ctrl', 'right')  # swipe to the next desktop
                    cooldown_frames = 15

                elif (thumb_tip.x - index_tip.x > 0.1) and abs(index_tip.y - index_mcp.y) < 0.05:
                    pyautogui.hotkey('ctrl', 'left')  # swipe to the previous desktop
                    cooldown_frames = 15

                # Check if only the index finger is raised (for the copy action)
                finger_up = [index_tip.y < index_mcp.y, pinky_tip.y < pinky_mcp.y, middle_tip.y < middle_mcp.y, ring_tip.y < ring_mcp.y]

                if finger_up[0] and not finger_up[1] and not finger_up[2] and not finger_up[3]:
                    pyautogui.hotkey('command', 'c')  # copy
                    cooldown_frames = 15

                # Check if only the pinky finger is raised (for the paste action)
                elif not finger_up[0] and finger_up[1] and not finger_up[2] and not finger_up[3]:
                    pyautogui.hotkey('command', 'v')  # paste
                    cooldown_frames = 15

                # Check if the index, middle, and ring fingers are raised (for the select all action)
                elif finger_up[2] and finger_up[3] and not finger_up[1]:
                    pyautogui.hotkey('command', 'a')  # select all
                    cooldown_frames = 15

root = tk.Tk()
app = HandGestureApp(root, "Hand Gesture Recognition")
