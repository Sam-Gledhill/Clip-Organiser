import os
import subprocess
import tkinter as tk
from tkinter import filedialog as fd

from pyvidplayer2 import VideoTkinter

DISPLAY_RESOLUTION = 720  # p
DEFAULT_CATEGORY = "No Category"


class App(tk.Tk):
    def __init__(self, vidpath):
        super().__init__()
        self.video = VideoTkinter(vidpath)
        self.video.change_resolution(DISPLAY_RESOLUTION)
        self.vidpath = vidpath
        self.title("Clip Manager")

        video_tkframe = tk.Frame(self)

        self.canvas = tk.Canvas(
            video_tkframe,
            width=self.video.current_size[0],
            height=self.video.current_size[1],
            highlightthickness=0,
        )
        self.canvas.pack()
        video_tkframe.pack()

        button_tkframe = tk.Frame(self)

        select_video_button = tk.Button(
            button_tkframe, text="Select Vid", command=self.select_vid
        )
        select_video_button.pack(side=tk.LEFT)

        pause_button = tk.Button(
            button_tkframe, text="||", command=self.video.toggle_pause
        )
        pause_button.pack(side=tk.LEFT, padx=3)

        self.start_timestamp = 0.0
        start_button = tk.Button(button_tkframe, text="START", command=self.set_start)
        start_button.pack(pady=5, side=tk.LEFT)

        self.end_timestamp = 0.0
        end_button = tk.Button(button_tkframe, text="END", command=self.set_end)
        end_button.pack(side=tk.LEFT, padx=3)

        publish_button = tk.Button(
            button_tkframe, text="PUBLISH", command=self.publish_clip
        )
        publish_button.pack(side=tk.LEFT, padx=20)

        self.selected_category = tk.StringVar(value=DEFAULT_CATEGORY)

        # lists only directories in folder "categories"
        categories = next(os.walk("categories"))[1]

        category_button = tk.OptionMenu(
            button_tkframe,
            self.selected_category,
            *categories,
            "Custom",
            command=self.check_custom_category,
        )
        category_button.pack(side=tk.LEFT)

        self.custom_category = tk.StringVar(value="")
        self.custom_category_button = tk.Entry(
            button_tkframe, textvariable=self.custom_category
        )

        button_tkframe.pack()

        seeker_tkframe = tk.Frame(self)
        self.seekervar = tk.DoubleVar()
        self.seeker = tk.Scale(
            seeker_tkframe,
            variable=self.seekervar,
            from_=0,
            to=self.video.duration,
            orient=tk.HORIZONTAL,
            length=self.video.current_size[0] - 20,
            tickinterval=10,
            command=self.seek,
        )
        self.seeker.pack(pady=5, side=tk.BOTTOM)

        seeker_tkframe.pack()

        self.update_video()

    def select_vid(self):

        # opens dialog in same folder as python file
        filepath = fd.askopenfilename(
            title="Select Video...",
            initialdir=__file__,
        )

        if len(filepath) == 0:
            print("NO FILE SELECTED. FALLING BACK.")
            return

        # Close old video stream
        self.video.close()

        # Reopen new one
        self.video = VideoTkinter(filepath)
        self.vidpath = filepath

        # Refresh variables
        self.seeker.configure(to=self.video.duration)
        self.selected_category.set(DEFAULT_CATEGORY)
        self.start_timestamp, self.end_timestamp = 0, 0
        self.video.change_resolution(DISPLAY_RESOLUTION)

    def check_custom_category(self, choice):
        if choice == "Custom":
            self.custom_category_button.pack(side=tk.LEFT, padx=2)
        else:
            self.custom_category_button.pack_forget()

    def set_start(self):
        self.start_timestamp = self.video.get_pos()

    def set_end(self):
        self.end_timestamp = self.video.get_pos()
        self.video.pause()

    def publish_clip(self):
        if self.end_timestamp <= self.start_timestamp:
            print("End before or equal to start timestamp, not publishing")
            return

        print("Publishing...")

        if self.selected_category.get() == DEFAULT_CATEGORY:
            cat_folder = ""
        elif self.selected_category.get() == "Custom":
            cat_folder = self.custom_category.get()
        else:
            cat_folder = self.selected_category.get()

        output_prefix = os.path.join("categories", cat_folder)
        output_suffix = f"{os.path.basename(self.vidpath.split('.')[0])}-{self.start_timestamp:.0f}-{self.end_timestamp:.0f}.mp4"
        output_path = os.path.join(os.getcwd(), output_prefix, output_suffix)

        if not os.path.exists(output_prefix):
            os.makedirs(output_prefix)

        # Clip video using ffmpeg - required to be installed on the path
        subprocess.Popen(
            [
                "ffmpeg",
                "-y",
                "-i",
                f"{self.vidpath}",
                "-ss",
                f"00:00:{self.start_timestamp}",
                "-t",
                f"00:00:{self.end_timestamp - self.start_timestamp}",
                output_path,
            ]
        )
        # subprocess.Popen(...).poll() checks if alive or not

    def get_timestamp(self) -> float:
        print(self.video.get_pos())
        return self.video.get_pos()

    def seek(self, e):
        self.video.seek(int(e), relative=False)

    def update_video(self):
        self.video.draw(
            self.canvas,
            (self.video.current_size[0] // 2, self.video.current_size[1] // 2),
            force_draw=False,
        )

        self.seekervar.set(self.video.get_pos())

        # Designed for if video ends. Might trigger on something else?
        if not self.video.active:
            self.video.restart()

        # TODO: get framerate from video file. 32ms ~= 30fps
        self.after(32, self.update_video)


app = App("selling_everything_scaled.mp4")
app.mainloop()
app.video.close()
