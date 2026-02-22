"""
This is a quick example of integrating a video into a tkinter project
"""

# Sample videos can be found here: https://github.com/anrayliu/pyvidplayer2-test-resources/tree/main/resources

import tkinter as tk

from pyvidplayer2 import VideoTkinter


class App(tk.Tk):
    def __init__(self, vidname):
        super().__init__()
        self.video = VideoTkinter(vidname)

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
        gcf_button = tk.Button(button_tkframe, text="Hello", command=self.get_timestamp)
        gcf_button.pack(pady=5)

        self.seekervar = tk.DoubleVar()
        seeker = tk.Scale(
            button_tkframe,
            variable=self.seekervar,
            from_=0,
            to=self.video.duration,
            orient=tk.HORIZONTAL,
            length=self.video.current_size[0] - 20,
            tickinterval=10,
            command=self.seek,
        )
        seeker.pack(pady=5)

        button_tkframe.pack()

        self.update_video()

    def get_timestamp(self) -> float:
        print(self.video.get_pos())
        return self.video.get_pos()

    def seek(self, e):
        self.video.pause()
        self.video.seek(int(e), relative=False)
        self.video.resume()

    def update_video(self):
        self.video.draw(
            self.canvas,
            (self.video.current_size[0] // 2, self.video.current_size[1] // 2),
            force_draw=False,
        )

        self.seekervar.set(self.video.get_pos())

        # Designed for if video ends. Might trigger on pause?
        if not self.video.active:
            self.video.restart()

        self.after(32, self.update_video)


app = App("selling_everything_scaled.mp4")
app.mainloop()
app.video.close()
