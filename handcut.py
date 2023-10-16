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
        
        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        self.btn_start = tk.Button(window, text="Start", width=10, command=self.start_camera)
        self.btn_start.pack(padx=20, pady=20, side=tk.LEFT)
        
        self.btn_stop = tk.Button(window, text="Stop", width=10, command=self.stop_camera)
        self.btn_stop.pack(pady=20, side=tk.RIGHT)
        
        self.is_camera_running = False

        # Your gesture detection initialization code here
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.6)
        self.cooldown_frames = 0

        self.window.mainloop()

    def start_camera(self):
        self.is_camera_running = True
        self.update_camera_feed()

    def stop_camera(self):
        self.is_camera_running = False

    def update_camera_feed(self):
        ret, frame = self.vid.read()
        if self.is_camera_running and ret:
            # Your gesture detection code here
            frame = cv2.flip(frame, 1)
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(img_rgb)

            if self.cooldown_frames > 0:
                self.cooldown_frames -= 1

            if results.multi_hand_landmarks and self.cooldown_frames == 0:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                    # ... (Continue with the rest of your hand detection logic)

            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        if self.is_camera_running:
            self.window.after(10, self.update_camera_feed)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

root = tk.Tk()
app = HandGestureApp(root, "Hand Gesture Detection App")
