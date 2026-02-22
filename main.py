"""
This is a quick example of integrating a video into a tkinter project
"""

# Sample videos can be found here: https://github.com/anrayliu/pyvidplayer2-test-resources/tree/main/resources

import tkinter as tk

from numpy import pad
from pyvidplayer2 import VideoTkinter

video = VideoTkinter("selling_everything_scaled.mp4")


def get_timestamp() -> float:
    print(video.get_pos())
    return video.get_pos()


root = tk.Tk()
root.title("Clip Manager")

video_frame = tk.Frame(root)
button_frame = tk.Frame(root)


canvas = tk.Canvas(
    video_frame,
    width=video.current_size[0],
    height=video.current_size[1],
    highlightthickness=0,
)
canvas.pack()
video_frame.pack()

gcf_button = tk.Button(button_frame, text="Hello", command=get_timestamp)
gcf_button.pack()

w_var = tk.DoubleVar()


def seek(e):
    video.pause()
    video.seek(int(e), relative=False)
    video.resume()


w = tk.Scale(
    button_frame,
    variable=w_var,
    from_=0,
    to=video.duration,
    orient=tk.HORIZONTAL,
    length=video.current_size[0] - 20,
    tickinterval=10,
    command=seek,
)
w.pack(pady=5)

button_frame.pack(pady=10, padx=10, side=tk.LEFT)


def update():
    video.draw(
        canvas,
        (video.current_size[0] // 2, video.current_size[1] // 2),
        force_draw=False,
    )

    w_var.set(video.get_pos())

    if video.active:
        root.after(32, update)  # for around 60 fps
    else:
        pass
        video.restart()
        video.resume()


update()
root.mainloop()

video.close()
