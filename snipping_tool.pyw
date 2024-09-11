from tkinter import filedialog
from mss import mss
from tkinter import *
from PIL import Image, ImageTk, ImageEnhance
from datetime import datetime

with mss() as sct:
    screenshot = sct.grab(sct.monitors[1])
img = Image.frombytes('RGB', (screenshot.width, screenshot.height), screenshot.rgb)

root = Tk()
root.attributes('-fullscreen', True)


enhancer = ImageEnhance.Brightness(img)
brightened_image = enhancer.enhance(0.5)
bg_img = ImageTk.PhotoImage(brightened_image)

bg_label = Label(root, image=bg_img)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

first = True


def quit_root():
    root.destroy()

def save_path(image):
    path = filedialog.asksaveasfilename(initialfile=f"Screenshot {datetime.now():%Y-%m-%d-%H-%M}",defaultextension=".jpg",
                                        filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")])
    if path:
        image.save(path)
    root.destroy()

def dragEvent(event=None):
    global first, first_x, first_y
    if first:
        first_x, first_y = event.x, event.y
        print('Dragging at x = % d, y = % d' % (event.x, event.y))
        first = False
    else:
        """
        Card size config for every direction
        """
        if event.x > first_x:
            # check if on right-side of screen
            if event.y > first_y:
                # check if y under the first click down
                card.place(x=first_x, y=first_y)
                card.config(width=(event.x - first_x), height=(event.y - first_y))
            else:
                card.place(x=first_x, y=event.y)
                card.config(width=(event.x - first_x), height=(first_y - event.y))
        if event.x < first_x:
            # check if on left-side of screen
            if event.y > first_y:
                # check if y under the first click down
                card.place(x=event.x, y=first_y)
                card.config(width=(first_x - event.x), height=(event.y - first_y))
            else:
                card.place(x=event.x, y=event.y)
                card.config(width=(first_x - event.x), height=(first_y - event.y))


def move(event=None):
    if not first:
        print(card.winfo_width(), card.winfo_height())
        print(img.size)
        new_image = img
        if event.x > first_x:
            if event.y > first_y:
                new_image = img.crop((first_x, first_y, event.x, event.y))
            else:
                new_image = img.crop((first_x, event.y, event.x, first_y))
        if event.x < first_x:
            print(event.x, first_x)
            if event.y > first_y:
                new_image = img.crop((event.x, first_y, first_x, event.y))
            else:
                new_image = img.crop((event.x, event.y, first_x, first_y))
        save_path(new_image)


card = Canvas(root, width=0, height=0, highlightthickness=0,  bd=0, bg="gray64")
root.wm_attributes('-transparentcolor','gray64')
card.pack()
root.bind("<B1-Motion>", dragEvent)
root.bind("<ButtonRelease-1>", move)

root.mainloop()
