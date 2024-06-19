import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
from pyzbar.pyzbar import decode

class App:
    def __init__(self, root, video_source=0):
        self.root = root
        self.video_source = video_source

        # Open the video source
        self.vid = cv2.VideoCapture(video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(root, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), 
                                        height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        # Button to take a snapshot
        self.btn_snapshot = ttk.Button(root, text="Snapshot", command=self.snapshot)
        self.btn_snapshot.pack(anchor=tk.CENTER, expand=True)

        # Update & display frames in the Tkinter window
        self.update()

        self.root.mainloop()

    def snapshot(self):
        # Get a frame from the video source and save it
        ret, frame = self.vid.read()
        if ret:
            cv2.imwrite("frame" + ".png", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            # do barcode detection here

    

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.read()
        if ret:
            # Convert the image to RGB (for PIL) and then to ImageTk format
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

            # or maybe even here?
        
        # Repeat after an interval to get the next frame
        self.root.after(10, self.update)  # update after 10 miliseconds

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Create a window and pass it to the Application object
App(tk.Tk())